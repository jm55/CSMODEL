#CSMODEL: COVID-19 Dataset
#Crunches all country data into a world equivalent

#LIBRARIES
import numpy as np
import pandas as pd
print("LIBRARIES LOADED\n")

#GLOBAL VARIABLES
checkpoint = False
NaN = float("nan")
group_pop = 0 #Placeholder for the population of group of nations specified.

#CUSTOM FUNCTIONS
def add(dst, src): #Used in map(), adding source to destination
    if(type(dst) == str or type(src) == str):
        return -1
    return dst + src
def sortbydate(df): #Sorts and returns a given DataFrame on the 'date' column using MergeSort.
    date_values = df['date'].unique()
    date_values = np.sort(date_values,kind='mergesort')
    return date_values
def fillZeros(size): #Returns a list of zeros from a specified size
    return np.zeros(size).tolist()
def writeCheckpoint(df, filename): #Writes a given DataFrame to a CSV file
    if(checkpoint):
        df.to_csv(filename+".csv",index=False)
        print("Checkpoint Complete:",filename)
def aggregator(src_df,iso_code,continent,location): #Aggregates the given DataFrame to a grouped version
    tmp_df = pd.DataFrame(columns=raw_cols)
    for i in range(dateCount):
        sp_date = date_values[i] #Specified date
        filtered_df = src_df[src_df['date']==sp_date] #Series of nations with specified date
        observations = filtered_df.shape[0]
        if(observations != 0): #Will run only if there is atleast 1 observation
            id = [iso_code,continent,location,sp_date] #Default identifiers for ASEAN
            data = fillZeros(len(raw_dataCol))
            for j in range(observations):
                #add current data with the retrieved data
                retrieve = filtered_df[raw_dataCol].iloc[j]
                retrieve = retrieve.to_numpy()
                data = list(map(add,retrieve,data))
            #Make values in average if they are based on trends (Keyword: new, per_xxxx)
            #0-4 = iso_code,continent,location,date; equated to id
            #5-16 = available for aggregation
            data[1] = data[1]/observations #new_cases
            data[2] = data[2]/observations #new_cases_smoothed
            data[4] = data[4]/observations #new_deaths
            data[5] = data[5]/observations #new deaths smoothed
            data[6] = data[6]/observations #total_cases_per_million
            data[7] = data[7]/observations #new_cases_per_million
            data[8] = data[8]/observations #new_cases_smoothed_per_million
            data[9] = data[9]/observations #total_deaths_per_million
            data[10] = data[10]/observations #new_deaths_per_million
            data[11] = data[11]/observations #new_deaths_smoothed_per_million
            #...
            #35-43 = available for aggregation
            data[30] = data[30]/observations #total_vaccinations
            data[31] = data[31]/observations #people_vaccinated
            data[32] = data[32]/observations #people_fully_vaccinated
            data[33] = data[33]/observations #new_vaccinations
            data[34] = data[34]/observations #new_cases_smoothed
            data[35] = data[35]/observations #total_vaccinations_per_hundred
            data[36] = data[36]/observations #people_vaccinated_per_hundred
            data[37] = data[37]/observations #people_fully_vaccinated_per_hundred
            data[38] = data[38]/observations #new_vaccinations_smoothed_per_million	
            #45 = population
            data[40] = group_pop #population of group of nations
            result = id+data
            tmp_df.loc[tmp_df.shape[0]] = result #"ADDS" THE RESULTING LIST AT THE END OF THE DATAFRAME
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

