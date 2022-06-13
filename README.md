
# ForgeryDetector

ForgeryDetector is a Python library created for the paper "*Detecting Image Manipulation of Gel Electrophoresis Images in Scientific Publications*". The purpose of the library is to assist the user in finding possible copy-move manipulations in gel electrophoresis images (western, southern, and northern blots). There are however some limitations as described in the paper.

  

## Requirements

In order for the library to work properly, you must have Chrome downloaded and the accompanying [chromedriver](https://chromedriver.chromium.org/downloads). The path of these (when relevant) can be set when the relevant class is instantiated. it is a keyword argument and if nothing is given, it will be assumed that the user is on Windows and as such the default paths for Windows will be used. The rest of the dependencies can be installed via the requirements file by cd'ing via a terminal into the directory where the `requirements.txt` file is located (the main directory of the package) and then using the command:
```py
python -m pip install -r requirements.txt
```
This will install the following packages:
```
numpy		  |	v1.22.3
pymupdf 	  |	v1.19.5
scipy 		  |	v1.5.4
scikit-learn  |	v0.24.1
selenium	  |	v3.141.0
beatifulsoup4 |	v4.10.0
pdfkit		  |	v1.0.0
biopython	  |	v1.79
opencv-python | v4.5.5.64
python-dotenv |	v0.14.0
tensorflow	  |	v2.8.0
```

## Quick demonstration
There is an attached  `examples.py` file that shows the most important/useful functions of the library. You can either open it and run it via your favorite IDE (it has to be in the same directory as the package `ForgeryDetector`) or you can run it via the command:
```py
python -m example_steps.py
```
**Note**: If you choose to run it directly, make sure to first open the file and comment out some of the function calls as it would otherwise take a long time to go through them all and be difficult to distinguish which function gave which output.

There are also multiple test files, but these have to be placed in a folder outside ForgeryDetector in order to be able to use the package. Otherwise it won't recognize the package.