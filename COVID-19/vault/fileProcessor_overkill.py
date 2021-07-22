#CSMODEL: COVID-19 Dataset
#Crunches all country data into a world equivalent

#LIBRARIES
import numpy as np
import pandas as pd
import re
print("LIBRARIES LOADED")

#GLOBAL VARIABLES
checkpoint = True
NaN = float("nan")
group_pop = 0 #Placeholder for the population of group of nations specified.

#CUSTOM FUNCTIONS
def add(dst, src): #Used in map(), adding source to destination
    if(type(dst) == str or type(src) == str):
        return NaN
    return dst + src
def sortbydate(df): #Sorts and returns a given DataFrame on the 'date' column using MergeSort.
    date_values = df['date'].unique()
    date_values = np.sort(date_values,kind='mergesort')
    return date_values
def fillZeros(size): #Returns a list of zeros from a specified size
    return np.zeros(size).tolist()
def writeCheckpoint(df, filename): #Writes a given DataFrame to a CSV file
    if(checkpoint):
        print("WRITING CHECKPOINT...")
        df.to_csv(filename+".csv",index=False)
        print("Checkpoint Complete:",filename)
def aggregator(src_df,iso_code,continent,location,count): #Aggregates the given DataFrame to a grouped version
    tmp_df = pd.DataFrame(columns=toRetain) 
    for i in range(dateCount):
        sp_date = date_values[i] #Specified date
        filtered_df = src_df[src_df['date']==sp_date] #Series of nations with specified date
        observations = filtered_df.shape[0]
        if(observations == count): #Will run only if all countries listed are there
            id = [iso_code,continent,location,sp_date] #Default identifiers for ASEAN
            data = fillZeros(len(toRetainData))
            for j in range(observations):
                #add current data with the retrieved data
                retrieve = filtered_df[toRetainData].iloc[j].tolist()
                #print(retrieve)
                data = list(map(lambda x,y:x+y,retrieve,data))
            #Make values in average if they are based on trends (Keyword: new, per_xxxx)
            #0-3 = iso_code,continent,location,date; equated to id
            data[1] = data[1]/observations #new cases
            data[3] = data[3]/observations #new deaths
            data[6] = data[6]/observations #new_vaccinations
            data[8] = data[8]/observations #stringency_index
            data[9] = group_pop #population
            data[10] = data[10]/observations #gdp_per_capita
            result = id+data
            tmp_df.loc[tmp_df.shape[0]] = result #"ADDS" THE RESULTING LIST AT THE END OF THE DATAFRAME
    return tmp_df
def dateRange(df): #Finds the lowest and highest date recorded.
    date_values = df['date'].unique()
    date_values = np.sort(date_values,kind='mergesort')
    dateCount = date_values.size
    return [date_values[0], date_values[len(date_values)-1]] #the latest possible data maybe incomplete thus the day prior the latest will be used

#FILENAME INPUT
filename = input("Enter Filename of CSV file: ")

#PREPARE FILES AND RAW DATAFRAME
covid_df = pd.read_csv(filename)
#Raw file reading: make use of covid_df.readline() to retrieve a str line (as str) from

#DATE SORTING AND VALUES
date_values = sortbydate(covid_df)
dateCount = date_values.size

#COLUMNS TO RETAIN
toRetain = ['iso_code','continent','location','date','total_cases','new_cases','total_deaths','new_deaths','total_vaccinations','people_vaccinated','people_fully_vaccinated','new_vaccinations','stringency_index',
            'population','gdp_per_capita']
toRetainData = toRetain[4:]
print(toRetainData)
identifiers = toRetain[0:4]
#LIST OF ONLY DATA THAT CAN BE USED IN A COLLECTIVE MANNER (AS USED BY OWID ITSELF)
forCollective = ['total_cases','new_cases','new_cases_smoothed','total_deaths','new_deaths','new_deaths_smoothed','total_cases_per_million'
                ,'new_cases_per_million','new_cases_smoothed_per_million','total_deaths_per_million','new_deaths_per_million','new_deaths_smoothed_per_million','total_vaccinations'
                ,'people_vaccinated','people_fully_vaccinated','new_vaccinations','new_vaccinations_smoothed','total_vaccinations_per_hundred','people_vaccinated_per_hundred'
                ,'people_fully_vaccinated_per_hundred','new_vaccinations_smoothed_per_million','population']
targetCountries = ['PHL','BRN','KHM','IDN','SGP','LAO','THA','MYS','MMR','VNM'] #CHANGE CHOICES FOR TARGET COUNTRIES TO GROUP

#COLUMN FLAGS
raw_cols = covid_df.columns.tolist() #ALL COLUMNS AVAILABLE
raw_dataCol = list(set(raw_cols)-set(identifiers)) #DATA ONLY COLUMNS

#DROP COLUMNS
print("DROPPING COLUMNS...")
toDrop = identifiers.copy()
toDrop = list(set(covid_df.columns.tolist()) - set(toRetain))
covid_df = covid_df.drop(columns=toDrop)

#FILTERING COUNTRIES
print("FILTERING COUNTRIES...")
ph_df = covid_df[covid_df['iso_code']=='PHL'] #PH ONLY
world_df = covid_df[covid_df['iso_code'].str.contains('OWID_WRL')] #OVERALL WORLD DATA BY OWID
covid_df = covid_df[covid_df['iso_code'].str.contains(re.compile('|'.join(targetCountries)),regex=True)] #ASEAN NATIONS; YOU CAN CHANGE LIST OF COUNTRIES TO FOCUS

#FIND TOTAL POPULATION OF ASEAN
pop = covid_df[covid_df['date']==dateRange(covid_df)[1]]
if(pop.shape[0] != len(targetCountries)): #REFERENCES TO targetCountries
    print("COUNTRIES!=",len(targetCountries),"AT MAX DATE!")
    exit()
group_pop = pop['population'].sum()

#DATA CLEANUP: NaN->0
print("DATA CLEANUP (NaN->0)...")
for i in range(0,len(toRetain),1):
    covid_df.loc[covid_df[toRetain[i]].isnull(),toRetain[i]]=0

#READING CONENTS OF EACH OBSERVATION AVAILABLE OF ALL COUNTRIES AVAILABLE ON A GIVEN DATE 
#NOT THE MOST EFFICIENT ALGO AS IT RUNS AT O(n*m)
#WILL MAKE USE OF THE CURRENT LIST OF COUNTRIES AVAILABLE AT covid_df.
print("AGGREGATING ASEAN COUNTRIES...")
group_df = aggregator(covid_df,"MDL_SEA",NaN,"Asia",len(targetCountries)) #Will hold the resulting aggregation of ASEAN countries

#ASEAN Checkpoint
writeCheckpoint(group_df,"asean_checkpoint")

#COMBINING ALL SUBDATAFRAMES TO covid_df
print("COMBINING DATAFRAMES...")
covid_df = pd.concat([group_df, covid_df, world_df])
sortbydate(covid_df) #resort by date
print(covid_df['iso_code'].unique())

print("FILE PROCESSING COMPLETE")