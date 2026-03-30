#!/usr/bin/python3

import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

def count_labels(df_train, label_col="label"):
    if label_col not in df_train.columns:
        raise ValueError(f"Coluna '{label_col}' não encontrada no DataFrame")

    counts = df_train[label_col].value_counts().sort_values(ascending=False).to_dict()
    return counts
    
def train_test_split_stratify_index(y, test_size=0.38, random_state=42):
    y = np.asarray(y)

    if y.ndim != 1:
        raise ValueError("y must be a 1-dimensional array of labels")

    idx = np.arange(len(y))

    idx_train, idx_test, y_train, y_test = train_test_split(
        idx,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    return idx_train, idx_test, y_train, y_test

def generate_train_test_csv(
    input_csv,
    csv_train_file,
    csv_test_file,
    test_factor,
    column_name,
    random_state=42
):
    df = pd.read_csv(input_csv)

    # Seleção da coluna
    if len(column_name.strip()) == 0:
        column_name = df.columns[-1]
        y_np = df.iloc[:, -1].to_numpy()
    elif column_name in df.columns:
        y_np = df[column_name].to_numpy()
    else:
        raise ValueError(f"Column '{column_name}' not found")

    # Mapear labels para números
    d_set = list(set(y_np))
    d_lbl = list(range(len(d_set)))
    mydict = dict(zip(d_set, d_lbl))

    y = np.array([mydict[val] for val in y_np])

    # Split
    y_train_id, y_test_id, _, _ = train_test_split_stratify_index(
        y,
        test_size=test_factor / 100.0,
        random_state=random_state
    )

    df_train = df.iloc[np.uint32(y_train_id).tolist(), :]
    df_test = df.iloc[np.uint32(y_test_id).tolist(), :]

    # Salvar CSV
    df_train.to_csv(csv_train_file, index=False)
    df_test.to_csv(csv_test_file, index=False)

    # Contagem
    df_train_count = count_labels(df_train, label_col=column_name)
    df_test_count = count_labels(df_test, label_col=column_name)

    # Salvar JSON
    with open(csv_train_file + ".json", "w") as f:
        json.dump(df_train_count, f, indent=4)

    with open(csv_test_file + ".json", "w") as f:
        json.dump(df_test_count, f, indent=4)

    return True
