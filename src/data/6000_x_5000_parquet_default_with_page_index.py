import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

# Constants for the table dimensions
n_rows = 10000
n_cols = 5000

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

# Convert DataFrames to PyArrow Tables
table1 = pa.Table.from_pandas(df1)
table2 = pa.Table.from_pandas(df2)

# Save the tables as Parquet files
pq.write_table(table1, "src/data/table1_with_page_index.parquet", write_page_index=True)
pq.write_table(table2, "src/data/table2_with_page_index.parquet", write_page_index=True)

print("Parquet tables created successfully!")
