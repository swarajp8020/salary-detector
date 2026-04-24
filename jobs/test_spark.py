import os
import sys

os.environ["JAVA_HOME"]              = r"C:\Program Files\Java\jdk-11.0.31"
os.environ["PYSPARK_PYTHON"]        = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
os.environ["SPARK_LOCAL_IP"]        = "127.0.0.1"

from pyspark.sql import SparkSession

print("Creating session...")

spark = (
    SparkSession.builder
    .master("local[2]")
    .appName("SalaryDetectionMVP")
    .config("spark.ui.enabled",             "false")
    .config("spark.ui.showConsoleProgress", "false")
    .config("spark.sql.shuffle.partitions", "4")
    .config("spark.driver.memory",          "2g")
    .config("spark.driver.host",            "127.0.0.1")
    .config("spark.driver.bindAddress",     "127.0.0.1")
    .getOrCreate()
)

print(f"✅ Spark {spark.version} ready")

test_df = spark.createDataFrame([(1, "test")], ["id", "value"])
test_df.show()

spark.stop()
print("✅ Done")