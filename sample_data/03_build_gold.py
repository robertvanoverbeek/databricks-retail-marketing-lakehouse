# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
from pyspark.sql import functions as F

catalog = "workspace"
schema = "retail"

customers_silver_table = f"{catalog}.{schema}.customers_silver"
products_silver_table = f"{catalog}.{schema}.products_silver"
orders_silver_table = f"{catalog}.{schema}.orders_silver"

customer_product_sales_gold_table = f"{catalog}.{schema}.customer_product_sales_gold"
sales_by_category_year_gold_table = f"{catalog}.{schema}.sales_by_category_year_gold"

# COMMAND ----------

customers_silver_df = spark.table(customers_silver_table)
products_silver_df = spark.table(products_silver_table)
orders_silver_df = spark.table(orders_silver_table)

customers_silver_df.printSchema()
products_silver_df.printSchema()
orders_silver_df.printSchema()  

# COMMAND ----------

customers = customers_silver_df.alias("c")
products = products_silver_df.alias("p")
orders = orders_silver_df.alias("o")

# COMMAND ----------

customer_product_sales_gold_df = (
    orders
    .join(
        customers,
        on="customer_id",
        how="left"
    )
    .join(
        products,
        on="product_id",
        how="left"
    )
    .select(
        F.col("order_id"),
        F.col("order_date"),

        F.col("customer_id"),
        F.col("first_name"),
        F.col("last_name"),
        F.col("country"),
        F.col("marketing_opt_in"),
        F.col("loyalty_tier"),

        F.col("product_id"),
        F.col("product_name"),
        F.col("category"),
        F.col("brand"),

        F.col("quantity"),
        F.col("o.unit_price").alias("order_unit_price"),
        F.col("discount"),
        F.col("revenue")
    )
)

# COMMAND ----------

customer_product_sales_gold_df.printSchema()


# COMMAND ----------

(
    customer_product_sales_gold_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(customer_product_sales_gold_table)
)

# COMMAND ----------


spark.table(customer_product_sales_gold_table).printSchema()


# COMMAND ----------

spark.table(customer_product_sales_gold_table).show(5)

# COMMAND ----------

spark.table(customer_product_sales_gold_table).count()

# COMMAND ----------

sales_by_category_year_df = (
    customer_product_sales_gold_df
    .groupBy(
        F.year("order_date").alias("year"),
        "category"
    )
    .agg(
        F.count("order_id").alias("total_orders"),
        F.sum("quantity").alias("total_quantity"),
        F.round(F.sum("revenue"), 2).alias("total_revenue")
    )
    .orderBy("year", "category")
)

# COMMAND ----------

(
    sales_by_category_year_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(sales_by_category_year_gold_table)
)

# COMMAND ----------

spark.table(sales_by_category_year_gold_table).show(5)
