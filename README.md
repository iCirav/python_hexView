![Screenshot of the help interface](/assets/images/cli.png)

Default Colors:
```
python hexviewer.py -f example.bin
```

Custom color scheme:
```
python hexviewer.py -f example.bin --color-scheme "null=blue,repeat=green,pattern=yellow,nonprint=red,search=magenta"
```

With search and region limit:
```
python hexviewer.py -f example.bin --start 512 --length 256 --search DEADBEEF
```
