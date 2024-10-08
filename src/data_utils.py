# src/data_utils.py

import os
import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler


def load_data(config):
    data_file = config["data"]["data_file"]
    if not os.path.exists(data_file):
        logging.error(f"Data file {data_file} not found.")
        raise FileNotFoundError(f"Data file {data_file} not found.")
    else:
        logging.info(f"Loading data from {data_file}...")
        df = pd.read_csv(data_file)
    return df


def preprocess_data(df, config):

    # Check for necessary columns
    required_columns = config["data"]["required_columns"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        logging.error(f"Missing columns in the dataset: {missing_columns}")
        raise KeyError(f"Missing columns in the dataset: {missing_columns}")

    return df


def sample_data(df, config):
    sample_size = config["data"]["sample_size"]
    if sample_size:
        df = df.sample(sample_size, random_state=42).reset_index(drop=True)
        logging.info(f"Sampled {sample_size} entries from the dataset.")
    else:
        logging.info("Using all data in the dataset.")
    return df


def split_data(df):
    logging.info("Splitting data into training, validation, and testing sets...")
    # First, split into train + validation and test
    train_val_texts, test_texts, train_val_labels, test_labels = train_test_split(
        df["full_text"].tolist(), df["yo2"].tolist(), test_size=0.2, random_state=42
    )

    # Now, split the train + validation into actual train and validation sets
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        train_val_texts,
        train_val_labels,
        test_size=0.25,  # 25% of train + validation set for validation
        random_state=42,
    )

    return train_texts, val_texts, test_texts, train_labels, val_labels, test_labels
