using System;
using System.IO;
using System.Windows.Forms;
using NetManager;

namespace Client
{
    public partial class Form1 : Form
    {
        Stream outputStream;
        public Form1()
        {
            InitializeComponent();
            myClientControl1.Client.Reseive += Client_Reseive;
            myClientControl1.Client.Error += Client_Error;

            outputStream = Console.OpenStandardOutput();
        }

        private void Client_Error(object sender, EventMsgArgs e)
        {
            MessageBox.Show(e.Msg, "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }

        private void Client_Reseive(object sender, NetManager.EventClientMsgArgs e)
        {
            int n = BitConverter.ToInt32(e.Msg, 0);
            n = (e.Msg.Length - 68) / 2;
            short[] data = new short[n];
            for (int i = 0; i < n; i++)
            {
                data[i] = BitConverter.ToInt16(e.Msg, 68 + 2 * i);
            }
            byte[] buffer = new byte[data.Length * sizeof(short)];
            Buffer.BlockCopy(data, 0, buffer, 0, buffer.Length);
            outputStream.Write(buffer, 0, buffer.Length);
            outputStream.Flush();
        }
    }
}
