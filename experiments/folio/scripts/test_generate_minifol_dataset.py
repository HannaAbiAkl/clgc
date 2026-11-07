import sys
sys.path.append('../../../')
from src.clgc.__base import *
import pandas as pd

# generate combined train KR dataset
def test_generate_minifol_dataset(dataset="folio", split="train"):
    if split not in ["train", "test", "valid"]:
        raise ValueError("Invalid split name. Must be one of 'train', 'test', or 'valid'.")
    else:
        # init base notations
        dataset_df = pd.read_csv(f"../../../experiments/{dataset}/data/{dataset}_kr_gold_{split}_sef.csv")
        # generate and concat all notations
        gold_split_df = dataset_df
        gold_split_df['premises-MINIFOL'] = dataset_df['premises-FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism.fol_to_minifol(FOLSyllogism(x).syllogism))
        print("*** Generated Premises - MINIFOL ***")
        gold_split_df['conclusion-MINIFOL'] = dataset_df['conclusion-FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism.fol_to_minifol(FOLSyllogism(x).syllogism))
        print("*** Generated Conclusions - MINIFOL ***")
        gold_split_df['premises-MINIFOL3'] = dataset_df['premises-FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism.fol_to_minifol3(FOLSyllogism(x).syllogism))
        print("*** Generated Premises - MINIFOL3 ***")
        gold_split_df['conclusion-MINIFOL3'] = dataset_df['conclusion-FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism.fol_to_minifol3(FOLSyllogism(x).syllogism))
        print("*** Generated Conclusions - MINIFOL3 ***")
        gold_split_df['premises-MINIFOL4'] = dataset_df['premises-FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism.fol_to_minifol4(FOLSyllogism(x).syllogism))
        print("*** Generated Premises - MINIFOL4 ***")
        gold_split_df['conclusion-MINIFOL4'] = dataset_df['conclusion-FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism.fol_to_minifol4(FOLSyllogism(x).syllogism))
        gold_split_df.to_csv(f"../../../experiments/{dataset}/data/{dataset}_kr_gold_{split}_sef.csv", index=False)
        print(f"Generated gold {dataset} dataset for {split} split.")

if __name__ == "__main__":
    # generate gold splits for folio dataset
    for dataset in ["folio"]:
        for split in ["train", "test", "valid"]:
            print(f"Generating gold {dataset} dataset for {split} split...")
            test_generate_minifol_dataset(dataset=dataset, split=split)