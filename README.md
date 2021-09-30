# SurfTheOWL
## Simple use of SurfTheOWL 
1. Download the zip file ```SurfTheOWL_executable.zip```
2. Unzip the file for example via 7zip
3. Open the unzipped folder and double-click on ```SurfTheOWL.bat```
4. Now your Browser opens and SurfTheOWL is running 

>**Please note:** If you are used an older version of SurfTheOWL before, delete the cached data in your browser, because some new features need to be reloaded. An old cached stylesheet can course that some elements are not displayed as intended. To delete your cached data got to your browser settings and in the tab data you can delete the browser cache data.

### Surf another OWL
Replace the "```TriboDataFAIR_Ontology.owl```" in folder ```SurfTheOWL``` with a new Ontology.
>**Please note:** If you are defining new classes and instances the name of these should follow a good naming convention and be Python compatible, because if you are using code reserved characters the code will not run a throw an error.
>* Name can not start with a number
>* Name only contain A-Z, a-z, 0-9 
>* Name can not use special characters such as * .  -  +  / etc.
>* Name can not contain code reserved keywords like ```class``` ```for``` ```def``` ```is``` ```else``` ```try``` ```from``` etc.
>* Name should not contain a space ```Deionized Water``` => ```DeIonizedWater```

---
## Use SurfTheOWL as Python/Django Project 
### Requirements
+ Python 3
+ package owlready2
```pip install owlready2```
+ package django ```pip install django```
### Recommendation 
+ package Cython, speeds up Owlready2 ```pip install cython``` 
>**Please note:** Cython has to be installed before Owlready2 is installed 

### How to start SurfTheOWL
Just open the "start SurfTheOWL.py" file. 
This will open your Browser, and you can start surfing the OWL.
It also opens a little GUI whit which you can terminate all started subprocesses.(big red Button) 
>**Please note:** If you are used an older version of SurfTheOWL before, delete the cached data in your browser, because some new features need to be reloaded. An old cached stylesheet can course that some elements are not displayed as intended. To delete your cached data got to your browser settings an in the Tab Data you can delete the browser cache data.



### Surf another OWL 
replace the "```TriboDataFAIR_Ontology.owl```" with a new file, in dir ```./SurfTheOWL/TriboDaterFAIR_Ontology.owl```.
Change the name of the to opened file in the script "```SurfTheOWL.py```", dir ```./SurfTheOWL/SurfTheOWL.py```
>**Please note:** If you are defining new classes and instances the name of these should follow a good naming convention and be Python compatible, because if you are using code reserved characters the code will not run a throw an error.
>* Name can not start with a number
>* Name only contain A-Z, a-z, 0-9 
>* Name can not use special characters such as * .  -  +  / etc.
>* Name can not contain code reserved keywords like ```class``` ```for``` ```def``` ```is``` ```else``` ```try``` ```from``` etc.
>* Name should not contain a space ```Deionized Water``` => ```DeIonizedWater```

### Make a new Executable
If static files (html template, css, js, images, etc.) have chanced, pull new static files in root staticfiles Folder by calling ````python manage.py collectstatic````

First install PyInstaller ```pip install pyinstaller```.
Then go into the main Project Folder and open a cmd Terminal.
Run the Command ``pyinstaller --clean --onedir SurfTheOWL/manage.py --collect-data owlready2 --collect-data django --add-data SurfTheOWL\SurfTheOWL\TriboDataFAIR_Ontology.owl;SurfTheOWL --add-data SurfTheOWL\SurfTheOWL\templates\SurfTheOWL.html;SurfTheOWL\templates --add-data SurfTheOWL\staticfiles\favicon.svg;staticfiles --add-data SurfTheOWL\staticfiles\SurfTheOWL_style.css;staticfiles --add-data SurfTheOWL\staticfiles\SurfTheOWL_JavaScript.js;staticfiles``

Now a new Folder ```dist``` appears in the main project Folder, in the child Folder you will find the executable. 
To run the executable you need a Terminal and call the command ``manage.exe runserver 127.0.0.1:8000 --noreload``,
or you write a ```.bat``` file to call the command and make it easy to use, like the existing ```.bat``` file. 
