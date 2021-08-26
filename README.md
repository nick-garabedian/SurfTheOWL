# SurfTheOWL
## Requirements
+ Python 3
+ package owlready2
```pip install owlready2```
+ package django ```pip install django```

## How to strat SurfTheOWL
Just open the "start SurfTheOWL.py" file. 
This will open your Browser, and you can start surfing the OWL.
It also opens a little GUI whit which you can terminate all started subprocesses.(big red Button) 


## Surf another OWL 
replace the "```TriboDaterFAIR_v0.4.owl```" with a new file, in dir ```./SurfTheOWL/TriboDaterFAIR_v0.4.owl```.
Change the name of the to opened file in the script "```SurfTheOWL.py```", dir ```./SurfTheOWL/SurfTheOWL.py```


## Make a new Executable
if static files chanced, pull new static files in root staticfiles Folder by calling ````python manage.py collectstatic````

First install PyInstaller ```pip install pyinstaller```.
Then go into the main Project Folder and open a cmd Terminal.
Run the Command ``pyinstaller --clean --onedir SurfTheOWL/manage.py --collect-data owlready2 --collect-data django --add-data SurfTheOWL\SurfTheOWL\TriboDataFAIR_Ontology.owl;SurfTheOWL --add-data SurfTheOWL\SurfTheOWL\templates\SurfTheOWL.html;SurfTheOWL\templates --add-data SurfTheOWL\staticfiles\favicon.svg;staticfiles --add-data SurfTheOWL\staticfiles\SurfTheOWL_style.css;staticfiles --add-data SurfTheOWL\staticfiles\SurfTheOWL_JavaScript.js;staticfiles``

Now a new Folder ```dist``` appears in the main project Folder, in the child Folder you will find the executable. 
To run the executable you need it a Terminal and call the command ``mange.exe runserver 127.0.0.1:8000 --noreload``,
ore you write a .bat file to call the command and make it easy to use, like the existing .bat file. 
