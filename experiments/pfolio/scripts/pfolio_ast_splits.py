import pandas as pd
from sklearn.model_selection import train_test_split

# load dataset
dataset_df = pd.read_csv(f"../data/pfolio_ast_gold_train.csv")

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

dev.to_csv(f"../data/pfolio_ast_train.csv", index=False)
print(f"Generated gold AST dataset for train split.")
val.to_csv(f"../data/pfolio_ast_val.csv", index=False)
print(f"Generated gold AST dataset for val split.")
test.to_csv(f"../data/pfolio_ast_test.csv", index=False)
print(f"Generated gold AST dataset for test split.")