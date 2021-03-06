#export
import os, json, copy
from pathlib import Path
from nbdev.export import read_nb

#export
def get_py_files(path): 
    '''Get all py files in a direcotry'''
    return [f for f in os.listdir(path) if f[-3:] == '.py']

#export
def get_cells_one_nb(path,file_name):
    '''For py file in path get a return list of strings
    Each item in list will corrospond to the contents of a cell in a notebook'''

    file = open(path/file_name)
    Lines = file.readlines()

    split_flag = True
    cells = [[]]
    i = 0
    
    for j,line in enumerate(Lines):
        split_criteria = line.startswith(('import ','from ','def ','class ','@',"if __name__ == '__main__':"))
        
        if split_flag != split_criteria:  cells[i].append(line)

        if split_criteria and split_flag:
            i+=1
            cells.append([])
            cells[i].append('#export\n')
            cells[i].append(line)
            split_flag = False

        if not split_flag and not split_criteria: split_flag = True    

    return cells

#export
def write_code_cell(code):
    '''take a piece of code and write it to a code cell
    '''
    out = {"cell_type": "code","execution_count": 0,"metadata": {},"outputs": [],"source": []}
    out["source"] = code
    return out  

#export
def py_to_nb(py_path,nb_path):
    '''Write jupyter notebooks based on py files in py_path'''
    if not os.path.exists(nb_path): os.makedirs(nb_path)
      
    files = get_py_files(py_path)
    
    nb = {"cells": [],"metadata": {},"nbformat": 4, "nbformat_minor": 4}
    for i,file in enumerate(files): 
        out_file = f'{file[:-2]}ipynb'; print(f'writing {out_file}') # change extension
        cells = get_cells_one_nb(py_path,files[i]) # get cells that should be written
        for cell in cells: nb["cells"].append(write_code_cell(cell)) # add cells to dict
        with open(nb_path/out_file, 'w') as file: file.write(json.dumps(nb)) # write dict to json

#export
def get_module_text(notebook_path):
    '''Read ipynb file and get all code from code cells with #export or # export at the beginning'''
    nb = read_nb(notebook_path)
    module = ''
    for cell in nb['cells']: 
        if cell['cell_type']=='code':
            if cell['source'].startswith('#export') or cell['source'].startswith('# export'):
                module = module + cell['source'] + '\n\n'
    return module

#export
def write_module_text(module_text,notebook_name,lib_path=Path('./src')):
    '''Write module_text to lib_path/notebook_name as .py file'''
    if not os.path.exists(lib_path): os.makedirs(lib_path)
    module_name = (str(notebook_name)[:-5] + 'py').lstrip('0123456789.- _').replace('-','_')
    f = open(lib_path/module_name, "w")
    f.write(module_text)
    f.close()
    print(f'Converted {lib_path/module_name}')

#export
def clear_all_modules(lib_path=Path('./src')):
    '''Clear all .py files from lib_path to reset your .py exported files'''
    if not os.path.exists(lib_path): os.makedirs(lib_path)
    filelist = [ f for f in os.listdir(lib_path) if f.endswith('.py')]
    for f in filelist: os.remove(os.path.join(lib_path, f))
    print('========= Modules Cleared ==========')

#export
def simple_export_one_nb(nb_path,lib_path = Path('./src')):
    '''clear_all_modules in lib_path
    for each notebook in nbs_path get_module_text and write_module_text to lib_path 
    All .py files in lib_path will be removed and replaced
    '''
    module_text = get_module_text(nb_path)
    if module_text == '': print(f'Nothing to Convert {lib_path/nb_path}')
    else: write_module_text(module_text,nb_path,lib_path)

#export
def simple_export_all_nb(nbs_path = Path('.'),lib_path = Path('./src'),clear=False):
    '''clear_all_modules in lib_path if clear=True
     for each notebook in nbs_path get_module_text and write_module_text to lib_path 
     All .py files in lib_path will be removed and replaced
    '''
    nbs = [nbs_path/n for n in  os.listdir(nbs_path) if n.endswith('.ipynb')]
    if clear: clear_all_modules(lib_path)
    for i in range(len(nbs)): simple_export_one_nb(nbs[i],lib_path)

