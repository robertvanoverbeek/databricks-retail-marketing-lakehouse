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

orders_table = f"{catalog_name}.{schema_name}.orders_bronze"
processed_order_files_table = (
    f"{catalog_name}.{schema_name}.processed_order_files"
)

# COMMAND ----------

# DBTITLE 1,copy the files to catalog
order_files = list(source_directory.glob("orders_*.csv"))

for order_file in order_files:
    destination = volume_path / order_file.name
    shutil.copy(order_file, destination)

    print(f"Copied: {order_file.name}")

# COMMAND ----------

# DBTITLE 1,pyspark to read multiple files at once
# orders_source = f"{volume_path}/orders_*.csv"

# let op dit leest dus alle bestanden ineens in

# orders_bronze_df = (
#     spark.read
#     .option("header", True)
#     .option("inferSchema", True)
#     .csv(orders_source)
# )

# print(f"Number of orders: {orders_bronze_df.count()}")

# orders_bronze_df.show(5)
# orders_bronze_df.printSchema()

# COMMAND ----------

processed_order_files = f"{catalog_name}.{schema_name}.processed_order_files"
processed_order_files_df = spark.table(processed_order_files_table)
processed_order_files_df.printSchema()
processed_order_files_df.show()



# COMMAND ----------

files = dbutils.fs.ls(str(volume_path))

order_files = [
    file
    for file in files
    if file.name.startswith("orders_")
]

available_order_files_df = spark.createDataFrame(
    [(file.name,) for file in order_files],
    ["file_name"],
)

available_order_files_df.show()

# COMMAND ----------

new_order_files_df = (
    available_order_files_df
    .join(
        processed_order_files_df,
        on="file_name",
        how="left_anti",
    )
)

new_order_files_df.show()

# COMMAND ----------

new_file_names = [
    row.file_name
    for row in new_order_files_df.collect()
]

new_file_names

# COMMAND ----------

new_file_paths = [
    str(volume_path / file_name)
    for file_name in new_file_names
]

new_file_paths

# COMMAND ----------

if new_file_paths:
    new_orders_df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(new_file_paths)
        .select(
            "*",
            F.col("_metadata.file_name").alias("_source_file"),
        )
        .select(
            "order_id",
            "customer_id",
            "product_id",
            "order_date",
            "quantity",
            "unit_price",
            "discount",
            "revenue",
            "_source_file",
        )
        .withColumn("_ingested_at", F.current_timestamp())
    )

    print(f"New orders: {new_orders_df.count()}")

    (
        new_orders_df.write
        .format("delta")
        .mode("append")
        .saveAsTable(orders_table)
    )

    processed_new_files_df = (
        new_order_files_df
        .withColumn(
            "processed_at",
            F.current_timestamp(),
        )
    )

    (
        processed_new_files_df.write
        .format("delta")
        .mode("append")
        .saveAsTable(processed_order_files_table)
    )

    print(f"Processed files: {new_file_names}")

else:
    print("No new order files to process.")

# COMMAND ----------

processed_order_files_df = spark.table(processed_order_files_table)

processed_order_files_df.show()
