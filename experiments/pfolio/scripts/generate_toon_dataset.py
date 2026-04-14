import sys
sys.path.append('../../../')
from src.clgc.__base import *
import pandas as pd


# generate combined train TOON dataset
def generate_toon_dataset(split="train"):
    if split not in ["train", "test", "valid"]:
        raise ValueError("Invalid split name. Must be one of 'train', 'test', or 'valid'.")
    else:
        # init base notations
        dataset_df = pd.read_csv(f"../data/pfolio.csv")
    
        # generate and concat all notations
        gold_split_df = dataset_df
        #gold_split_df['Premises - FOL'] = dataset_df['Premises - FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism(x).syllogism).apply(lambda x: ''.join([line+'\n' for line in x.splitlines()])).apply(lambda x: FOLSyllogism(x+'\n').validate(grammar='fol'))
        #print("*** Generated Premises - FOL ***")
        #gold_split_df['Conclusions - FOL'] = dataset_df['Conclusions - FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism(x).syllogism).apply(lambda x: ''.join([line+'\n' for line in x.splitlines()])).apply(lambda x: FOLSyllogism(x+'\n').validate(grammar='fol'))
        #print("*** Generated Conclusions - FOL ***")
        gold_split_df['Premises - CLIF'] = dataset_df['Premises - FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism.fol_to_clif(FOLSyllogism(x).syllogism)).apply(lambda x: ''.join([line+'\n' for line in x.splitlines()])).apply(lambda x: FOLSyllogism(x+'\n').treeify(x, grammar='clif', format='json')).apply(lambda x: FOLSyllogism.simplify_tree(x)).apply(lambda x: FOLSyllogism.toonify(x))
        print("*** Generated Premises - CLIF ***")
        gold_split_df['Conclusions - CLIF'] = dataset_df['Conclusions - FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism.fol_to_clif(FOLSyllogism(x).syllogism)).apply(lambda x: ''.join([line+'\n' for line in x.splitlines()])).apply(lambda x: FOLSyllogism(x+'\n').treeify(x, grammar='clif', format='json')).apply(lambda x: FOLSyllogism.simplify_tree(x)).apply(lambda x: FOLSyllogism.toonify(x))
        print("*** Generated Conclusions - CLIF ***")
        gold_split_df.to_csv(f"../data/pfolio_ast_formats_{split}.csv", index=False)
        print(f"Generated TOON dataset for {split} split.")

if __name__ == "__main__":
    # generate gold splits
    for split in ["train"]:
        generate_toon_dataset(split)