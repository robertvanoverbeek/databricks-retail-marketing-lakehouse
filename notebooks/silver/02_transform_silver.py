# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
catalog = "workspace"
schema = "retail"

customers_bronze_table = f"{catalog}.{schema}.customers_bronze"
products_bronze_table = f"{catalog}.{schema}.products_bronze"
orders_bronze_table = f"{catalog}.{schema}.orders_bronze"

customers_silver_table = f"{catalog}.{schema}.customers_silver"
products_silver_table = f"{catalog}.{schema}.products_silver"
orders_silver_table = f"{catalog}.{schema}.orders_silver"

from pyspark.sql import functions as F

# COMMAND ----------

# DBTITLE 1,Process Orders
orders_bronze_df = spark.table(orders_bronze_table)

orders_bronze_df.printSchema()

# COMMAND ----------

# DBTITLE 1,quality checks
print(f"Bronze rows: {orders_bronze_df.count()}")

# COMMAND ----------

orders_silver_df = (
    orders_bronze_df
    .dropDuplicates(["order_id"])
)

# COMMAND ----------

print(f"Bronze rows: {orders_bronze_df.count()}")
print(f"Silver rows after deduplication: {orders_silver_df.count()}")

# COMMAND ----------

# future orders is possible by design of the case

future_orders = (
    orders_bronze_df
    .filter(F.col("order_date") > F.current_date())
)

print(future_orders.count())

# COMMAND ----------

duplicate_order_ids = (
    orders_bronze_df
    .groupBy("order_id")
    .count()
    .filter(F.col("count") > 1)
)

print(f"Duplicate order IDs: {duplicate_order_ids.count()}")

# COMMAND ----------

invalid_quantity = orders_bronze_df.filter(F.col("quantity") <= 0).count()
invalid_price = orders_bronze_df.filter(F.col("unit_price") < 0).count()
invalid_discount = orders_bronze_df.filter(
    (F.col("discount") < 0) | (F.col("discount") > 1)
).count()
invalid_revenue = orders_bronze_df.filter(F.col("revenue") < 0).count()

print(f"Invalid quantity: {invalid_quantity}")
print(f"Invalid unit price: {invalid_price}")
print(f"Invalid discount: {invalid_discount}")
print(f"Invalid revenue: {invalid_revenue}")

# COMMAND ----------

orders_checked_df = (
    orders_bronze_df
    .withColumn(
        "_calculated_revenue",
        F.bround(
            F.col("quantity")
            * F.col("unit_price").cast("decimal(10,2)")
            * (F.lit(1).cast("decimal(3,2)") - F.col("discount").cast("decimal(3,2)")),
            2,
        ),
    )
)

revenue_difference_df = (
    orders_checked_df
    .withColumn(
        "difference",
        F.round(
            F.col("revenue") - F.col("_calculated_revenue"),
            2,
        ),
    )
)

(
    revenue_difference_df
    .groupBy("difference")
    .count()
    .orderBy("difference")
    .show()
)


# COMMAND ----------

orders_silver_table = f"{catalog}.{schema}.orders_silver"

(
    orders_silver_df.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(orders_silver_table)
)

# COMMAND ----------

spark.table(orders_silver_table).printSchema()

# COMMAND ----------


orders_silver_table = f"{catalog}.{schema}.orders_silver"

(
    orders_silver_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(orders_silver_table)
)

# COMMAND ----------

display(
    spark.table(orders_silver_table).head(3)
)

# COMMAND ----------

# DBTITLE 1,Process customers
customers_bronze_df = spark.table(customers_bronze_table)

# COMMAND ----------

duplicate_customer_ids_df = (
    customers_bronze_df
    .groupBy("customer_id")
    .count()
    .filter(F.col("count") > 1)
)
duplicate_customer_id_count = duplicate_customer_ids_df.count()

invalid_email_count = (
    customers_bronze_df
    .filter(
        F.col("email").isNull()
        | (F.trim(F.col("email")) == "")
    )
    .count()
)

future_registration_date_count = (
    customers_bronze_df
    .filter(F.col("registration_date") > F.current_date())
    .count()
)

invalid_registration_date_count = (
    customers_bronze_df
    .filter(
        F.col("registration_date").isNull()
        | (F.col("registration_date") > F.current_date())
    )
    .count()
)

print("Customer data-quality checks")
print("--------------------------------")
print(f"Dubbele customer_id's: {duplicate_customer_id_count}")
print(f"Lege e-mailadressen: {invalid_email_count}")
print(f"Ongeldige registratiedatums: {invalid_registration_date_count}")




# COMMAND ----------

customers_silver_df = (
    customers_bronze_df
    .filter(
        F.col("email").isNotNull()
        & (F.trim(F.col("email")) != "")
    )
    .filter(
        F.col("registration_date").isNotNull()
        & (F.col("registration_date") <= F.current_date())
    )
    .dropDuplicates(["customer_id"])
)

# COMMAND ----------

bronze_customer_count = customers_bronze_df.count()
silver_customer_count = customers_silver_df.count()

print(f"Bronze records: {bronze_customer_count}")
print(f"Silver records: {silver_customer_count}")
print(f"removed records: {bronze_customer_count - silver_customer_count}")

# COMMAND ----------

customers_silver_df.show(5)

# COMMAND ----------

(
    customers_silver_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(customers_silver_table)
)

# COMMAND ----------

customers_silver_df = spark.table(customers_silver_table)
customers_silver_df.show(5)

# COMMAND ----------

# DBTITLE 1,Process products
products_bronze_df = spark.table(products_bronze_table)

# COMMAND ----------

# DBTITLE 1,quality checks
duplicate_product_ids_df = (
    products_bronze_df
    .groupBy("product_id")
    .count()
    .filter(F.col("count") > 1)
)
duplicate_product_ids_count = duplicate_product_ids_df.count()

invalid_product_price_count = (
    products_bronze_df
    .filter(
        (F.col("unit_price").isNull())
        | (F.col("unit_price") <= 0)
    )
    .count()
)

print("Product data-quality checks")
print("--------------------------------")
print(f"Dubbele product_id's: {duplicate_product_ids_count}")
print(f"Ongeldige prijzen: {invalid_product_price_count}")

# COMMAND ----------

products_silver_df = (
    products_bronze_df
    .filter(
        (F.col("unit_price").isNotNull())
        & (F.col("unit_price") > 0)
    )
    .dropDuplicates(["product_id"])
)

# COMMAND ----------

bronze_product_count = products_bronze_df.count()
silver_product_count = products_silver_df.count()

print(f"Bronze records: {bronze_product_count}")
print(f"Silver records: {silver_product_count}")
print(f"removed records: {bronze_product_count - silver_product_count}")

# COMMAND ----------

(
    products_silver_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(products_silver_table)
)

# COMMAND ----------

products_silver_df = spark.table(products_silver_table)
products_silver_df.show(5)
