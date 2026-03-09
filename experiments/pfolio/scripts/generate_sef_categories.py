import clgc
from clgc.__base import *
import pandas as pd

# load dataset
dataset_df = pd.read_csv(f"../data/pfolio_kr_gold_train.csv")

# combine syllogism premises and conclusions to determine sef categories
dataset_df["syllogism"] = dataset_df["Premises - FOL"] + dataset_df["Conclusions - FOL"]
# generate sef cagegories
dataset_df["sef"] = dataset_df["syllogism"].apply(lambda x: FOLSyllogism(x).categorize())
print(dataset_df[["syllogism", "sef"]].head())
# export dataset
dataset_df.to_csv(f"../data/pfolio_kr_gold_train_sef.csv", index=False)
print(f"Generated gold KR dataset with SEF categories for train split")