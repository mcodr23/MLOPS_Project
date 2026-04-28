import json, sys, os
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')

nb = json.load(open(sys.argv[1], 'r', encoding='utf-8'))
for i, c in enumerate(nb['cells']):
    ct = c['cell_type']
    src = ''.join(c['source'])
    print(f"--- Cell {i} ({ct}) ---")
    print(src)
    print()
