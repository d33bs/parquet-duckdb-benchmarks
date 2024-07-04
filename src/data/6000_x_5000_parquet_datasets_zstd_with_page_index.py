import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import os

# Constants for the table dimensions and chunk size
n_rows = 10000
n_cols = 5000
chunk_size = 1000

# Generate unique keys
keys = np.arange(1, n_rows + 1)

# Create the first DataFrame with 'key' column
data1 = {
    "key": keys,
}
for i in range(1, n_cols):
    data1[f"col1_{i}"] = np.random.random(n_rows)

df1 = pd.DataFrame(data1)

# Create the second DataFrame with 'key' column
data2 = {
    "key": keys,
}
for i in range(1, n_cols):
    data2[f"col2_{i}"] = np.random.random(n_rows)

df2 = pd.DataFrame(data2)

# Define output directories
output_dir1 = "src/data/table1_dataset_zstd_with_page_index"
output_dir2 = "src/data/table2_dataset_zstd_with_page_index"

# Create directories if they don't exist
os.makedirs(output_dir1, exist_ok=True)
os.makedirs(output_dir2, exist_ok=True)


# Function to save DataFrame in chunks
def save_dataframe_in_chunks(df, output_dir, chunk_size):
    for start in range(0, len(df), chunk_size):
        end = start + chunk_size
        chunk = df.iloc[start:end]
        table = pa.Table.from_pandas(chunk)
        file_path = os.path.join(output_dir, f"chunk_{start // chunk_size + 1}.parquet")
        pq.write_table(table, file_path, write_page_index=True, compression="ZSTD")


# Save both DataFrames in chunks
save_dataframe_in_chunks(df1, output_dir1, chunk_size)
save_dataframe_in_chunks(df2, output_dir2, chunk_size)

print("Parquet datasets created successfully in chunks!")
