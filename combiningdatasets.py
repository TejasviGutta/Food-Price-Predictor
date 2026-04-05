import pandas as pd
import glob

# Directory containing CSV files (adjust path as needed)
directory = '/c:/Users/tejas/Downloads/Personal Projects/Food-Price-Predictor/'

# Get all CSV files in the directory
csv_files = glob.glob(directory + '*.csv')

# List to hold dataframes
dfs = []

# Read each CSV file and append to list
for file in csv_files:
    df = pd.read_csv(file)
    dfs.append(df)

# Concatenate all dataframes (assuming same columns)
combined_df = pd.concat(dfs, ignore_index=True)

# Save combined dataframe to a new CSV file
combined_df.to_csv(directory + 'combined_data.csv', index=False)

print("CSV files combined successfully!")