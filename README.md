# generate-V1-baseline-files

After cloning...

1. Change filename_baseline_file and schema_to_search strings (in generate_baseline.py) to the correct values.

2. ```pipenv install pandas```

3. ```pipenv shell```

4. ```python generate_baseline.py```

----------

Tips...

1. It would be best to update the table_data_all_tables_internal.csv before running. Use DataGrip or similar and run this script in internal redshift:
```
-- get schema name, owner, table name, type for whole internal redshift
SELECT n.nspname AS schema_name
 , c.relname AS table_name
 , pg_get_userbyid(c.relowner) AS table_owner
 , CASE WHEN c.relkind = 'v' THEN 'view' ELSE 'table' END
   AS table_type
 FROM pg_class As c
 LEFT JOIN pg_namespace n ON n.oid = c.relnamespace
 LEFT JOIN pg_tablespace t ON t.oid = c.reltablespace
 LEFT JOIN pg_description As d
      ON (d.objoid = c.oid AND d.objsubid = 0)
 WHERE c.relkind IN('r', 'v')
ORDER BY n.nspname, c.relname ;
```

Export the returned values as a CSV file. Rename the new file to table_data_all_tables_internal.csv and place it in the folder.

2. Use this script to get the ddl for your schema (replace datalake references with your schema):
```
-- Get ddl for schema
SET SEARCH_PATH TO datalake; -- Replace with schema
SELECT ddl
FROM admin.v_generate_tbl_ddl
JOIN pg_table_def ON (
    admin.v_generate_tbl_ddl.schemaname = pg_table_def.schemaname AND
    admin.v_generate_tbl_ddl.tablename = pg_table_def.tablename
)
WHERE admin.v_generate_tbl_ddl.schemaname = 'datalake' -- Replace with schema
GROUP BY admin.v_generate_tbl_ddl.tablename, ddl, "seq"
ORDER BY admin.v_generate_tbl_ddl.tablename ASC, "seq" ASC;
```

Export the returned values as a TSV file, then remove all " characters from the file. Rename the new file to V1_baseline_SCHEMA.sql (Replace SCHEMA with your schema) and place it in the folder.
