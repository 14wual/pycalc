@echo off

set PYTHON_INSTALLER=src\python-3.11.3-amd64.exe

echo Installing Python...
start /wait %PYTHON_INSTALLER% /quiet PrependPath=1

echo Python installed successfully.

echo Installing dependencies...
python -m pip install -r requirements.txt

echo Dependencies installed successfully.

echo Press any key to exit.
pause >nul
