from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, DoubleType, IntegerType, StringType
import pandas as pd

spark = SparkSession.builder.getOrCreate()

def convert_csv_to_delta(path, col_types, table_name):
  
  def create_schema(col_types):
    struct = StructType()
    for col_name, type in col_types:
      struct.add(col_name, type)
    return struct
  
  schema = create_schema(col_types)
  
  def create_pd_dataframe(path, schema):
    df = pd.read_csv(path)
    return spark.createDataFrame(df, schema = schema)
    
  pdf = create_pd_dataframe(path, schema)
  
  def write_to_delta(spark_df, delta_table_name):
    spark_df.write.mode('overwrite').format('delta').saveAsTable(delta_table_name)
    
  write_to_delta(pdf, table_name)
  
  out = f"""The following tables were created:
          - {table_name}
       """
  
  print(out)
