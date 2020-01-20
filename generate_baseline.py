import pandas
import os


filename_all_table_data = "table_data_all_tables_internal.csv"
filename_baseline_file = "V1_baseline_datalagoon.tsv"  # EDIT
schema_to_search = "datalagoon"  # EDIT


def generate_baseline():
    print(f"\n>> Reading Data from {filename_all_table_data}")
    df = pandas.read_csv(filename_all_table_data)

    schema_name = df["schema_name"].tolist()
    table_name = df["table_name"].tolist()
    owner = df["owner"].tolist()
    # Keeping here in case we need to only put one of tables or views in file
    # table_type = df["table_type"].tolist()

    lines = []
    this_schema_tables = []
    this_schema_owners = []

    j = 0
    for i in range(len(table_name)):
        if schema_name[i] == schema_to_search and "_all" not in table_name[i]:
            this_schema_tables.append(table_name[i])
            this_schema_owners.append(owner[i])
            j += 1
    print(f"\n>> Number of tables in {schema_to_search}: {j}")


    current_table_name = ""
    with open(filename_baseline_file) as f:
        while True:
            c = f.read(1)
            if not c:
                print(f">> Finished reading {filename_baseline_file}.")
                break

            for line in f:
                if ";" not in line:
                    if "CREATE TABLE" in line:
                        lines.append(f"\n{line.rstrip()}\n")
                        current_table_name = line.replace(f"CREATE TABLE IF NOT EXISTS {schema_to_search}.", "")
                    else:
                        lines.append(f"{line.rstrip()}\n")
                else:
                    if "DROP TABLE" in line:
                        pass
                    elif "ALTER TABLE" in line:
                        lines.append(f"{line.rstrip()}\n")
                    else:
                        for table in this_schema_tables:
                            if table.strip() == current_table_name.strip():
                                index = this_schema_tables.index(table)
                                lines.append(f";\nALTER TABLE {schema_to_search.strip()}.{this_schema_tables[index].strip()} OWNER TO {this_schema_owners[index].strip()};\n")
                                break

    new_filename = f"V1_baseline_{schema_to_search}.sql"
    new_file_path = f"generated-files/{new_filename}"
    # create generated-files/ subdirectory
    os.makedirs(os.path.dirname(new_file_path), exist_ok=True)

    print(f"\n>> Writing to {new_filename}.\n>> Please review this file. You'll find it in generated-files/")

    with open(new_file_path, "w") as f:
        f.writelines(lines)
    print(f"\n>> Successfully created the new baseline script, saved as {new_filename}")


if __name__ == "__main__":
    generate_baseline()
