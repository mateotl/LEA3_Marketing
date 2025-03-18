print("hola")
### Santiago
print("adios")

import pandas as pd

df_read = 'https://raw.githubusercontent.com/mateotl/LEA3_Seminario/6c97255963fc9d1f001fb3e74aaaef7762cbc2cf/aug_test.csv'
df = pd.read_csv(df_read, sep = ',')

df.head()