@echo off

python3.12 -m pip install -r .\requirements.txt
echo Installed requirements

python3.12 -m uvicorn main:app --host "127.0.0.1" --port 8100

pause