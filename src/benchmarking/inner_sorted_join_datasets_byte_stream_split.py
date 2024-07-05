import duckdb
from pyarrow import parquet

with duckdb.connect() as ddb:
    result = ddb.execute("""
                SELECT *
                FROM ( SELECT * FROM
                    read_parquet('src/data/table1_dataset_byte_stream_split/*')
                    ORDER BY key) as table1
                LEFT JOIN ( SELECT * FROM
                    read_parquet('src/data/table2_dataset_byte_stream_split/*')
                    ORDER BY key) as table2 ON
                    table1.key = table2.key;
                """).arrow()

parquet.write_table(
    table=result, where="src/data/join_result_table1_table2_dataset.parquet"
)
