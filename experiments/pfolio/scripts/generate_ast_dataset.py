import sys
sys.path.append('../../../')
from src.clgc.__base import *
import pandas as pd

# generate combined train KR dataset
def generate_ast_dataset(split="train"):
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
        gold_split_df['Premises - CLIF'] = dataset_df['Premises - FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism.fol_to_clif(FOLSyllogism(x).syllogism)).apply(lambda x: ''.join([line+'\n' for line in x.splitlines()])).apply(lambda x: FOLSyllogism(x+'\n').treeify(x, grammar='clif', format='str'))
        print("*** Generated Premises - CLIF ***")
        gold_split_df['Conclusions - CLIF'] = dataset_df['Conclusions - FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism.fol_to_clif(FOLSyllogism(x).syllogism)).apply(lambda x: ''.join([line+'\n' for line in x.splitlines()])).apply(lambda x: FOLSyllogism(x+'\n').treeify(x, grammar='clif', format='str'))
        print("*** Generated Conclusions - CLIF ***")
        #gold_split_df['Premises - CLINGO'] = dataset_df['Premises - FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism.fol_to_clingo(FOLSyllogism(x).syllogism)).apply(lambda x: ''.join([line+'\n' for line in x.splitlines()])).apply(lambda x: FOLSyllogism(x+'\n').validate(grammar='clingo'))
        #print("*** Generated Premises - CLINGO ***")
        #gold_split_df['Conclusions - CLINGO'] = dataset_df['Conclusions - FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism.fol_to_clingo(FOLSyllogism(x).syllogism)).apply(lambda x: ''.join([line+'\n' for line in x.splitlines()])).apply(lambda x: FOLSyllogism(x+'\n').validate(grammar='clingo'))
        #print("*** Generated Conclusions - CLINGO ***")
        #gold_split_df['Premises - CGIF'] = dataset_df['Premises - FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism.fol_to_cgif(FOLSyllogism(x).syllogism)).apply(lambda x: ''.join([line+'\n' for line in x.splitlines()])).apply(lambda x: FOLSyllogism(x+'\n').validate(grammar='cgif'))
        #print("*** Generated Premises - CGIF ***")
        #gold_split_df['Conclusions - CGIF'] = dataset_df['Conclusions - FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism.fol_to_cgif(FOLSyllogism(x).syllogism)).apply(lambda x: ''.join([line+'\n' for line in x.splitlines()])).apply(lambda x: FOLSyllogism(x+'\n').validate(grammar='cgif'))
        #print("*** Generated Conclusions - CGIF ***")
        #gold_split_df['Premises - MINIFOL2'] = dataset_df['Premises - FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism.fol_to_minifol2(FOLSyllogism(x).syllogism)).apply(lambda x: ''.join([line+'\n' for line in x.splitlines()])).apply(lambda x: FOLSyllogism(x+'\n').validate(grammar='minifol2'))
        #print("*** Generated Premises - MINIFOL2 ***")
        #gold_split_df['Conclusions - MINIFOL2'] = dataset_df['Conclusions - FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism.fol_to_minifol2(FOLSyllogism(x).syllogism)).apply(lambda x: ''.join([line+'\n' for line in x.splitlines()])).apply(lambda x: FOLSyllogism(x+'\n').validate(grammar='minifol2'))
        #print("*** Generated Conclusions - MINIFOL2 ***")
        #gold_split_df['Premises - TFLPLUS'] = dataset_df['Premises - FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: ''.join([line+'\n' for line in x.splitlines()])).apply(lambda x: FOLSyllogism.fol_to_tfl_plus(FOLSyllogism(x).syllogism)).apply(lambda x: FOLSyllogism(x+'\n').validate(grammar='tfl+'))
        #print("*** Generated Premises - TFLPLUS ***")
        #gold_split_df['Conclusions - TFLPLUS'] = dataset_df['Conclusions - FOL'].apply(lambda x: x.replace("'", "").replace("_", "")).apply(lambda x: FOLSyllogism.fol_to_tfl_plus(FOLSyllogism(x.replace("'","").replace("_","")+'\n').syllogism)).apply(lambda x: ''.join([line+'\n' for line in x.splitlines()])).apply(lambda x: FOLSyllogism(x+'\n').validate(grammar='tfl+'))
        #print("*** Generated Conclusions - TFLPLUS ***")
        gold_split_df.to_csv(f"../data/pfolio_ast_gold_{split}.csv", index=False)
        print(f"Generated gold AST dataset for {split} split.")

if __name__ == "__main__":
    # generate gold splits
    for split in ["train"]:
        generate_ast_dataset(split)