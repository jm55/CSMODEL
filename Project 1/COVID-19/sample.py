#importing libraries
import numpy as np
import pandas as pd
print("libraries imported...")

#importing csv into dataframe
covid_df = pd.read_csv('covid_july_15.csv')
#print("covid_df info:")
#covid_df.info()
print("")
#deleting columns
#source: https://pythonexamples.org/pandas-dataframe-delete-column/
covid_df = covid_df.drop(columns=['new_cases_smoothed','new_deaths_smoothed','total_cases_per_million','new_cases_per_million','new_cases_smoothed_per_million'
                                  ,'total_deaths_per_million','new_deaths_per_million','new_deaths_smoothed_per_million','reproduction_rate','icu_patients'
                                  ,'icu_patients_per_million','hosp_patients','hosp_patients_per_million','weekly_icu_admissions','weekly_icu_admissions_per_million'
                                  ,'weekly_hosp_admissions_per_million','female_smokers','male_smokers','excess_mortality','median_age','aged_65_older','aged_70_older'
                                  ,'handwashing_facilities','hospital_beds_per_thousand','population_density','median_age','total_vaccinations_per_hundred'
                                  ,'people_vaccinated_per_hundred','people_fully_vaccinated_per_hundred','new_vaccinations_smoothed_per_million'])
print("revised covid_df info:")
covid_df.info() #rechecking changes

#remove entries that contain OWID as it is a commulative equivalent of every country on every continent
#owid_list = covid_df['iso_code'].str.contains('OWID') #conditional
#covid_df.drop(covid_df.index[covid_df['iso_code'].str.contains('OWID')=='True'],inplace=True)
covid_df.shape
    
