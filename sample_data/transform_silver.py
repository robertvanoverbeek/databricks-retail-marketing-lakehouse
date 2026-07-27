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

# COMMAND ----------

customers_bronze_df = spark.table(customers_bronze_table)
products_bronze_df = spark.table(products_bronze_table)
orders_bronze_df = spark.table(orders_bronze_table)

# COMMAND ----------

from pyspark.sql import functions as F

duplicate_customer_ids_df = (
    customers_bronze_df
    .groupBy("customer_id")
    .count()
    .filter(F.col("count") > 1)
)
duplicate_customer_id_count = duplicate_customer_ids_df.count()

# COMMAND ----------

invalid_email_count = (
    customers_bronze_df
    .filter(
        F.col("email").isNull()
        | (F.trim(F.col("email")) == "")
    )
    .count()
)


# COMMAND ----------

future_registration_date_count = (
    customers_bronze_df
    .filter(F.col("registration_date") > F.current_date())
    .count()
)

# COMMAND ----------

invalid_registration_date_count = (
    customers_bronze_df
    .filter(
        F.col("registration_date").isNull()
        | (F.col("registration_date") > F.current_date())
    )
    .count()
)

# COMMAND ----------

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
print(f"Verwijderde records: {bronze_customer_count - silver_customer_count}")

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

duplicate_product_ids_df = (
    products_bronze_df
    .groupBy("product_id")
    .count()
    .filter(F.col("count") > 1)
)
duplicate_product_ids_count = duplicate_product_ids_df.count()

# COMMAND ----------

invalid_product_price_count = (
    products_bronze_df
    .filter(
        (F.col("unit_price").isNull())
        | (F.col("unit_price") <= 0)
    )
    .count()
)

# COMMAND ----------

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
print(f"Verwijderde records: {bronze_product_count - silver_product_count}")

# COMMAND ----------

products_silver_df.show(5)

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

# COMMAND ----------

invalid_order_discount_count = (
    orders_bronze_df
    .filter(
        (F.col("discount") < 0 )
        | (F.col("discount") > 1)
    )
    .count()
)

invalid_order_quantity_count = (
    orders_bronze_df
    .filter(
        (F.col("quantity") <= 0 )
    )
    .count()
)

invalid_order_revenue_count = (
    orders_bronze_df
    .filter(
        F.abs(
            (
                F.col("unit_price")
                * (1 - F.col("discount"))
                * F.col("quantity")
            )
            - F.col("revenue")
        ) > 0.01
    )
    .count()
)


# COMMAND ----------

print("Order data-quality checks")
print("--------------------------------")
print(f"Ongeldige korting: {invalid_order_discount_count}")
print(f"Ongeldige hoeveelheid: {invalid_order_quantity_count}")
print(f"Ongeldige omzet: {invalid_order_revenue_count}")



# COMMAND ----------

orders_silver_df = (
    orders_bronze_df
    .filter(
        (F.col("discount") >= 0)
        & (F.col("discount") <= 1)
        & (F.col("quantity") > 0)
        & (
            F.abs(
                (
                    F.col("unit_price")
                    * (1 - F.col("discount"))
                    * F.col("quantity")
                )
                - F.col("revenue")
            ) <= 0.01
        )
    )
    .dropDuplicates(["order_id"])
)

# COMMAND ----------

bronze_order_count = orders_bronze_df.count()
silver_order_count = orders_silver_df.count()

print(f"Bronze records: {bronze_order_count}")
print(f"Silver records: {silver_order_count}")
print(f"Verwijderde records: {bronze_order_count - silver_order_count}")

# COMMAND ----------

(
    orders_silver_df.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable(orders_silver_table)
)

# COMMAND ----------

orders_silver_df = spark.table(orders_silver_table)
orders_silver_df.show(5)
