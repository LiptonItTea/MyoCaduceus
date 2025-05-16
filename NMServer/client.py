import clr
import sys
from pathlib import Path
import inspect

# Path to the directory containing NetManager.dll
dll_path = Path(r'D:\\Coding\\чми\\server\\NetManager.dll').resolve()
sys.path.append(str(dll_path.parent))

# Load the DLL
clr.AddReference('NetManager')  # No .dll extension

# Now you can import namespaces/classes
from NetManager.Client import NMClient

# Print constructor signatures
constructors = inspect.getmembers(NMClient, predicate=inspect.isfunction)
for name, method in constructors:
    if name == '__init__':
        print("Constructor:", method)