# SPONGE'S MP3 PLAYER
This is a fully functioning mp3 player originally intended to be put on a Raspberry Pi, but I've added support for Windows.
Essentially, it's a directory viewer but with the capability of playing mp3s.
So how do you use it?
1. Run it in the command line with `python main.py`.

Or:
1. Build it by launching the `makefile.bat`. This will build an exe file using pyinstaller for ease of use.
2. Find the `.exe` file in the `dist` folder.
3. Drag the file out of the folder, into a directory with mp3 files (or folders as albums).
4. Launch the file.
5. Enjoy your music.

### HOTKEYS
|Hotkey|Control|Hotkey|Control|
|------|-------|------|-------|
|q|View Switch|a|Rewind
|w|Back|s|Pause/Play|
|e|Select|d|Fast Forward|
|r|Navigate Up|f|Navigate Down|
|PageUp|Volume Up|PageDown|Volume Down|
|a + s|Previous/Beginning|s + d|Next|
|a + s + d|Stop|