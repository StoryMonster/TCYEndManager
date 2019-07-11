$env:PATH += ";$PWD\src"
pythonw ./src/main.pyw --config-file=$PWD/config.xml --log-dir=$PWD/logs
