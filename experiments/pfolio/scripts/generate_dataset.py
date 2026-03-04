import clgc
from clgc.__base import *
import pandas as pd

# generate combined train KR dataset
def generate_dataset(split="train"):
    if split not in ["train", "test", "valid"]:
        raise ValueError("Invalid split name. Must be one of 'train', 'test', or 'valid'.")
    else:
        # init base notations
        dataset_df = pd.read_csv(f"../data/pfolio.csv")
        
        # generate and concat all notations
        gold_split_df = dataset_df
        gold_split_df['Premises - CLIF'] = dataset_df['Premises - FOL'].apply(lambda x: FOLSyllogism.fol_to_clif(FOLSyllogism(x).syllogism))
        gold_split_df['Conclusions - CLIF'] = dataset_df['Conclusions - FOL'].apply(lambda x: FOLSyllogism.fol_to_clif(FOLSyllogism(x).syllogism))
        gold_split_df['Premises - CLINGO'] = dataset_df['Premises - FOL'].apply(lambda x: FOLSyllogism.fol_to_clingo(FOLSyllogism(x).syllogism))
        gold_split_df['Conclusions - CLINGO'] = dataset_df['Conclusions - FOL'].apply(lambda x: FOLSyllogism.fol_to_clingo(FOLSyllogism(x).syllogism))
        gold_split_df['Premises - CGIF'] = dataset_df['Premises - FOL'].apply(lambda x: FOLSyllogism.fol_to_cgif(FOLSyllogism(x).syllogism))
        gold_split_df['Conclusions - CGIF'] = dataset_df['Conclusions - FOL'].apply(lambda x: FOLSyllogism.fol_to_cgif(FOLSyllogism(x).syllogism))
        gold_split_df['Premises - MINIFOL2'] = dataset_df['Premises - FOL'].apply(lambda x: FOLSyllogism.fol_to_minifol2(FOLSyllogism(x).syllogism))
        gold_split_df['Conclusions - MINIFOL2'] = dataset_df['Conclusions - FOL'].apply(lambda x: FOLSyllogism.fol_to_minifol2(FOLSyllogism(x).syllogism))
        gold_split_df['Premises - TFLPLUS'] = dataset_df['Premises - FOL'].apply(lambda x: FOLSyllogism.fol_to_tfl_plus(FOLSyllogism(x.replace("'","").replace("_","")+'\n').syllogism))
        gold_split_df['Conclusions - TFLPLUS'] = dataset_df['Conclusions - FOL'].apply(lambda x: FOLSyllogism.fol_to_tfl_plus(FOLSyllogism(x.replace("'","").replace("_","")+'\n').syllogism))
        gold_split_df.to_csv(f"../data/pfolio_kr_gold_{split}.csv", index=False)
        print(f"Generated gold KR dataset for {split} split.")

if __name__ == "__main__":
    # generate gold splits
    for split in ["train"]:
        generate_dataset(split)