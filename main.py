import sys
import subprocess
import struct
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, 
    QVBoxLayout, QWidget, QTextEdit, 
    QHBoxLayout, QLineEdit
)
from PyQt6.QtCore import QThread, pyqtSignal
import queue
import threading
import time
from collections import deque

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# путь до исполняемого файла
path_to_csharp_exe = "Client/Client/bin/Debug/Client.exe"
# количество чисел в пакете. не менять, если не знаете, что делаете
num_elements = 696
# размер short в байтах. не менять, если не знаете, что делаете
elements_size = 2
# индекс канала, с которого читаете значения.
# индексация с 1 (12 - FP2-A2)
channel_ind = 12
# количество чисел в пакете на канал. не менять, если не знаете, что делаете
elements_per_channel = 24


class PipeReaderThread(QThread):
    """
    Класс, отвечающий за постоянное чтение поступающих пакетов от C# прослойки.
    Исполняется в отдельном потоке.
    """
    data_ready = pyqtSignal()

    def __init__(self, pipe, q):
        super().__init__()
        self.pipe = pipe
        self.q = q
        self.running = True

    def run(self):
        while self.running:
            data = self.pipe.read(num_elements * elements_size)
            if not data:
                break
            self.q.put(data)
            self.data_ready.emit()

    def stop(self):
        self.running = False


def wait_array(q, num_elements, elements_size, element_type='h'):
    """
    Функция для чтения пакета с числами из стандартного вывода C# прослойки.
    Важно: не чистит вывод, т.е. данные не являются свежими.
    """
    expected_bytes = num_elements * elements_size
    data = b''
    while len(data) < expected_bytes:
        try:
            data += q.get(timeout=1)
        except queue.Empty:
            continue
    if len(data) < expected_bytes:
        return None
    return struct.unpack(f'{num_elements}{element_type}', data)


def empty_pipe(q):
    """
    Чистит стандартный вывод C# прослойки.
    """
    while not q.empty():
        q.queue.clear()


def stream_channel_windows(q, channel_ind, window_size, num_elements, elements_size):
    """
    Генератор данных от C# прослойки. Получает только самые свежие данные.
    Нужен для основного цикла программы после калибровки.
    """
    buffer = deque(maxlen=window_size)
    empty_pipe(q)
    while True:
        raw = wait_array(q, num_elements, elements_size)
        if raw is None:
            break
        buffer += raw[elements_per_channel * (channel_ind - 1):elements_per_channel * channel_ind]
        if len(buffer) == window_size:
            yield np.array(buffer, dtype=np.int32)
            buffer.clear()
            empty_pipe(q)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signal Control Interface")

        self.begin_csharp_button = QPushButton("Включить C# прослойку")
        self.begin_csharp_button.clicked.connect(self.begin_csharp_process)

        self.sliding_window_input = QLineEdit("500")

        self.start_button = QPushButton("Начать калибровку")
        self.start_button.clicked.connect(self.begin_calibration)

        self.inference_button = QPushButton("Основной цикл")
        self.inference_button.clicked.connect(self.begin_inference)

        self.status_log = QTextEdit()
        self.status_log.setReadOnly(True)
        self.status_log.textChanged.connect(lambda: self.status_log.verticalScrollBar().setValue(self.status_log.verticalScrollBar().maximum() + 10))

        self.canvas = FigureCanvas(Figure(figsize=(16, 10)))

        control_layout = QVBoxLayout()
        control_layout.addWidget(self.begin_csharp_button)
        control_layout.addWidget(QLabel("Окно значений"))
        control_layout.addWidget(self.sliding_window_input)
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.inference_button)
        
        control_layout.addWidget(QLabel("Status log:"))
        control_layout.addWidget(self.status_log)

        canvas_layout = QVBoxLayout()
        canvas_layout.addWidget(QLabel("Calibration plots"))
        canvas_layout.addWidget(self.canvas)

        layout = QHBoxLayout()
        layout.addLayout(control_layout)
        layout.addLayout(canvas_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.proc = None
        self.q = queue.Queue()
        self.reader_thread = None
        self.calibrating = False
        self.inferencing = False

    def log(self, text):
        self.status_log.append(text)
        self.status_log.verticalScrollBar().setValue(self.status_log.verticalScrollBar().maximum() + 10)

    def begin_csharp_process(self):
        self.log("Включаем C# прослойку...")
        self.proc = subprocess.Popen(
            [path_to_csharp_exe],
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0
        )
        self.reader_thread = PipeReaderThread(self.proc.stdout, self.q)
        self.reader_thread.start()
        self.log("C# прослойка включена. В прослойке подключитесь к NMServer.")

    def begin_calibration(self):
        # todo lock everithing
        if not self.calibrating:
            self.calibrating = True
            threading.Thread(target=self.calibration_stage, daemon=True).start()
        else:
            self.calibrating = False

    def calibration_stage(self):
        # clear axes
        for ax in self.canvas.figure.axes:
            ax.remove()
        
        empty_pipe(self.q)
        start = time.time()
        calibration_time = 10
        squeeze_timings = [(0.1, 2.5), (5.5, 7.5)]
        current_timing = 0
        data = []
        data_timings = []
        insertint_timing = False

        while True:
            if not self.calibrating:
                return

            shorts = wait_array(self.q, num_elements, elements_size)
            if shorts is None:
                break
            data += shorts[elements_per_channel * (channel_ind - 1):elements_per_channel * channel_ind]

            now = time.time()
            if now - start >= calibration_time:
                break

            if current_timing == len(squeeze_timings):
                continue

            if now >= start + squeeze_timings[current_timing][0]:
                if not insertint_timing:
                    insertint_timing = True
                    data_timings.append([len(data) - 25, -1])
                    self.log("Начало сегмента")
                elif now > start + squeeze_timings[current_timing][1]:
                    data_timings[-1][1] = (len(data) - 1)
                    current_timing += 1
                    insertint_timing = False
                    self.log("Конец сегмента")

        data = np.array(data)
        self.calibrating = False
        self.log(f"Собрали {data.shape[0]} значений")
        self.log(f"Сегменты: {data_timings}")

        axs = self.canvas.figure.subplots()
        axs.plot(data)

        self.canvas.figure.tight_layout()
        self.canvas.draw()
    
    def begin_inference(self):
        if not self.inferencing:
            self.inferencing = True
            threading.Thread(target=self.inference_stage, daemon=True).start()
        else:
            self.inferencing = False

    def inference_stage(self):
        sliding_window = int(self.sliding_window_input.text())

        # begin streaming
        for chunk in stream_channel_windows(self.q, channel_ind, sliding_window, num_elements, elements_size):
            if not self.inferencing:
                return
            
            self.log(f"Получили {chunk.shape[0]} значений.")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())