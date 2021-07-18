#CSMODEL: COVID-19 Dataset
#Crunches all country data into a world equivalent

#just in case it is needed
import numpy as np
import pandas as pd
print("libraries loaded\n")

#custom functions
def add(dst, src):
    return dst + src
def overlap(identifier, drop, retain): #not used; https://stackoverflow.com/questions/1388818/how-can-i-compare-two-lists-in-python-and-return-matches
    return bool(set(identifier).intersection(drop) and set(identifier).intersection(retain) and set(drop).intesection(retain))

filename = input("Enter Filename of CSV file: ")

#prepare files both as file_obj and as df
covid_df = pd.read_csv(filename)
#Raw file reading: make use of covid_df.readline() to retrieve a str line (as str) from


date_values = covid_df['date'].unique()
date_values = np.sort(date_values,kind='mergesort')
dateCount = date_values.size
print("dateCount:",dateCount,"\n")
#print(date_values)

print("original shape:",covid_df.shape)

#COLUMN FLAGS
identifiers = ['iso_code','continent','location','date']
toDrop = ['new_cases_smoothed','new_deaths_smoothed','total_cases_per_million','new_cases_per_million','new_cases_smoothed_per_million'
          ,'total_deaths_per_million','new_deaths_per_million','new_deaths_smoothed_per_million','reproduction_rate','icu_patients'
          ,'icu_patients_per_million','hosp_patients','hosp_patients_per_million','weekly_icu_admissions','weekly_icu_admissions_per_million'
          ,'weekly_hosp_admissions_per_million','female_smokers','male_smokers','excess_mortality','median_age','aged_65_older','aged_70_older'
          ,'handwashing_facilities','hospital_beds_per_thousand','population_density','median_age','total_vaccinations_per_hundred'
          ,'people_vaccinated_per_hundred','people_fully_vaccinated_per_hundred','new_vaccinations_smoothed_per_million'
          ,'new_vaccinations_smoothed','extreme_poverty','cardiovasc_death_rate','diabetes_prevalence', 'weekly_hosp_admissions'
          ,'new_tests','total_tests','total_tests_per_thousand','new_tests_per_thousand','new_tests_smoothed'
          ,'new_tests_smoothed_per_thousand','tests_per_case','tests_units','positive_rate','life_expectancy','human_development_index']
toRetainData = ['total_cases','new_cases','total_deaths','new_deaths','total_vaccinations',
                'people_vaccinated','people_fully_vaccinated','new_vaccinations','stringency_index',
                'population','gdp_per_capita']

#data cleanup - column removal
covid_df = covid_df.drop(columns=toDrop)
covid_df.info()
print("curr shape (column removal):",covid_df.shape,"\n")

#data cleanup - nan->0; https://www.geeksforgeeks.org/python-pandas-dataframe-fillna-to-replace-null-values-in-dataframe/
for i in range(0,len(toRetainData),1):
    covid_df[toRetainData[i]].fillna(0,inplace=True)
covid_df['continent'].fillna('OWID',inplace=True)
print(covid_df.isnull().any())
covid_df.to_csv("drop_checkpoint.csv",index=False)
print("data cleaned")

#whitelisting: all observations that do not belong on the list are to be dropped
iso_code_whitelist = ['PHL','JPN','IDN','TWN','SGP','IND','OWID_WRL']
whitelisted = covid_df[covid_df['iso_code'].str.contains('PHL|JPN|IDN|TWN|SGP|IND|OWID_WRL',regex=True)]
whitelisted.sort_values(by=['date'])
whitelisted.to_csv("cleaned.csv")
#last part, assumes modifications have been made into df, save it as csv via:
    #df.to_csv('filename.csv')
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html
