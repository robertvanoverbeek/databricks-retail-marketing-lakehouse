# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# Databricks notebook source
# MAGIC %md
# MAGIC # Bronze ingestion
# MAGIC
# MAGIC **Doel:** gegenereerde CSV-bronbestanden inlezen en opslaan als Delta-tabellen.
# MAGIC
# MAGIC **Input:** CSV-bestanden uit `data/generated`
# MAGIC
# MAGIC **Output:** Bronze-tabellen in `workspace.retail`

# COMMAND ----------

from pathlib import Path
import shutil

from pyspark.sql import functions as F

# COMMAND ----------

current_directory = Path.cwd()

print(f"Current directory: {current_directory}")

# COMMAND ----------

project_root = current_directory.parent
source_directory = project_root / "data" / "generated"
customers_file = source_directory / "customers.csv"

print(f"Project root: {project_root}")
print(f"Source directory: {source_directory}")
print(f"Customers file: {customers_file}")
print(f"File exists: {customers_file.exists()}")

# COMMAND ----------

catalog_name = "workspace"
schema_name = "retail"
volume_name = "raw_files"

spark.sql(f"""
CREATE SCHEMA IF NOT EXISTS {catalog_name}.{schema_name}
COMMENT 'Retail marketing lakehouse project'
""")

spark.sql(f"""
CREATE VOLUME IF NOT EXISTS {catalog_name}.{schema_name}.{volume_name}
COMMENT 'Raw source files used for Bronze ingestion'
""")

print(f"Schema ready: {catalog_name}.{schema_name}")
print(f"Volume ready: {catalog_name}.{schema_name}.{volume_name}")

# COMMAND ----------

spark.sql(f"SHOW VOLUMES IN {catalog_name}.{schema_name}").show(truncate=False)

# COMMAND ----------

volume_path = f"/Volumes/{catalog_name}/{schema_name}/{volume_name}"

print(f"Volume path: {volume_path}")

# COMMAND ----------

import shutil

destination = Path(volume_path) / "customers.csv"

shutil.copy(customers_file, destination)

print("Customers copied!")

# COMMAND ----------

customers_bronze_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(destination))
)

customers_bronze_df.show(5)

# COMMAND ----------


