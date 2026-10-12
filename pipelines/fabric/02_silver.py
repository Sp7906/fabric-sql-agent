# Fabric notebook 2: Silver - clean, type, de-duplicate, validate.
from pyspark.sql import functions as F

df = spark.table("bronze_orders")

silver = (df
    .dropDuplicates(["order_id"])
    .withColumn("order_date", F.to_date("order_date"))
    .withColumn("quantity", F.col("quantity").cast("int"))
    .withColumn("unit_price", F.col("unit_price").cast("double"))
    .withColumn("revenue", F.round(F.col("quantity") * F.col("unit_price"), 2))
    .filter(F.col("order_id").isNotNull() & (F.col("quantity") > 0))
)

bad = df.count() - silver.count()
print(f"Rejected {bad} rows during cleaning")
silver.write.format("delta").mode("overwrite").saveAsTable("silver_orders")