#COLUMN FLAGS
raw_cols = covid_df.columns.tolist() #ALL COLUMNS AVAILABLE
identifiers = ['iso_code','continent','location','date'] #BASIC COUNTRY IDENTIFYING COLUMNS
raw_dataCol = list(set(raw_cols)-set(identifiers)) #DATA ONLY COLUMNS; https://stackoverflow.com/a/3428547
#COLUMNS TO BE REMOVED
toDrop = ['new_cases_smoothed','new_deaths_smoothed','total_cases_per_million','new_cases_per_million','new_cases_smoothed_per_million'
          ,'total_deaths_per_million','new_deaths_per_million','new_deaths_smoothed_per_million','reproduction_rate','icu_patients'
          ,'icu_patients_per_million','hosp_patients','hosp_patients_per_million','weekly_icu_admissions','weekly_icu_admissions_per_million'
          ,'weekly_hosp_admissions_per_million','female_smokers','male_smokers','excess_mortality','median_age','aged_65_older','aged_70_older'
          ,'handwashing_facilities','hospital_beds_per_thousand','population_density','median_age','total_vaccinations_per_hundred'
          ,'people_vaccinated_per_hundred','people_fully_vaccinated_per_hundred','new_vaccinations_smoothed_per_million'
          ,'new_vaccinations_smoothed','extreme_poverty','cardiovasc_death_rate','diabetes_prevalence', 'weekly_hosp_admissions'
          ,'new_tests','total_tests','total_tests_per_thousand','new_tests_per_thousand','new_tests_smoothed'
          ,'new_tests_smoothed_per_thousand','tests_per_case','tests_units','positive_rate','life_expectancy','human_development_index']
#COLUMNS TO RETAIN
toRetain = ['total_cases','new_cases','total_deaths','new_deaths','total_vaccinations',
                'people_vaccinated','people_fully_vaccinated','new_vaccinations','stringency_index',
                'population','gdp_per_capita']
#LIST OF ONLY DATA THAT CAN BE USED IN A COLLECTIVE MANNER (AS USED BY OWID ITSELF)
forCollective = ['total_cases','new_cases','new_cases_smoothed','total_deaths','new_deaths','new_deaths_smoothed','total_cases_per_million'
                ,'new_cases_per_million','new_cases_smoothed_per_million','total_deaths_per_million','new_deaths_per_million','new_deaths_smoothed_per_million','total_vaccinations'
                ,'people_vaccinated','people_fully_vaccinated','new_vaccinations','new_vaccinations_smoothed','total_vaccinations_per_hundred','people_vaccinated_per_hundred'
                ,'people_fully_vaccinated_per_hundred','new_vaccinations_smoothed_per_million','population']

#FILTERING COUNTRIES
ph_df = covid_df[covid_df['iso_code']=='PHL'] #PH ONLY
world_df = covid_df[covid_df['iso_code'].str.contains('OWID_WRL')] #OVERALL WORLD DATA
covid_df = covid_df[covid_df['iso_code'].str.contains('PHL|BRN|KHM|IDN|SGP|LAO|THA|MYS|MMR|VNM',regex=True)] #ASEAN NATIONS; YOU CAN CHANGE LIST OF COUNTRIES TO FOCUS

#TODO: FIND A WAY TO HAVE THE group_df FILLED WITH POPULATION DATA ON ALL ASEAN NATIONS (WHETHER PH IS INCLUDED OR NOT)
group_pop = 0

#DATA CLEANUP: NaN->0
for i in range(0,len(raw_dataCol),1):
    covid_df.loc[covid_df[raw_dataCol[i]].isnull(),raw_dataCol[i]]=0
print(covid_df.isnull().any())

#READING CONENTS OF EACH OBSERVATION AVAILABLE OF ALL COUNTRIES AVAILABLE ON A GIVEN DATE 
#NOT THE MOST EFFICIENT ALGO AS IT RUNS AT O(n*m)
#WILL MAKE USE OF THE CURRENT LIST OF COUNTRIES AVAILABLE AT covid_df.
group_df = aggregator(covid_df,"MDL_SEA",NaN,"Asia") #Will hold the resulting aggregation of ASEAN countries
print("AGGREGATING ASEAN COUNTRIES...")

#ASEAN Checkpoint
writeCheckpoint(group_df,"asean_checkpoint.csv")

#merge with covid_df
covid_df = pd.concat([group_df, covid_df, world_df])
covid_df = sortbydate(covid_df) #resort by date
print(covid_df["iso_code"].unique())

print("\n\nSCRIPT COMPLETE")