# Personal Utils (perutils)
> Notebook -> module conversion with #export flags and nothing else


**Purpose:**  The purpose and main use of this module is for adhoc projects where a full blown nbdev project is not necessary 

**Example Scenario** 

Imagine you are working on a kaggle competition. You may not want the full nbdev.  For example, you don't need separate documentation from your notebooks and you're never going to release it to pip or conda.  This module simplifies the process so you just run one command and it creates .py files from your notebooks.  Maybe you are doing an ensemble and to export the dataloaders from a notebook so you can import them into seperate notebooks for your seperate models, or maybe you have a seperate use case.

That's what this module does.  it's just the #export flags from nbdev and exporting to a module folder with no setup (ie settings.ini, \_\_nbdev.py, etc.) for fast minimal use

## Install

`pip install git+https://github.com/isaac-flath/perutils`

## How to use

### nb -> py

#### Full Directory Conversion

In python run the `simple_export_all_nb` function.  This will:
+ Look through all your notebooks in the directory (nbs_path) for any code cells starting with `#export` or `# export`
+ If any export code cells exist, it will take all the code and put it in a .py file located in `lib_path`
+ The .py module will be named the same as the notebook.  There is no option to specify a seperate .py file name from your notebook name

**Any .py files in your lib_path will be removed and replaced.  Do not set lib_path to a folder where you are storing other .py files.  I recommend lib_path being it's own folder only for these auto-generated modules**

```python
simple_export_all_nb(nbs_path=Path('.'), lib_path=Path('test_example'))```

#### Single Notebook Conversion

In python run the `simple_export_one_nb` function.  This will:

+ Look through the specified notebook (nb_path) for any code cells starting with `#export` or `# export`
+ If any export code cells exist, it will take all the code and put it in a .py file located in `lib_path`
+ The .py module will be named the same as the notebook.  There is no option to specify a seperate .py file name from your notebook name


```python
simple_export_one_nb(nb_path=Path('./00_core.ipynb'), lib_path=Path('test_example'))```

### py -> nb

#### Full Directory Conversion

In python run the `py_to_nb` function.  This will:
+ Look through all your py files in the `py_path`
+ Find the simple breaking points in each file (ie when new functions or classes are defined
+ Create jupyter notebooks in `nb_path` and put code in seperate cells (with `#export` flag)

**This will overwrite notebooks in the `nb_path` if they have the same name other than extension as a python module**

```python
py_to_nb(py_path=Path('./src/'),nb_pth=Path('.')```
