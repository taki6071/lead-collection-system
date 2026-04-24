import pandas as pd
import ast

# Load the messed up CSV
df_messed = pd.read_csv('leads.csv')

# Convert each cell from string dictionary to actual dictionary
all_rows = []
for col in df_messed.columns:
    for cell in df_messed[col]:
        if pd.notna(cell):  # Skip empty cells
            try:
                # Convert string to dictionary
                row_dict = ast.literal_eval(cell)
                all_rows.append(row_dict)
            except:
                print(f"Failed to parse: {cell}")

# Create proper DataFrame
df_clean = pd.DataFrame(all_rows)

print("✅ Cleaned DataFrame created!")
print(f"Shape: {df_clean.shape}")
print(f"\nColumns: {df_clean.columns.tolist()}")
print(f"\nFirst 5 rows:")
print(df_clean.head())

df_clean.to_csv('leads_cleaned.csv', index=False)
print("✅ Saved to 'leads_cleaned.csv'")