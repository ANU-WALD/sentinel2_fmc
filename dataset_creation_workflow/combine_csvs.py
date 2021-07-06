import pandas as pd

combined_csv = pd.concat([pd.read_csv(f"modis_reflectances_s{i}.csv") for i in [1,2,3,4,5,6,8,9,10]])
combined_csv.to_csv( "modis_reflectances.csv", index=False, encoding='utf-8-sig')
