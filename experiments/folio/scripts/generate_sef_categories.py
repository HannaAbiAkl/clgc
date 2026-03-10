import clgc
from clgc.__base import *
import pandas as pd

# load dataset
for split in ["train", "test", "valid"]:
    dataset_df = pd.read_csv(f"../data/folio_kr_gold_" + split + ".csv")

    # combine syllogism premises and conclusions to determine sef categories
    dataset_df["syllogism"] = dataset_df["premises-FOL"] + dataset_df["conclusion-FOL"]
    # generate sef cagegories
    dataset_df["sef"] = dataset_df["syllogism"].apply(lambda x: FOLSyllogism(x).categorize())
    print(dataset_df[["syllogism", "sef"]].head())
    # export dataset
    dataset_df.to_csv(f"../data/folio_kr_gold_" + split + "_sef.csv", index=False)
    print(f"Generated gold KR dataset with SEF categories for " + split + " split")