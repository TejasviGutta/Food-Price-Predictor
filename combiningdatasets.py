import pandas as pd
import glob
import os

directory = r'C:\Users\tejas\Downloads\Personal Projects\Food-Price-Predictor'

csv_files = [f for f in glob.glob(os.path.join(directory, '*.csv')) if 'combined_data.csv' not in f]

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
    combined_df.to_csv(os.path.join(directory, 'combined_data.csv'), index=False)
    print("CSV files combined successfully!")