pyinstaller game.py -F --noconfirm --log-level=WARN ^
--add-data "audio;audio" --add-data "fonts;fonts" --add-data "images;images"  --add-data "level-data;level-data" ^
-n "GuidoTheSnakeCharmer" --hidden-import "tile" ^
--noconsole -i "images\icon.ico"