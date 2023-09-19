## original download site: https://health.data.ny.gov/api/views/tg3i-cinn/rows.csv?accessType=DOWNLOAD

# import pandas as pd
# df = pd.read_csv("All_Payer_Hospital_Inpatient_Discharges_by_Facility__SPARCS_De-Identified___Beginning_2009.csv")
# df.to_parquet('./sparcs/sparcs_summary.parquet')
# ## Saving as parquet file brings down the file size from ~20mb to ~1mb 


import duckdb

db = duckdb.connect(database=':memory:', read_only=False)

## get random sample of 100 rows from sparcs/sparcs_summary.parquet and load into dataframe using duckdb

test = db.execute(
    """
        select * from parquet_scan('sparcs/sparcs_summary.parquet') limit 100
    """
).df()

test.columns


## group by Discharge Year and get a sum of Number of Discharges, and rename Discharge Year to year and Number of Discharges to discharges_sum
test2 = db.execute(
    """
        select "Discharge Year" as year, sum("Number of Discharges") as discharges_sum from parquet_scan('sparcs/sparcs_summary.parquet') group by "Discharge Year"
    """
).df()