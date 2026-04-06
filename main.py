import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("default")

df = pd.read_csv("Womens Clothing E-Commerce Reviews.csv")
df = df.drop(columns=["Unnamed: 0"])
df = df.dropna(subset=["Division Name", "Department Name", "Class Name"])
df["Review Text"] = df["Review Text"].fillna("")
df["Title"] = df["Title"].fillna("")

df["review_length"] = df["Review Text"].str.len()
df["is_trend"] = (df["Department Name"] == "Trend").astype(int)
df["log_feedback"] = np.log1p(df["Positive Feedback Count"])
