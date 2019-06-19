$env:PATH += ";$PWD\src"
#start-process -WindowStyle Hidden "python ./src/main.py --config-file=D:/projects/TCYEndManager/config.json"
python ./src/main.pyw --config-file=D:/projects/TCYEndManager/config.json
