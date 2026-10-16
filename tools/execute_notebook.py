from pathlib import Path
import nbformat
from nbclient import NotebookClient

root=Path(__file__).parents[1]
nb=nbformat.read(root/'notebooks/retail_analysis.ipynb',as_version=4)
NotebookClient(nb,timeout=120,kernel_name='python3',resources={'metadata':{'path':str(root)}}).execute()
nbformat.write(nb,root/'reports/executed_analysis.ipynb')
print('Notebook executed successfully from a fresh kernel.')
