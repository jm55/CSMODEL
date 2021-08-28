#Cluster.py

import pip
import time
import pandas as pd

from cluster import KMeans
#params: 1,10,300,main_df

#call cluster.train()

main_df = pd.read_csv('Dataset2.csv')
print(main_df.info())

cluster = KMeans(3,1,10,300,main_df)
cluster.train(main_df,300)