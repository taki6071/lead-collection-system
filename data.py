import pandas as pd
import ast

df_messed = pd.read_csv('leads.csv')

all_rows = []
for col in df_messed.columns:
    for cell in df_messed[col]:
        if pd.notna(cell): 
            try:
                row_dict = ast.literal_eval(cell)
                all_rows.append(row_dict)
            except:
                print(f"Failed to parse: {cell}")

df_clean = pd.DataFrame(all_rows)

print("✅ Cleaned DataFrame created!")
print(f"Shape: {df_clean.shape}")
print(f"\nColumns: {df_clean.columns.tolist()}")
print(f"\nFirst 5 rows:")
print(df_clean.head())

df_clean.to_csv('leads_cleaned.csv', index=False)
print("✅ Saved to 'leads_cleaned.csv'")