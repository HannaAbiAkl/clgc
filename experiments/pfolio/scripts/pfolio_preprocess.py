import pandas as pd
import requests

headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = "https://datasets-server.huggingface.co/first-rows?dataset=yale-nlp%2FP-FOLIO&config=default&split=train"

def query():
    response = requests.get(API_URL, headers=headers)
    return response.json()

def format_rows(dataset):
  df = pd.DataFrame()
  for i in range(len(dataset['rows'])):
    row = dataset['rows'][i]['row']
    print("** ROW:", row)
    for k, v in row.items():
      row[k] = v
    row_df =  pd.DataFrame.from_dict([row])
    df = pd.concat([df, row_df])
  return df

data = query()
dataset_df = format_rows(data)
# Columns that need row duplication
cols_to_expand = ["Truth Values", "Conclusions - NL", "Conclusions - FOL"]
# Convert multiline strings into aligned lists
dataset_df[cols_to_expand] = (
    dataset_df[cols_to_expand]
    .apply(lambda col: col.fillna("")
                      .apply(lambda x: [v.strip() for v in str(x).split("\n") if v.strip()]))
)
# Explode all three columns together (alignment preserved)
dataset_df = dataset_df.explode(cols_to_expand, ignore_index=True)
# Optional: clean index
dataset_df.reset_index(drop=True, inplace=True)
# Export to csv
dataset_df.to_csv("../data/pfolio.csv", index=False)