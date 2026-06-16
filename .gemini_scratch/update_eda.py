import json

def main():
    with open('v2.ipynb', 'r', encoding='utf-8') as f:
        nb = json.load(f)
        
    cells = nb['cells']
    
    # Update Cell 25
    cells[25]['source'] = [
        "df_clean.describe().T\n"
    ]
    
    # Update Cell 26
    cells[26]['source'] = [
        "fig, axes = plt.subplots(len(CONTINUOUS_COLS), 2, figsize=(14, 4.5 * len(CONTINUOUS_COLS)))\n",
        "\n",
        "for i, col in enumerate(CONTINUOUS_COLS):\n",
        "    data = df_clean[col].dropna()\n",
        "\n",
        "    sns.histplot(data, kde=True, ax=axes[i, 0], color='steelblue')\n",
        "    axes[i, 0].set_title(f'{col} — Distribution', fontsize=11)\n",
        "    axes[i, 0].tick_params(axis='x', labelsize=9)\n",
        "\n",
        "    sns.boxplot(x=data, ax=axes[i, 1], color='lightcoral')\n",
        "    axes[i, 1].set_title(f'{col} — Box Plot', fontsize=11)\n",
        "    axes[i, 1].tick_params(axis='x', labelsize=9)\n",
        "\n",
        "plt.tight_layout(pad=2.0, h_pad=3.0)\n",
        "plt.savefig('continuous_columns.png', dpi=150, bbox_inches='tight')\n",
        "plt.show()\n"
    ]
    
    # Update Cell 27
    cells[27]['source'] = [
        "label_counts = df_clean[LABEL_COLS].sum().sort_values(ascending=False)\n",
        "\n",
        "plt.figure(figsize=(9, 5))\n",
        "ax = sns.barplot(x=label_counts.values, y=label_counts.index, palette='viridis', hue=label_counts.index, legend=False)\n",
        "ax.set_title('Disease Label Distribution (Positive Cases)', fontsize=12)\n",
        "ax.set_xlabel('Count', fontsize=10)\n",
        "ax.set_ylabel('')\n",
        "ax.tick_params(axis='y', labelsize=9)\n",
        "\n",
        "for i, v in enumerate(label_counts.values):\n",
        "    ax.text(v + 1, i, str(int(v)), va='center', fontsize=9)\n",
        "\n",
        "plt.tight_layout()\n",
        "plt.savefig('label_distribution.png', dpi=150, bbox_inches='tight')\n",
        "plt.show()\n"
    ]
    
    # Update Cell 28
    cells[28]['source'] = [
        "categorical = [\n",
        "    'Gender' ,'Type of fever', 'Health Center', 'Fever 48 hrs', 'Fever in the last 7 days'\n",
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
    
    # Update Cell 29
    cells[29]['source'] = [
        "def categorical_distribution(data, catCols):\n",
        "    slots = len(categorical)\n",
        "    rows = -(-slots//3)\n",
        "    plt.figure(figsize=(15, rows * 3))\n",
        "    for i, col in enumerate(catCols, 1):\n",
        "        plt.subplot(rows, 3, i)\n",
        "        counts = data[col].value_counts()\n",
        "        plt.bar(counts.index, counts.values)\n",
        "        plt.title(col)\n",
        "    plt.tight_layout()\n",
        "    plt.show()\n",
        "\n",
        "categorical_distribution(df_clean, categorical)\n"
    ]
    
    # Update Cell 30
    cells[30]['source'] = [
        "def positive_count(series):\n",
        "    clean_series = series.astype(str).str.strip().str.lower()\n",
        "    return clean_series.isin(['yes', '1', 'true']).sum()\n",
        "\n",
        "symptom_counts = pd.Series(\n",
        "    {col: positive_count(df_clean[col]) for col in symptom_cols}\n",
        ").sort_values(ascending=False)\n",
        "\n",
        "top10 = symptom_counts.head(10)\n",
        "\n",
        "plt.figure(figsize=(9, 6))\n",
        "plt.barh(top10.index[::-1], top10.values[::-1], color='steelblue')\n",
        "plt.title('Top 10 Most Common Symptoms (YES count)', fontsize=12)\n",
        "plt.xlabel('Count')\n",
        "plt.tight_layout()\n",
        "plt.show()\n"
    ]
    
    with open('v2.ipynb', 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

if __name__ == '__main__':
    main()
