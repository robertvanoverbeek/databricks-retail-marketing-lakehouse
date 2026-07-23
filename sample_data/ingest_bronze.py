from pyspark.sql import SparkSession

spark = SparkSession.getActiveSession()

print(spark.version)