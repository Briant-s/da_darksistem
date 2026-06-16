import json
import sys

def main():
    with open('v2.ipynb', 'r', encoding='utf-8') as f:
        nb = json.load(f)
        
    cells = nb['cells']
    
    # 1. Update Cell 8
    cells[8]['source'] = [
        "target_cols = ['Malaria', 'Diagnosed Dengue', 'Other']\n",
        "\n",
        "num_issues = ['Hematocrit', 'White blood cell count', 'Platelet count', 'Neutrophils', 'Age']\n",
        "\n",
        "redudant_cols = [\n",
        "    'UUID', 'Diagnosed diseases', 'Other diseases presented by patient',\n",
        "    'Diagnosed Chikungunya', 'Diagnosed Zika', 'Diagnosed Option 8',\n",
        "    'Mua circumference', 'Capillary refill time', 'Arterial blood pressure',\n",
        "    'Lymphocytes', 'Health Center', 'Conjunctivitis', 'Facial flushing', 'Profuse sweating',\n",
        "    'Rheumatic disease', 'Autoimmune disease', 'Allergies', 'Cancer', 'Leucopenia', \n",
        "]\n",
        "\n",
        "disease_to_target = {\n",
        "    'Malaria':  'Malaria',\n",
        "    'Dengue':   'Diagnosed Dengue',\n",
        "    'Other':    'Other'\n",
        "}"
    ]
    
    # 2. Update Cell 10 to include the merge BEFORE the backfill
    cells[10]['source'] = [
        "# 2. Parsing Diagnosed Diseasies to backfill targets\n",
        "def parse_diagnosed_diseases(text):\n",
        "    if pd.isna(text) or str(text).strip() == '':\n",
        "        return {col: np.nan for col in target_cols}\n",
        "    return {\n",
        "        'Malaria':                  1 if 'Paludisme' in text or 'Malaria' in text else 0,\n",
        "        'Diagnosed Dengue':         1 if 'Dengue' in text else 0,\n",
        "        'Other':                    1 if ('jaune' in text or 'yellow' in text.lower() \n",
        "                                          or 'Typho' in text \n",
        "                                          or 'Autres' in text or 'Others' in text) else 0\n",
        "    }\n",
        "\n",
        "# Merge Yellow fever, Typhoid, Other diagnosed diseases -> Other FIRST\n",
        "df_temp['Other'] = (\n",
        "    df_temp[['Yellow fever', 'Typhoid fever', 'Other diagnosed diseases']]\n",
        "    .max(axis=1)  # 1 jika salah satu = 1\n",
        ")\n",
        "df_temp.drop(columns=['Yellow fever', 'Typhoid fever', 'Other diagnosed diseases'], inplace=True)\n",
        "\n",
        "parsed = pd.DataFrame(\n",
        "    df_temp['Diagnosed diseases'].apply(parse_diagnosed_diseases).to_list(),\n",
        "    index=df_temp.index\n",
        ")\n",
        "\n",
        "for col in target_cols:\n",
        "    mask = df_temp[col].isna()\n",
        "    df_temp.loc[mask, col] = parsed.loc[mask, col]\n"
    ]
    
    # 3. Update Cell 19 (make_label)
    cells[19]['source'] = [
        "def make_label(row):\n",
        "    labels = []\n",
        "    if row['Malaria'] == 1:          labels.append('Malaria')\n",
        "    if row['Diagnosed Dengue'] == 1: labels.append('Dengue')\n",
        "    if row['Other'] == 1:            labels.append('Other')\n",
        "    return ' + '.join(labels) if labels else 'Unknown'"
    ]
    
    # 4. Update Cell 24 (LABEL_COLS)
    cells[24]['source'] = [
        "CONTINUOUS_COLS = ['Age', 'Weight', 'Axillary temperature', 'Respiratory rate',\n",
        "                    'Pulse rate', 'Hematocrit', 'White blood cell count',\n",
        "                    'Platelet count', 'Neutrophils', 'Elevated Creatinine']\n",
        "\n",
        "LABEL_COLS = ['Malaria', 'Diagnosed Dengue', 'Other']"
    ]
    
    # 5. Update Cell 34 (TARGETS)
    cells[34]['source'] = [
        "MIN_N = 15          \n",
        "FDR_ALPHA = 0.05\n",
        "TARGETS = ['Malaria', 'Diagnosed Dengue', 'Other']\n",
        "LEAKAGE_MAP = {'Diagnosed Dengue': ['Dengue']}"
    ]
    
    # 6. Update Cell 44 (Imputation logic)
    cells[44]['source'] = [
        "# 3. Global median imputation for binary columns (no label leakage)\n",
        "global_medians = X_train[binary_cols].median()\n",
        "\n",
        "for split in [X_train, X_val, X_test]:\n",
        "    for col in binary_cols:\n",
        "        split[col] = split[col].fillna(global_medians[col])\n"
    ]
    
    # 7. Update Cell 49 (Winsorize & Log transform)
    cells[49]['source'] = [
        "# Winsorizing + Log Transform\n",
        "clip_caps = {}\n",
        "log_cols = ['Elevated Creatinine', 'Respiratory rate', \n",
        "            'White blood cell count', 'Platelet count']\n",
        "\n",
        "for col in num_cols:\n",
        "    cap = X_train[col].quantile(0.99)\n",
        "    clip_caps[col] = cap\n",
        "    for split in [X_train, X_val, X_test]:\n",
        "        split[col] = split[col].clip(upper=cap)\n",
        "\n",
        "for col in log_cols:\n",
        "    for split in [X_train, X_val, X_test]:\n",
        "        split[col] = np.log1p(split[col])\n"
    ]
    
    # 8. Update Cell 50 (Scaling)
    cells[50]['source'] = [
        "# 6. Scale (fit only done on train)\n",
        "scaler = RobustScaler()\n",
        "scaler.fit(X_train[num_cols])\n",
        "\n",
        "for split in [X_train, X_val, X_test]:\n",
        "    split[num_cols] = scaler.transform(split[num_cols])\n"
    ]
    
    # 9. Update Cell 52 and 54 (Feature Selection)
    cells[52]['source'] = [
        "# (Random Forest feature selection removed to avoid double selection bias)\n"
    ]
    
    cells[54]['source'] = [
        "targets = target_cols  # ['Malaria', 'Diagnosed Dengue', 'Other']\n",
        "all_selected_features = set()\n",
        "\n",
        "for target in targets:\n",
        "    # Calculate MI for this specific disease\n",
        "    mi_scores = mutual_info_classif(X_train, y_train[target], discrete_features=True)\n",
        "    mi_series = pd.Series(mi_scores, index=X_train.columns).sort_values(ascending=False)\n",
        "    \n",
        "    # Grab the top 15 features for this disease and add them to our master set\n",
        "    top_15 = mi_series.head(15).index.tolist()\n",
        "    all_selected_features.update(top_15)\n",
        "\n",
        "# Convert the set back to a list (sets automatically remove duplicates)\n",
        "final_features = list(all_selected_features)\n",
        "\n",
        "print(f'Total unique features selected across all 3 diseases: {len(final_features)}')\n",
        "\n",
        "# Filter datasets\n",
        "X_train = X_train[final_features]\n",
        "X_val = X_val[final_features]\n",
        "X_test = X_test[final_features]\n"
    ]
    
    # 10. Update Cell 56 (import iterstrat and copy)
    cells[56]['source'] = [
        "from iterstrat.ml_stratifiers import MultilabelStratifiedKFold\n",
        "import copy\n",
        "import torch\n",
        "import torch.nn as nn\n",
        "import torch.optim as optim\n",
        "from torch.utils.data import DataLoader, TensorDataset\n",
        "from sklearn.metrics import classification_report, roc_auc_score, f1_score\n",
        "import pandas as pd\n",
        "import numpy as np\n"
    ]
    
    # 11. Update Cell 58 (K-Fold & tuning leakage)
    cells[58]['source'] = [
        "# ==========================================\n",
        "# 4. Persiapan Stratified K-Fold\n",
        "# ==========================================\n",
        "k_folds = 5\n",
        "mlskf = MultilabelStratifiedKFold(n_splits=k_folds, shuffle=True, random_state=42)\n",
        "\n",
        "print('\\nMemulai Multilabel Stratified 5-Fold Cross-Validation...')\n",
        "\n",
        "test_probs_ensemble = np.zeros_like(y_test_tensor.numpy(), dtype=float)\n",
        "val_probs_ensemble = np.zeros_like(y_val_tensor.numpy(), dtype=float)\n",
        "\n",
        "# ==========================================\n",
        "# 5. K-Fold Training Loop\n",
        "# ==========================================\n",
        "for fold, (train_idx, val_idx) in enumerate(mlskf.split(X_train_tensor, y_train_tensor)):\n",
        "    print(f'\\n{\"=\"*20} FOLD {fold + 1} {\"=\"*20}')\n",
        "    \n",
        "    X_fold_train = X_train_tensor[train_idx]\n",
        "    y_fold_train = y_train_tensor[train_idx]\n",
        "    X_fold_val = X_train_tensor[val_idx]\n",
        "    y_fold_val = y_train_tensor[val_idx]\n",
        "    \n",
        "    fold_train_dataset = TensorDataset(X_fold_train, y_fold_train)\n",
        "    fold_train_loader = DataLoader(fold_train_dataset, batch_size=16, shuffle=True)\n",
        "    \n",
        "    pos_weights = []\n",
        "    for i in range(len(target_cols)):\n",
        "        num_positives = y_fold_train[:, i].sum().item()\n",
        "        num_negatives = len(y_fold_train) - num_positives\n",
        "        weight = num_negatives / (num_positives + 1e-5) \n",
        "        pos_weights.append(weight)\n",
        "    pos_weight_tensor = torch.FloatTensor(pos_weights)\n",
        "    \n",
        "    model = MultiLabelNN(X_train_tensor.shape[1], len(target_cols))\n",
        "    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight_tensor)\n",
        "    optimizer = optim.Adam(model.parameters(), lr=0.001)\n",
        "    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=4)\n",
        "    \n",
        "    best_val_loss = float('inf')\n",
        "    epochs_no_improve = 0\n",
        "    patience_limit = 12\n",
        "    epochs = 50\n",
        "    \n",
        "    best_model_state = None\n",
        "    \n",
        "    for epoch in range(epochs):\n",
        "        model.train()\n",
        "        total_train_loss = 0\n",
        "        \n",
        "        for batch_X, batch_y in fold_train_loader:\n",
        "            optimizer.zero_grad()\n",
        "            outputs = model(batch_X)\n",
        "            loss = criterion(outputs, batch_y)\n",
        "            loss.backward()\n",
        "            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)\n",
        "            optimizer.step()\n",
        "            total_train_loss += loss.item()\n",
        "            \n",
        "        model.eval()\n",
        "        with torch.no_grad():\n",
        "            val_logits = model(X_fold_val)\n",
        "            val_loss = criterion(val_logits, y_fold_val).item()\n",
        "            \n",
        "        scheduler.step(val_loss)\n",
        "        \n",
        "        if val_loss < best_val_loss:\n",
        "            best_val_loss = val_loss\n",
        "            epochs_no_improve = 0\n",
        "            best_model_state = copy.deepcopy(model.state_dict())\n",
        "        else:\n",
        "            epochs_no_improve += 1\n",
        "            \n",
        "        if epochs_no_improve >= patience_limit:\n",
        "            print(f'  -> Early stopping aktif di epoch {epoch+1} (Best Val Loss: {best_val_loss:.4f})')\n",
        "            break\n",
        "\n",
        "    if best_model_state is not None:\n",
        "        model.load_state_dict(best_model_state)\n",
        "    \n",
        "    model.eval()\n",
        "    with torch.no_grad():\n",
        "        # Ensemble for test set\n",
        "        test_logits = model(X_test_tensor)\n",
        "        test_probs_ensemble += torch.sigmoid(test_logits).numpy()\n",
        "        # Ensemble for val set\n",
        "        val_logits_fold = model(X_val_tensor)\n",
        "        val_probs_ensemble += torch.sigmoid(val_logits_fold).numpy()\n",
        "\n",
        "# ==========================================\n",
        "# 6. Ensemble Evaluation (Rata-rata 5 Fold)\n",
        "# ==========================================\n",
        "final_test_probs = test_probs_ensemble / k_folds\n",
        "final_val_probs = val_probs_ensemble / k_folds\n",
        "\n",
        "print('\\n' + '='*50)\n",
        "print('MENCARI THRESHOLD OPTIMAL (TUNING PADA VALIDATION SET)')\n",
        "print('='*50)\n",
        "\n",
        "best_thresholds = {}\n",
        "for i, col in enumerate(target_cols):\n",
        "    best_thresh = 0.5\n",
        "    best_f1 = 0\n",
        "    \n",
        "    for thresh in np.arange(0.05, 0.95, 0.01):\n",
        "        preds = (final_val_probs[:, i] > thresh).astype(int)\n",
        "        score = f1_score(y_val_tensor.numpy()[:, i], preds, zero_division=0)\n",
        "        \n",
        "        if score > best_f1:\n",
        "            best_f1 = score\n",
        "            best_thresh = thresh\n",
        "            \n",
        "    if best_f1 == 0:\n",
        "        best_thresh = 0.3\n",
        "        \n",
        "    best_thresholds[col] = best_thresh\n",
        "    print(f'{col:<26} -> Final Optimal Thresh: {best_thresh:.2f} | F1-Val: {best_f1:.4f}')\n",
        "\n",
        "print('\\n' + '='*50)\n",
        "print('FINAL ENSEMBLE CLASSIFICATION REPORT (ON TEST SET)')\n",
        "print('='*50)\n",
        "\n",
        "test_preds_tuned = np.zeros_like(final_test_probs, dtype=int)\n",
        "for i, col in enumerate(target_cols):\n",
        "    test_preds_tuned[:, i] = (final_test_probs[:, i] > best_thresholds[col]).astype(int)\n",
        "\n",
        "print(classification_report(y_test_tensor.numpy(), test_preds_tuned, target_names=target_cols, zero_division=0))\n",
        "\n",
        "print('='*50)\n",
        "print('FINAL ENSEMBLE ROC-AUC SCORE')\n",
        "print('='*50)\n",
        "for i, col in enumerate(target_cols):\n",
        "    try:\n",
        "        auc = roc_auc_score(y_test_tensor.numpy()[:, i], final_test_probs[:, i])\n",
        "        print(f'{col:<30} : {auc:.4f}')\n",
        "    except ValueError:\n",
        "        print(f'{col:<30} : Error (Data test kurang variasi)')\n"
    ]
    
    with open('v2.ipynb', 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

if __name__ == '__main__':
    main()
