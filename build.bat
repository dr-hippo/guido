pyinstaller game.py -F --noconfirm --log-level=WARN ^
--add-data "audio;audio" --add-data "fonts;fonts" --add-data "images;images" ^
-n "Guido the Snake Charmer" ^
--noconsole -i "images\icon.ico"
pause