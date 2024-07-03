import duckdb
from pyarrow import parquet

with duckdb.connect() as ddb:
    result = ddb.execute("""
                SELECT *
                FROM read_parquet('src/data/table1.parquet') as table1
                LEFT JOIN read_parquet('src/data/table2.parquet') as table2 ON
                    table1.key = table2.key;
                """).arrow()

parquet.write_table(table=result, where="src/data/join_result_table1_table2.parquet")
