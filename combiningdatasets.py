import pandas as pd
import glob
import os

directory = r'C:\Users\tejas\Downloads\Personal Projects\Food-Price-Predictor'

csv_files = [
    f for f in glob.glob(os.path.join(directory, '*.csv'))
    if 'combined_data.csv' not in f
    and 'continents.csv' not in f   
]

print(f"Found {len(csv_files)} CSV files.")

dfs = []

for file in csv_files:
    try:
        df = pd.read_csv(file)
        dfs.append(df)
    except Exception as e:
        print(f"Error reading {file}: {e}")

if not dfs:
    print("No CSV files found.")
else:
    combined_df = pd.concat(dfs, ignore_index=True)

    combined_df = combined_df.drop(columns=['Unnamed: 0'], errors='ignore')
    combined_df = combined_df.drop(columns=['price_type'], errors='ignore')
    combined_df = combined_df.drop(columns=['market'], errors='ignore')

    # Load continents file
    continents_df = pd.read_csv(os.path.join(directory, 'continents_249.csv'))

    # Clean column names
    combined_df.columns = combined_df.columns.str.strip().str.lower()
    continents_df.columns = continents_df.columns.str.strip().str.lower()

    # Clean country names
    combined_df['country'] = combined_df['country'].astype(str).str.strip()
    continents_df['country'] = continents_df['country'].astype(str).str.strip()

    # Merge (LEFT JOIN)
    combined_df = combined_df.merge(
        continents_df[['country', 'continent']],
        on='country',
        how='left'
    )


    combined_df.to_csv(os.path.join(directory, 'combined_data.csv'), index=False)

    print("combined_data.csv created with continent column!")