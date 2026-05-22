"""
Data loading and preparation module.
Handles loading and transforming the women's clothing reviews dataset.
"""

import pandas as pd
import numpy as np

def load_and_prepare_data():
    """
    Load and prepare the women's clothing reviews dataset.
    
    Returns:
        pd.DataFrame: Processed dataframe with additional feature engineering
    """
    # Load data
    df = pd.read_csv("data/Womens Clothing E-Commerce Reviews.csv")
    
    # Clean data
    df = df.drop(columns=["Unnamed: 0"], errors='ignore')
    df = df.dropna(subset=["Division Name", "Department Name", "Class Name"])
    df["Review Text"] = df["Review Text"].fillna("")
    df["Title"] = df["Title"].fillna("")
    
    # Feature engineering
    df["review_length"] = df["Review Text"].str.len()
    df["is_trend"] = (df["Department Name"] == "Trend").astype(int)
    df["age_group"] = pd.cut(
        df["Age"],
        bins=[0, 25, 35, 45, 55, 100],
        labels=["<25", "25-35", "35-45", "45-55", "55+"]
    )
    df["log_feedback"] = np.log1p(df["Positive Feedback Count"])
    
    return df
