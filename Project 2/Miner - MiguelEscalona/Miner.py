import pip
import pandas as pd
import time

"""
This script executes the necessary commands and functions
for apriori data mining of Dataset3.csv.

It was determined that the given dataset may take a huge amount
of time from the mining process, thus an automation script was created
in order to enable unsupervised data mining where the resulting 
association rules will just be outputed as a file specified below.

The file contents will come from the resulting association rules
which was then turned into a DataFrame. Duplicates from the DataFrame 
are then removed to make the resulting data more lean and easy to read.
The structure of the resulting DF are as follows:
        A           B
0   itemsetA0   itemsetB0
1   itemsetA1   itemsetB1
2   itemsetA2   itemsetB2

Refer to sample_result.csv for an example result which ran at a
DF configuration of 100 rows 5 columns.
"""

from script2_verbose import RuleMiner #Do change source file to which ever is faster if there exists as such
miner = RuleMiner(10,.6) #10x0.6 configuration as specied in the instructions

main_df = pd.read_csv('Dataset3.csv') #Dataset3 as chosen by the group
main_df.drop(columns='Unnamed: 0', inplace=True) #Dropping the first column which is named as 'Unnamed: 0'
main_df.fillna(0,inplace=True)

#Changing list of columns; Please refer to Jupyter Notebook for source of itemlist
#itemList is sorted by sales volumes, effectively indicating the most purchased items.
itemList = ['CARBONATED BEVERAGES','MILK','BEER/ALE/ALCOHOLIC CIDER','SALTY SNACKS','FRESH BREAD & ROLLS',
            'NATURAL CHEESE','WINE','COLD CEREAL','YOGURT','FZ DINNERS/ENTREES','COFFEE','BOTTLED WATER',
            'ICE CREAM/SHERBET','CRACKERS','RFG FRESH EGGS','RFG JUICES/DRINKS','BREAKFAST MEATS','COOKIES',
            'CIGARETTES','SOUP','RFG SALAD/COLESLAW','TOTAL CHOCOLATE CANDY','LUNCHEON MEATS','BOTTLED JUICES - SS',
            'TOILET TISSUE','SPIRITS/LIQUOR','DOG FOOD','FZ PIZZA','FZ NOVELTIES','FZ / RFG POULTRY','FZ SEAFOOD',
            'SNACK BARS/GRANOLA BARS','DINNER SAUSAGE','SPICES/SEASONINGS','VEGETABLES','CREAMS/CREAMERS',
            'LAUNDRY DETERGENT','SHORTENING & OIL','CAT FOOD','BABY FORMULA/ELECTROLYTES','RFG MEAT','PROCESSED CHEESE',
            'PAPER TOWELS','BUTTER/BUTTER BLENDS','SNACK NUTS/SEEDS/CORN NUTS','MEXICAN FOODS','PROCESSED FZ / RFG POULTRY',
            'PASTRY/DOUGHNUTS','FZ PLAIN VEGETABLES','RFG SIDE DISHES','FZ BREAKFAST FOOD','FRANKFURTERS',
            'TOTAL NON-CHOCOLATE CANDY','SPORTS DRINKS','SPAGHETTI/ITALIAN SAUCE','PASTA','PICKLES/RELISH/OLIVES',
            'FOOD & TRASH BAGS','CANNED/BOTTLED FRUIT','RICE','SEAFOOD -SS','FZ MEAT','NUT BUTTER',
            'TEA/COFFEE READY-TO-DRINK','SALAD DRESSINGS - SS','BAKING NEEDS','VITAMINS','DOUGH/BISCUIT DOUGH - RFG',
            'BAKERY SNACKS','CUPS & PLATES','DRY PACKAGED DINNERS','MAYONNAISE','SS DINNERS','SOAP','SS MEAT & RFG HAM',
            'ENERGY DRINKS','CREAM CHEESE/CR CHS SPREAD','TOMATO PRODUCTS','FZ POTATOES/ONIONS','PIES & CAKES',
            'WEIGHT CONTROL','MEXICAN SAUCE','ALL OTHER SAUCES','SUGAR','BAKING MIXES','DISH DETERGENT','MARGARINE/SPREADS',
            'RFG ENTREES','HOUSEHOLD CLEANER','JELLIES/JAMS/HONEY','FZ APPETIZERS/SNACK ROLLS','DIAPERS','LUNCHES - RFG',
            'COLD/ALLERGY/SINUS TABLETS','GRAVY/SAUCE MIXES','HOT CEREAL','INTERNAL ANALGESICS','TEA - BAGS/LOOSE',
            'SOUR CREAM','BABY FOOD','COTTAGE CHEESE','PET SUPPLIES','ASEPTIC JUICES','TOOTHPASTE','MUSTARD & KETCHUP',
            'RFG TEAS/COFFEE','CAT/DOG LITTER','SPREADS - RFG','FLOUR/MEAL','GUM','FZ BREAD/FZ DOUGH','SHAMPOO',
            'GASTROINTESTINAL - TABLETS','SANITARY NAPKINS/TAMPONS','DRIED FRUIT','FACIAL TISSUE','DEODORANT','BAKING NUTS',
            'FZ FRUIT','POPCORN/POPCORN OIL','RFG WHIPPED TOPPINGS','SYRUP/MOLASSES','ENGLISH MUFFINS','RFG DIPS','BATTERIES',
            'CANNED JUICES - SS','AIR FRESHENERS','SKIN CARE','FZ PIES','FOILS & WRAPS','BAKED BEANS/CANNED BREAD','BLADES',
            'CLEANING TOOLS/MOPS/BROOMS','DESSERTS - RFG','ASIAN FOOD','TOOTHBRUSH/DENTAL ACCESORIES','FZ DESSERTS/TOPPING',
            'DRY FRUIT SNACKS','GELATIN/PUDDING PRD AND MIXES','BARBEQUE SAUCE','MISC. SNACKS','DRY BEANS/VEGETABLES',
            'HAIR CONDITIONER','DRINK MIXES','TOASTER PASTRIES/TARTS','SEAFOOD - RFG','NON-FRUIT DRINKS - SS','CHARCOAL',
            'VINEGAR','MOIST TOWELETTES','LAUNDRY CARE','DRIED MEAT SNACKS','MOUTHWASH','SUGAR SUBSTITUTES',
            'EYE/CONTACT LENS CARE PRODUCT','OTHER RFG PRODUCTS','FZ POT PIES','CANDLES','FABRIC SOFTENER LIQUID',
            'PAPER NAPKINS','KITCHEN STORAGE','LIGHT BULBS','HAND & BODY LOTION','SALAD DRESSING - RFG',
            'EVAPORATED/CONDENSED MILK','ADULT INCONTINENCE','SALAD TOPPINGS','MILK FLAVORING/COCOA MIXES',
            'COLD/ALLERGY/SINUS LIQUIDS','COFFEE CREAMER - SS','INSTANT POTATOES','FROZEN & DRY ICE','HAIR COLORING',
            'BREADCRUMBS/BATTERS','FZ PASTA','FOIL PANS','SMOKELESS TOBACCO','PANCAKE MIXES','DESSERT TOPPINGS',
            'BAKED GOODS - RFG','PASTA - RFG','FZ SIDE DISHES','FIRST AID TREATMENT','BLEACH','FROSTING','JUICES - FROZEN',
            'FIRST AID ACCESSORIES','COSMETICS - EYE','SPONGES & SCOURING PADS','DIP/DIP MIXES - SS',
            'GASTROINTESTINAL - LIQUID','FABRIC SOFTENER SHEETS','HAIR STYLING GEL/MOUSSE','LIQUID DRINK ENHANCERS',
            'PIZZA - RFG','STUFFING MIXES','DISPOSABLE TABLEWARE','FZ PREPARED VEGETABLES','SUNTAN PRODUCTS',
            'PICKLES/RELISH - RFG','HOUSEHOLD CLEANER CLOTHS','RUG/UPHOLSTERY/FABRIC TREATMT','COSMETICS - FACIAL',
            'TEA - INSTANT TEA MIXES','FIRELOG/FIRESTARTER/FIREWOOD','PEST CONTROL','CROUTONS','STEAK/WORCESTERSHIRE SAUCE',
            'COUGH DROPS','COCKTAIL MIXES','HAIR SPRAY/SPRITZ','COSMETICS - NAIL','PREMIXED COCKTAILS/COOLERS',
            'BABY ACCESSORIES','HAIR ACCESSORIES','RICE/POPCORN CAKES','BABY NEEDS','MARSHMALLOWS','OFFICE PRODUCTS',
            'CHEESECAKES','FOOT CARE PRODUCTS','MISC HEALTH REMEDIES','NASAL PRODUCTS','LIP TREATMENT','COUGH SYRUP',
            'FEMININE NEEDS','SHAVING CREAM','COFFEE FILTERS','ALL OTHER BREAKFAST FOOD','COTTON BALLS/SWABS','SOCKS',
            'DENTURE PRODUCTS','SLEEPING REMEDIES','CIGARS','PIZZA PRODUCTS','OUTDOOR INSECT/RODENT CONTROL',
            'FZ CORN ON THE COB','RFG TORTLLA/EGGRLL/WONTN WRAP','COSMETIC - ACCESSORIES','CHILDRENS ART SUPPLIES',
            'SHAVING LOTION/MENS FRAGRANCE','ICE CREAM CONES/MIXES','GLOVES','LIGHTERS','WRITING INSTRUMENTS',
            'BOTTLES','COSMETICS - LIP','EXTERNAL ANALGESIC RUBS','RAZORS','OTHER FROZEN FOODS','SEXUAL HEALTH',
            'AUTOMOBILE FLUIDS/ANTIFREEZE','ANTI-SMOKING PRODUCTS','FLOOR CLEANERS/WAX REMOVERS','WATER SOFTENERS/TREATMENT',
            'MOTOR OIL','WATER FILTERS/DEVICES','CHARCOAL LIGHTER FLUIDS','FURNITURE POLISH','FAMILY PLANNING',
            'FRAGRANCES - WOMENS','HEMORRHOIDAL REMEDIES','BAKING CUPS/PAPER','POWDERED MILK','FRT & VEG PRESERVATIVE/PECTIN',
            'BATH PRODUCTS','OTHER GROOMING SUPPLIES','PANTYHOSE/NYLONS','OUTDOOR/LAWN FRTLZR/WDKLLR','HOME HEALTH CARE/KITS',
            'ALL OTHER TOBACCO PRODUCTS','HOUSEHOLD PLASTICS','BATH/BODY SCRUBBERS/MASSAGERS','SHOE POLISH & ACCESSORIES',
            'POOL/SPA CHEMICALS','TIGHTS','AUTOMOBILE WAXES/POLISHES','MEAT PIES','PERSONAL THERMOMETERS',
            'ELECTRONIC SMOKING DEVICES','FLASHLIGHTS','SMOKING ACCESSORIES','MISC HEALTH REMEDY TABLETS',
            'JUICE/DRINK CONCENTRATE - SS','MATCHES','PLAYING CARDS','HAIR GROWTH PRODUCTS','GLAZED FRUIT',
            'VACUUM BAGS/BELTS','HOUSEHOLD LUBRICANTS','HOME PERMANENT/RELAXER KITS','BREATH FRESHENER SPRAYS/DROPS',
            'COSMETIC STORAGE','PHOTOGRAPHY SUPPLIES','CLOTH DYE','LARD','TOOTHBRUSH HOLDERS','PRODUCE RINSE',
            'BLANK AUDIO/VIDEO MEDIA','FZ COFFEE CREAMER']
main_df.columns = itemList

print(main_df.info())

#used for testing main_df of different sizes
n = 15 #Limits the number of columns/products listed
main_df = main_df.iloc[:,0:n] #Comment this out to enable full main_df size.
print('trimmed main_df:',n)

#benchmarks:
#0.00 mins @ 5 items only
#0.02 mins @ 10 items only
#0.90 mins @ 15 items only
#3.60 mins @ 16 items only
#target: 300 items

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
filename = 'output.csv'
rules_DF.to_csv(filename)
print('Rules file saved as:', filename)
print('Time taken in mining:{:.2f}mins'.format(duration))
print('=====================================')