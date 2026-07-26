# Databricks notebook source
from pyspark.sql import SparkSession

spark = SparkSession.getActiveSession()

# COMMAND ----------

print(f"Spark version: {spark.version}")

# COMMAND ----------

spark.sql("SELECT current_catalog()").show()

# COMMAND ----------

spark.sql("SELECT current_schema()").show()
