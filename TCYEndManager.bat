@echo off
set PYTHONPATH=%PYTHONPATH%;%cd%\src
start /b pythonw ./src/main.pyw --config-file=%cd%/config.xml --log-dir=%cd%/logs