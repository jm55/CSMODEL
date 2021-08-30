import pip
import pandas as pd
import time

from Collab import CollaborativeFiltering #Do change source file to which ever is faster if there exists as such
k = 5
miner = CollaborativeFiltering(k) #10x0.6 configuration as specied in the instructions
print('Miner_Collab Config:', k)
main_df = pd.read_csv('Dataset3.csv') #Dataset3 as chosen by the group
main_df.drop(columns='Unnamed: 0', inplace=True) #Dropping the first column which is named as 'Unnamed: 0'
main_df.fillna(0,inplace=True)

#Changing list of columns; Please refer to Jupyter Notebook for source of itemlist
#itemList is sorted by sales volumes, effectively indicating the most purchased items.
itemList = ['Game of Thrones','Band Brothers','Breaking Bad','Planet Earth','The Wire','Rick and Morty','Avatar: Last Airbender','Sherlock','Firefly','Death Note','Dark Knight','True Detective','Fargo','Lord Rings: Return King','Arrested Development','Black Mirror','Stranger Things',': Fellowship Ring','Office','Rome','Inception','House Cards','Narcos','Westworld','Six Feet Under',': Two Towers','M.D.','Doctor Who','Its Always Sunny in Philadelphia','Dexter','Daredevil','Better Call Saul','Sen to Chihiro no kamikakushi','Cidade de Deus','Mad Men','Sons Anarchy','Parks Recreation','Boardwalk Empire','Suits','Vikings','Interstellar','Mr. Robot','Punisher','La casa papel','Handmaids Tale','Gladiator','Memento','Pianist','Supernatural','Departed','Prestige','Community','Spartacus: Blood Sand','Intouchables','Hannibal','Whiplash','Mindhunter','Scrubs','24','Oldeuboi','Lost','Prison Break','Lives Others','WALL-E','Fringe','Modern Family','3 Idiots','Rises','Django Unchained','Coco','Snatch','Requiem for a Dream','Amiele','Eternal Sunshine Spotless Mind','Batman Begins','How I Met Your Mother','Californication','Inglourious Basterds','Up','Walking Dead','Toy Story ','Homeland','Jagten','Beautiful ','Der Untergang','Hauru ugoku shiro','V Vendetta','Big Bang Theory','Pans Labyrinth','There Will Be ','El secreto sus ojos','Warrior','Wolf Street','Inside Out','Room','Three Billboards Outside Ebbing','Missouri','Amores perros','Faa yeung nin wa','Monsters Inc.']
itemList = itemList[0:100] #limiting to entry size
main_df.index = itemList
print(main_df.info()) 

from Collab import CollaborativeFiltering #Do change source file to which ever is faster if there exists as such
k = 5
miner = CollaborativeFiltering(k) #10x0.6 configuration as specied in the instructions
print('Miner_Collab Config:', k)

print('========================================')
item = main_df.loc[itemList[0], :]
drop_item = main_df.drop(itemList[0])
similar_items = miner.get_k_similar(drop_item, item)
print('Item:{:}\nSimilar Items:\n{:}\n========================================'.format(itemList[0],similar_items[1].nlargest(5).round(4)))