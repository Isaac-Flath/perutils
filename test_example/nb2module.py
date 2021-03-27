#export
from nbdev.export import read_nb
from pathlib import Path
import os

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
  for i in range(len(nbs)):
    simple_export_one_nb(nbs[i],lib_path)

