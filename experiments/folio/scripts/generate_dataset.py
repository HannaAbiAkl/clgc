import pandas as pd

# generate combined train KR dataset
def generate_dataset(split="train"):
    if split not in ["train", "test", "valid"]:
        raise ValueError("Invalid split name. Must be one of 'train', 'test', or 'valid'.")
    else:
        # init base notations
        fol_split_df = pd.read_csv(f"../data/fol_{split}.csv")
        clif_split_df = pd.read_csv(f"../data/clif_{split}.csv")
        clingo_split_df = pd.read_csv(f"../data/clingo_{split}.csv")
        cgif_split_df = pd.read_csv(f"../data/cgif_{split}.csv")
        minifol_split_df = pd.read_csv(f"../data/minifol2_{split}.csv")
        tflplus_split_df = pd.read_csv(f"../data/tflplus_{split}.csv")
        
        # concat all notations
        gold_split_df = fol_split_df
        gold_split_df['premises-CLIF'] = clif_split_df['premises-CLIF']
        gold_split_df['conclusion-CLIF'] = clif_split_df['conclusion-CLIF']
        gold_split_df['premises-CLINGO'] = clingo_split_df['premises-CLINGO']
        gold_split_df['conclusion-CLINGO'] = clingo_split_df['conclusion-CLINGO']
        gold_split_df['premises-CGIF'] = cgif_split_df['premises-CGIF']
        gold_split_df['conclusion-CGIF'] = cgif_split_df['conclusion-CGIF']
        gold_split_df['premises-MINIFOL2'] = minifol_split_df['premises-MINIFOL2']
        gold_split_df['conclusion-MINIFOL2'] = minifol_split_df['conclusion-MINIFOL2']
        gold_split_df['premises-TFLPLUS'] = tflplus_split_df['premises-TFLPLUS']
        gold_split_df['conclusion-TFLPLUS'] = tflplus_split_df['conclusion-TFLPLUS']
        gold_split_df.to_csv(f"../data/folio_kr_gold_{split}.csv", index=False)
        print(f"Generated gold KR dataset for {split} split.")

if __name__ == "__main__":
    # generate gold splits
    for split in ["train", "test", "valid"]:
        generate_dataset(split)