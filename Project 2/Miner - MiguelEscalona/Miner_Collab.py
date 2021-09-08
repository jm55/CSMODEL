import pip
import pandas as pd
import time
import numpy as np

main_df = pd.read_csv('Dataset3.csv') #Dataset3 as chosen by the group
main_df.drop(columns='Unnamed: 0', inplace=True) #Dropping the first column which is named as 'Unnamed: 0'
main_df.info()

print('Rating Value Range For User 0:\n',main_df.value_counts(subset=['0']).sort_index())
print('\nMin={:.0f} and Max={:.0f}\n'.format(main_df.min().min(),main_df.max().max()))

movie_df = pd.read_csv('movie_ratings.csv')
movie_df.drop(columns='Unnamed: 0', inplace=True)
movie_df.drop_duplicates(subset='movie',inplace=True)
movie_df.sort_values(by='imdb',inplace=True,ascending=False)
movie_df['movie_year'] = movie_df.movie.map(str) +' ('+movie_df.year.map(str)+')' #https://stackoverflow.com/a/11858532
movie_df

main_df['row_mean'] = main_df.mean(axis=1)
main_df['votes'] = main_df.count(axis=1).to_list()
main_df['imdb'] = movie_df['imdb'].iloc[0:100].to_list() #adjusts it to 1-5
#main_df.sort_values(by='row_mean', inplace=True, ascending=False)
itemList = movie_df['movie_year'].to_list()
itemList = itemList[0:100] #limiting to row size
main_df.index = itemList
print(main_df['row_mean'])
print('')
print(main_df.info())
print('')

from Collab import CollaborativeFiltering #Do change source file to which ever is faster if there exists as such
k = 5
miner = CollaborativeFiltering(k)
print('Miner_Collab k value:', k)

filter_df = main_df.iloc[:,0:300]

n = 1 #filter_df.shape[0]
for i in range(n):
    item = filter_df.loc[itemList[i], :]
    drop_item = filter_df.drop(itemList[i])
    similar_items = miner.get_k_similar(drop_item, item)
    print('========================================')
    print('Item {:.0f}: {:}\n========================================\nSimilar Items:\n{:}\n========================================\n\n'.format(i,itemList[i],similar_items[1].nlargest(5).round(4)))