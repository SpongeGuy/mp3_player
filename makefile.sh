#!/bin/bash
pyinstaller --onefile --windowed --icon="spongex64mp3.ico" --add-data="spongex64mp3.ico;." -n MP3_PLAYER main.py
read -p "Press enter to continue"