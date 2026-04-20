import pandas as pd
import os

directory = r'C:\Users\tejas\Downloads\Personal Projects\Food-Price-Predictor'
file_path = os.path.join(directory, 'combined_data.csv')

df = pd.read_csv(file_path, encoding='ISO-8859-1')

print("Original shape:", df.shape)

df.columns = (
    df.columns
    .str.replace('"', '')
    .str.strip()
    .str.lower()
)

df = df.drop(columns=['month', 'time'], errors='ignore')

df = df.drop(columns=[col for col in df.columns if 'food.price' in col], errors='ignore')

if 'year' not in df.columns or df['year'].isna().all():
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['year'] = df['date'].dt.year

required = ['country', 'commodity', 'year']
for col in required:
    if col not in df.columns:
        raise ValueError(f"Missing column: {col}")

df['country'] = df['country'].astype(str).str.strip()
df['commodity'] = df['commodity'].astype(str).str.strip()


for col in df.columns:
    if col not in ['country', 'commodity', 'year', 'continent_x', 'continent_y']:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(',', '') 
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna(subset=['country', 'commodity', 'year'])

print("After cleaning:", df.shape)

group_cols = ['country', 'commodity', 'year']

numeric_cols = df.select_dtypes(include='number').columns.tolist()

if 'year' in numeric_cols:
    numeric_cols.remove('year')

print("Numeric columns:", numeric_cols)

yearly_df = df.groupby(group_cols, as_index=False)[numeric_cols].mean()


df['continent'] = pd.NA

if 'continent_x' in df.columns:
    df['continent'] = df['continent_x']

if 'continent_y' in df.columns:
    df['continent'] = df['continent'].combine_first(df['continent_y'])

continent_map = (
    df[['country', 'continent']]
    .dropna()
    .drop_duplicates(subset=['country'])
)

yearly_df = yearly_df.merge(continent_map, on='country', how='left')
yearly_df = yearly_df.drop(columns=['country_code', 'region', 'cost_category', 'data_quality'], errors='ignore')
yearly_df = yearly_df.dropna(axis=1, how='all')

output_path = os.path.join(directory, 'combined_yearly.csv')
yearly_df.to_csv(output_path, index=False)

print("Yearly dataset created!")
print("Final shape:", yearly_df.shape)
print(f"Saved to: {output_path}")