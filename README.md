# Personal Utils (perutils)
> Notebook -> module conversion with #export flags and nothing else


**Purpose:**  The purpose and main use of this module is for adhoc projects where a full blown nbdev project is not necessary 

**Example Scenario** 

Imagine you are working on a kaggle competition. You may not want the full nbdev.  For example, you don't need separate documentation from your notebooks and you're never going to release it to pip or conda.  This module simplifies the process so you just run one command and it creates .py files from your notebooks.  Maybe you are doing an ensemble and to export the dataloaders from a notebook so you can import them into seperate notebooks for your seperate models, or maybe you have a seperate use case.

That's what this module does.  it's just the #export flags from nbdev and exporting to a module folder with no setup (ie settings.ini, \_\_nbdev.py, etc.) for fast minimal use

## Install

`pip install perutils`

## How to use

### Shelve Experiment Tracking

This module is designed to assist me in tracking experiments when I am working on data science and machine learning tasks, though is flexible enough to track most things.  This allows for easy tracking and plotting of many different types of information and datatypes without requiring a consistent schema so you can add new things without adjusting your dataframe or table.

General access to a shelve db can be reached in one of two ways and behaves similar to a dictionary.

```python
with shelve.open('test.shelve') as d: 
    print(d['exp'])

d = shelve.open('test.shelve')
print(d['exp']
d.close()
```

This module assumes a certain structure.  If we assume: `d = shelve.open('test.shelve')`

```python
assert type(d[key]) == list
assert type(d[key][0]) == dict
```

Additionally:
+ keys in an experiment (`d['exp'][0][key]` must be strings but the values can be anything that can be pickled
+ Plotting functions assumes the value you want to plot (ie `d['exp][0]['batch_loss']` is list like and the name (for the legend) is a string

#### Create and Add Data

The process is:
1. Create a dict with all the information
2. Append dict to database

This will create `filename` if it does not exist

```python
append(filename,new_dict)
```
{% include note.html content='You can write individual elements at a time as well just like you would in a normal dictionary if that is preferred.' %}

#### Delete

`-1` can be replaced with any index location.

```python
delete(filename,-1)
```

#### What keys are available?

```python
print_keys(filename)
```

#### What were the results?

```python
el,ea,bl = get_stats(filename,-1,['epoch_loss','epoch_accuracy','batch_loss'],display=True)
```

#### Find the experiment with the best results.

```python
print_best(filename,'epoch_loss',best='min')
print_best(filename,'epoch_accuracy',best='max')
```

#### Graph some stats and compare results

```python
graph_stats(filename,['batch_loss','epoch_accuracy'],idxs=[-1,-2,-3])
```

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

### kaggle dataset

#### Uploading Libraries

```python
if __name__ == '__main__':
    libraries = ['huggingface','timm','torch','torchvision','opencv-python','albumentations','fastcore']

    for library in libraries: 
        print(f'starting {library}')
        dataset_path = Path(library)
        print("downloading dataset...")
        download_dataset(dataset_path,f'isaacflath/library{library}',f'library{library}',content=False,unzip=True)
        print("adding library...")
        add_library_to_dataset(library,dataset_path)
        print("updating dataset...")
        update_datset(dataset_path,"UpdateLibrary")

        print('+'*30)
```

#### Custom dataset (ie model weights)

```python
dataset_path = Path(library)
dataset_name = testdataset
download_dataset(dataset_path,f'isaacflath/{dataset_name}',f'{dataset_name}',content=False,unzip=True)
# add files (ie model weights to folder
update_datset(dataset_path,"UpdateLibrary")
```
