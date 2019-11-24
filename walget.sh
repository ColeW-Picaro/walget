#!/bin/zsh
image="image.jpg"
rm $HOME/.cache/wal/schemes/*None_None*.json
python3 walget.py
wal -a 85 -i $image
rm $image
