import sys
sys.path.append('../../../')
from src.clgc.__base import *
import pandas as pd

# generate combined train KR dataset
def test_generate_minifol_dataset(dataset="folio", split="train"):
    if split not in ["train", "test", "val"]:
        raise ValueError("Invalid split name. Must be one of 'train', 'test', or 'valid'.")
    else:
        # init base notations
        dataset_df = pd.read_csv(f"../../../experiments/{dataset}/data/{dataset}_{split}.csv")
        # generate and concat all notations
        gold_split_df = dataset_df
        gold_split_df['Premises - MINIFOL'] = dataset_df['Premises - FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism.fol_to_minifol(FOLSyllogism(x).syllogism))
        print("*** Generated Premises - MINIFOL ***")
        gold_split_df['Conclusions - MINIFOL'] = dataset_df['Conclusions - FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism.fol_to_minifol(FOLSyllogism(x).syllogism))
        print("*** Generated Conclusions - MINIFOL ***")
        gold_split_df['Premises - MINIFOL3'] = dataset_df['Premises - FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism.fol_to_minifol3(FOLSyllogism(x).syllogism))
        print("*** Generated Premises - MINIFOL3 ***")
        gold_split_df['Conclusions - MINIFOL3'] = dataset_df['Conclusions - FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism.fol_to_minifol3(FOLSyllogism(x).syllogism))
        print("*** Generated Conclusions - MINIFOL3 ***")
        gold_split_df['Premises - MINIFOL4'] = dataset_df['Premises - FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism.fol_to_minifol4(FOLSyllogism(x).syllogism))
        print("*** Generated Premises - MINIFOL4 ***")
        gold_split_df['Conclusions - MINIFOL4'] = dataset_df['Conclusions - FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism.fol_to_minifol4(FOLSyllogism(x).syllogism))
        gold_split_df.to_csv(f"../../../experiments/{dataset}/data/{dataset}_{split}.csv", index=False)
        print(f"Generated gold {dataset} dataset for {split} split.")

if __name__ == "__main__":
    # generate gold splits for pfolio dataset
    for dataset in ["pfolio"]:
        for split in ["train", "test", "val"]:
            print(f"Generating gold {dataset} dataset for {split} split...")
            test_generate_minifol_dataset(dataset=dataset, split=split)