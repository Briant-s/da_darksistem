import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('v2.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']
total = len(cells)

# Write all cells to a text file instead of stdout
with open('.gemini_scratch/v2_cells.txt', 'w', encoding='utf-8') as out:
    out.write(f"Total cells: {total}\n\n")
    for i, c in enumerate(cells):
        ct = c['cell_type']
        source = ''.join(c['source'])
        out.write(f"=== Cell {i} ({ct}) ===\n")
        out.write(source)
        out.write("\n\n")

print(f"Done. Total cells: {total}")
