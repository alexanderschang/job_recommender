import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk import word_tokenize
from unidecode import unidecode
import string
import texthero as hero
from texthero import preprocessing

# Load & combine scraped data
df_ml = pd.read_csv('glassdoor_data/glassdoor_data_ML.csv')
df_pm = pd.read_csv('glassdoor_data/glassdoor_data_pm.csv')

df_swe = pd.read_csv(
    'glassdoor_data/glassdoor_data_swe.csv', encoding='latin1')
df_swe = df_swe.drop(columns='Unnamed: 0')

df_ds = pd.read_csv('glassdoor_data/glassdoor_data_ds.csv')
df_ds = df_ds.drop(columns='Unnamed: 0')

df_ibd = pd.read_csv('glassdoor_data/glassdoor_data_ibd.csv')

df_consult = pd.read_csv('glassdoor_data/glassdoor_data_consulting.csv')

df = pd.concat([df_ml, df_pm, df_swe, df_ds, df_ibd,
                df_consult], ignore_index=True)

# Drop duplicated descriptions
df = df.drop_duplicates(subset=['job_description', 'company_name'])

# Salary Parsing
salary = df['estimate_salary_range'].apply(lambda x: x.replace('$', ''))
salary = salary.apply(lambda x: x.replace('K', '000'))
df['estimate_salary_range'] = salary

df['min_salary_estimate'] = salary.apply(lambda x: x.split('-')[0])
df['max_salary_estimate'] = salary.apply(lambda x: int(x.split('-')[1]))

# Remove URLs from job descriptions
no_url = [re.sub(r'http\S+', '', str(description))
          for description in df['job_description']]
df['description_cleaned'] = no_url

# Data cleaning helper function


def pre_process(text):
    text = text.lower()
    stop_set = stopwords.words('english') + list(string.punctuation)
    text = " ".join([i for i in word_tokenize(text) if i not in stop_set])
    text = unidecode(text)

    # Remove URL's
    #test = [re.sub(r'http\S+', '', str(description)) for description in df['job_description']]

    return text


# Parse job descriptions
df['description_cleaned'] = df['description_cleaned'].apply(
    lambda x: pre_process(str(x)))

# Remove diacritics using texthero
#custom_pipeline = [preprocessing.remove_diacritics]
# df['description_cleaned'] = hero.clean(
#    df['description_cleaned'], pipeline=custom_pipeline)

df.to_csv('cleaned_data.csv')
