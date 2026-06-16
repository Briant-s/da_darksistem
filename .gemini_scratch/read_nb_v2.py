import json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open(r'c:\Dokumen\Kuliah\Lomba\da_darksistem\v2.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    ct = cell['cell_type']
    src = ''.join(cell['source'])
    if len(src) > 3000:
        src = src[:3000] + '\n... [TRUNCATED]'
    print(f'=== Cell {i} ({ct}) ===')
    print(src)
    print()
