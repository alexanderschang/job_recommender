import re
from collections import Counter
import math
import numpy as np
import pandas as pd
import operator
import json
from cosine_similarity import CosineSimilarity

# Import job description data
#df = pd.read_csv('cleaned_data.csv')


def get_recommendations(resume, jobs_df):
    score_dict = {}

    for index, row in jobs_df.iterrows():
        # CosineSimilarity.cosine_similarity_of
        score_dict[index] = CosineSimilarity.cosine_similarity_of(
            row['description_cleaned'], resume)

    # Sort descriptions by score and index
    sorted_scores = sorted(score_dict.items(),
                           key=operator.itemgetter(1),
                           reverse=True)
    counter = 0

    # Create results data frame
    resultDF = pd.DataFrame(
        columns=['Job Index', 'Company', 'Title', 'Location', 'Description', 'Job Description'])  # , 'score'])

    # Get highest scored 5 jobs
    for i in sorted_scores:
        # print index & score of the job description
        resultDF = resultDF.append({'Description': jobs_df.iloc[i[0]]['job_description'],
                                    'Title': jobs_df.iloc[i[0]]['title'],
                                    'Company': jobs_df.iloc[i[0]]['company_name'],
                                    'Location': jobs_df.iloc[i[0]]['location'],
                                    'Job Index': jobs_df.iloc[i[0]]['Unnamed: 0']},
                                   ignore_index=True)
        # 'score': i[1]}, ignore_index=True)
        counter += 1

        if counter > 10:
            break

    json_result = json.dumps(resultDF.to_dict('records'))
    # return json_result

    # resultDF.to_csv('recs.csv')

    resultDF.fillna('', inplace=True)
    print(resultDF.head())
    return resultDF


def top_n_jobs(json_string):
    jobList = json.loads(json_string)
    result = []
    max_val = len(jobList)

    i = 0
    while i < max_val:
        result.append(jobList[i]['company'])
        i += 1

    return result


# top10_result = get_recommendations(cleaned_resume)
# company_names = top_5_jobs(top5_result)

# print(top10_result)
