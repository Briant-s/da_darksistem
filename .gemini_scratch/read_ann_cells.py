import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open(r'c:\Dokumen\Kuliah\Lomba\da_darksistem\v1.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i in [67, 70, 71]:
    cell = nb['cells'][i]
    ct = cell['cell_type']
    src = ''.join(cell['source'])
    print(f'=== Cell {i} ({ct}) ===')
    print(src)
    print()
