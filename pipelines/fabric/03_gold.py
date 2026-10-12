# Fabric notebook 3: Gold - star schema for analytics / Power BI semantic model.
from pyspark.sql import functions as F

s = spark.table("silver_orders")

(s.select("customer_id", "customer_name", "region", "segment").dropDuplicates(["customer_id"])
  .withColumnRenamed("customer_name", "name")
  .write.format("delta").mode("overwrite").saveAsTable("dim_customer"))

(s.select("product_id", F.col("product_name").alias("name"), "category", "unit_price")
  .dropDuplicates(["product_id"])
  .write.format("delta").mode("overwrite").saveAsTable("dim_product"))

(s.select("order_id", "order_date", "customer_id", "product_id", "quantity", "revenue")
  .write.format("delta").mode("overwrite").saveAsTable("fact_sales"))
