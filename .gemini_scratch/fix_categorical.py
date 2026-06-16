import json

with open('v2.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

cells[28]['source'] = [
    "categorical = [\n",
    "    'Gender', 'Type of fever', 'Fever 48 hrs', 'Fever in the last 7 days'\n",
    "]\n",
    "\n",
    "excluded = ['Gender', 'Age', 'Weight', 'Temperature', 'Type of fever',\n",
    "           'Axillary temperature', 'Respiratory rate', 'Pulse rate',\n",
    "           'Hematocrit', 'White blood cell count', 'Platelet count',\n",
    "           'Neutrophils', 'Elevated Creatinine',\n",
    "           'Malaria', 'Diagnosed Dengue', 'Other', 'Mua circumference']\n",
    "\n",
    "symptom_cols = [c for c in df_clean.columns if c not in excluded]\n"
]

cells[29]['source'] = [
    "def categorical_distribution(data, catCols):\n",
    "    label_map = {\n",
    "        'Gender': {1: 'Male', 0: 'Female'},\n",
    "        'Type of fever': {1: 'Recurrent', 0: 'Intermittent'},\n",
    "    }\n",
    "    slots = len(catCols)\n",
    "    rows = -(-slots//3)\n",
    "    plt.figure(figsize=(15, rows * 3))\n",
    "    for i, col in enumerate(catCols, 1):\n",
    "        plt.subplot(rows, 3, i)\n",
    "        series = data[col].copy()\n",
    "        if col in label_map:\n",
    "            series = series.map(label_map[col])\n",
    "        else:\n",
    "            series = series.map({1: 'YES', 0: 'NO'})\n",
    "        counts = series.value_counts()\n",
    "        plt.bar(counts.index, counts.values)\n",
    "        plt.title(col)\n",
    "    plt.tight_layout()\n",
    "    plt.show()\n",
    "\n",
    "categorical_distribution(df_clean, categorical)\n"
]

with open('v2.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
