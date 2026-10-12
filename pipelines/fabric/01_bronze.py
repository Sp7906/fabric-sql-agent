# Fabric notebook 1: Bronze - land raw files as-is into a Delta table.
from pyspark.sql import functions as F

raw = (spark.read.option("header", True).csv("Files/raw/orders.csv")
       .withColumn("_ingested_at", F.current_timestamp())
       .withColumn("_source_file", F.input_file_name()))

raw.write.format("delta").mode("overwrite").saveAsTable("bronze_orders")
print(f"bronze_orders rows: {raw.count()}")
