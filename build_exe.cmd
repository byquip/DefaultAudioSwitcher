pyinstaller --onefile --noconsole res/main_app.py --icon=res/hp.ico --add-data "res\hp.ico;\res" --add-data "res\hp.ico;." --add-data "res\hp.png;." --add-data "res\nircmd.exe;." --add-data "res\*.py;."