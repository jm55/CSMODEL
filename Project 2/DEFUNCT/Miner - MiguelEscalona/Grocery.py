import pip
import pandas as pd
import time
import numpy as np

from script2_verbose import RuleMiner #Do change source file to which ever is faster if there exists as such
config = [85,0.6]
miner = RuleMiner(config[0],config[1]) #10x0.6 configuration as specied in the instructions
print('Miner Configuration:',config)

temp_df = pd.read_csv("groceries.csv", header=None) #Dataset3 as chosen by the group
values = temp_df.values.ravel()
values = [value for value in pd.unique(values) if not pd.isnull(value)]
value_dict = {}
for i, value in enumerate(values):
    value_dict[value] = i
temp_df = temp_df.stack().map(value_dict).unstack()
baskets = []
for i in range(temp_df.shape[0]):
    basket = np.sort([int(x) for x in temp_df.iloc[i].values.tolist() if str(x) != 'nan'])
    baskets.append(basket)
main_df = pd.DataFrame([[0 for _ in range(169)] for _ in range(9835)], columns=values)
for i, basket in enumerate(baskets):
    main_df.iloc[i, basket] = 1
    
start = time.time()
rules = miner.get_association_rules(main_df) #Calling actual miner function 
duration = (time.time()-start)/60
print('Apriori Data Mining Completed!')

#Turns list into dataframe of items divided into two (A and B)
left_rules = []
right_rules = []
for i in range(len(rules)):
    for j in range(len(rules[i])):
        left_rules.append(', '.join(rules[i][j][0]))
        right_rules.append(', '.join(rules[i][j][1]))

#Turns aggregated lists into DFs and removes duplicates
rules_DF = pd.DataFrame({'A':left_rules,'B':right_rules})
rules_DF.drop_duplicates(inplace=True)
#rules_DF.sort_values(by='A', ascending=False, inplace=True)

#Saving DF as .csv file
filename = 'groceries_result.csv'
rules_DF.to_csv(filename)
print('Rules file saved as:', filename)
print('Time taken in mining:{:.2f}mins'.format(duration))
print('=====================================')