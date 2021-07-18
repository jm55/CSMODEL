#CSMODEL: COVID-19 Dataset
#Crunches all country data into a world equivalent

#just in case it is needed
import numpy as np
import pandas as pd
print("libraries loaded\n")

#prepare files both as file_obj and as df
covid_df = pd.read_csv('covid_july_15.csv')
#Raw file reading: make use of covid_df.readline() to retrieve a str line (as str) from


date_values = covid_df['date'].unique()
date_values = np.sort(date_values,kind='mergesort')
dateCount = date_values.size
print("dateCount:",dateCount,"\n")
#print(date_values)

print("original shape:",covid_df.shape)

#data cleanup
covid_df = covid_df.drop(columns=['new_cases_smoothed','new_deaths_smoothed','total_cases_per_million','new_cases_per_million','new_cases_smoothed_per_million'
                                  ,'total_deaths_per_million','new_deaths_per_million','new_deaths_smoothed_per_million','reproduction_rate','icu_patients'
                                  ,'icu_patients_per_million','hosp_patients','hosp_patients_per_million','weekly_icu_admissions','weekly_icu_admissions_per_million'
                                  ,'weekly_hosp_admissions_per_million','female_smokers','male_smokers','excess_mortality','median_age','aged_65_older','aged_70_older'
                                  ,'handwashing_facilities','hospital_beds_per_thousand','population_density','median_age','total_vaccinations_per_hundred'
                                  ,'people_vaccinated_per_hundred','people_fully_vaccinated_per_hundred','new_vaccinations_smoothed_per_million'
                                  ,'new_vaccinations_smoothed','extreme_poverty','cardiovasc_death_rate','diabetes_prevalence', 'weekly_hosp_admissions'
                                  ,'new_tests','total_tests','total_tests_per_thousand','new_tests_per_thousand','new_tests_smoothed'
                                  ,'new_tests_smoothed_per_thousand','tests_per_case','tests_units','positive_rate'])
covid_df.info()
print("curr shape (column removal):",covid_df.shape,"\n")

#removing contents that contain 'OWID' on iso_code
owid = covid_df[covid_df['iso_code'].str.contains('OWID')]
covid_df = covid_df.drop(owid.index.tolist())
print("curr shape (OWID dropping):",covid_df.shape,"\n")
for i in range(dateCount): #reading contents given a specific date
    sp_date = date_values[i] #specified date
    filtered_df = covid_df[covid_df['date']==sp_date] #series of nations with specified date
    #print(filtered_df)
    observations = filtered_df.shape[0]
    #print("date: ",sp_date,", observations: ",observations)
    iso_code = 'WLD'
    continent = 'World'
    location = 'World'
    date = sp_date
    values = np.zeros((observations,13))
    for j in range(observations):
        
        

exit()
#last part, assumes modifications have been made into df, save it as csv via:
    #df.to_csv('filename.csv')
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html
