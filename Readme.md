# Lauretta Test Image Puzzle Solver

Attached is a toy puzzle solver written in Python. It analyzes a collection of images from a single folder. It will then search each image for a collection of colored markers to determine which order the puzzled together image should take. 

Thank you for your time looking at my application

---

## Dependencies

This script only relies on two external modules. 
- OpenCV
- NumPy

Also used is Jupyter Notebook. But it is an optional install. 
## Install

```python
pip install -r requirements.txt

# If you optionally prefer some jupyter modules use the below:
pip install -r jupyter_requirements.txt
```
## Run

To run, use the Jupyter Notebook. You may also run in your terminal using:
```console
python puzzle.py <Image_Folder_Directory>
```


The program will create a `Build\` Directory to place the composite image into.
