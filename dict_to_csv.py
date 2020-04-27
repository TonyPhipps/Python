import pandas as pd
items = [
    {"color":"red", "size":"big", "value":"99"}, 
    {"color":"blue", "size":"medium", "value":"76"}
]

df = pd.DataFrame(items)
csv_data = df.to_csv(index=False)
print(csv_data)