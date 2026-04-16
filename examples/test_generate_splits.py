import sys
sys.path.append('../')
from src.clgc.__base import *
import pandas as pd
from sklearn.model_selection import train_test_split


def test_generate_splits(format="kr", split="train"):
    # load dataset
    dataset_df = pd.read_csv(f"../data/pfolio_{format}_gold_{split}.csv")

    train, test = train_test_split(dataset_df, test_size=0.2, random_state=0, stratify=dataset_df[['Truth Values']])
    # check if stratificaton is good
    print("*** Train set size:",len(train["Truth Values"].values))  
    print("*** Train set unique Truth Values:",len(set(train["Truth Values"].values)))

    print("*** Test set size:",len(test["Truth Values"].values))  
    print("*** Test set unique Truth Values:",len(set(test["Truth Values"].values)))

    dev, val = train_test_split(train, test_size=0.4, random_state=0, stratify=train[['Truth Values']])
    # check if stratificaton is good
    print("*** Train set size:",len(dev["Truth Values"].values))  
    print("*** Train set unique Truth Values:",len(set(dev["Truth Values"].values)))

    print("*** Val set size:",len(val["Truth Values"].values))  
    print("*** Val set unique Truth Values:",len(set(val["Truth Values"].values)))

    dev.to_csv(f"../data/pfolio_{format}_train.csv", index=False)
    print(f"Generated gold {format} dataset for train split.")
    val.to_csv(f"../data/pfolio_{format}_val.csv", index=False)
    print(f"Generated gold {format} dataset for val split.")
    test.to_csv(f"../data/pfolio_{format}_test.csv", index=False)
    print(f"Generated gold {format} dataset for test split.")

if __name__ == "__main__":
    # generate gold splits
    for split in ["train"]:
        test_generate_splits(format='kr', split=split)