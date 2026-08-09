# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
from pathlib import Path
import shutil

from pyspark.sql import functions as F

# COMMAND ----------

current_directory = Path.cwd()
project_root = current_directory.parent
source_directory = project_root / "data" / "generated"
volume_path = Path("/Volumes/workspace/retail/raw_files")
catalog_name = "workspace"
schema_name = "retail"

# COMMAND ----------


customers_file = source_directory / "customers.csv"

destination = volume_path / "customers.csv"

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

print(destination)
print(type(destination))
print(type(str(destination)))

# COMMAND ----------

customers_bronze_df.printSchema()

# COMMAND ----------

customers_bronze_df = (
    customers_bronze_df
    .select(
        "customer_id",
        "first_name",
        "last_name",
        "email",
        "country",
        "registration_date",
        "marketing_opt_in",
        "loyalty_tier",
    )
    .withColumn("_ingested_at", F.current_timestamp())
)

# COMMAND ----------

customers_bronze_df.show(5, truncate=False)
customers_bronze_df.printSchema()

# COMMAND ----------

customers_table = f"{catalog_name}.{schema_name}.customers_bronze"

(
    customers_bronze_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(customers_table)
)

print(f"Table written: {customers_table}")

# COMMAND ----------

spark.table(customers_table).show(5, truncate=False)

# COMMAND ----------

products_file = source_directory / "products.csv"

destination = Path(volume_path) / "products.csv"

shutil.copy(products_file, destination)

print("Products copied!")

# COMMAND ----------

products_bronze_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(destination))
)
products_bronze_df.printSchema()

# COMMAND ----------

products_bronze_df = (
    products_bronze_df
    .select(
        "category",
        "brand",
        "product_name",
        "unit_price",
        "product_id",
    )
    .withColumn("_ingested_at", F.current_timestamp())
)
products_bronze_df.printSchema()

# COMMAND ----------

products_table = f"{catalog_name}.{schema_name}.products_bronze"

(
    products_bronze_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(products_table)
)

print(f"Table written: {products_table}")

# COMMAND ----------

spark.table(customers_table).show(5)

spark.table(products_table).show(5)
