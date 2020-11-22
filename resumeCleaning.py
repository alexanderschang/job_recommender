import fitz
import re
import sys
import texthero as hero
from texthero import preprocessing
import pandas as pd


# Cleans text data from uploaded resume
def process_resume(doc):
    text = ""
    for page in doc:
        text = text + str(page.getText())

    # Split text by next line
    tx = " ".join(text.split('\n'))

    # Remove unnecessary punctuations
    cleaned_tx = re.sub(r'[§_|]', '', tx)

    # Remove/extract phone numbers
    pattern = re.compile(
        r'([+(]?\d+[)\-]?[ \t\r\f\v]*[(]?\d{2,}[()\-]?[ \t\r\f\v]*\d{2,}[()\-]?[ \t\r\f\v]*\d*[ \t\r\f\v]*\d*[ \t\r\f\v]*)')
    match = pattern.findall(cleaned_tx)
    match = [re.sub(r'[,.]', '', el) for el in match if
             len(re.sub(r'[()\-.,\s+]', '', el)) > 6]
    match = [re.sub(r'\D$', '', el).strip() for el in match]
    phoneNum_match = [el for el in match if len(re.sub(r'\D', '', el)) <= 15]
    phoneNum_match = ' '.join([str(elem) for elem in phoneNum_match])
    cleaned_tx = cleaned_tx.replace(phoneNum_match, '')

    # Get email
    email_pattern = re.compile(r'\S*@\S*')
    email_match = email_pattern.findall(cleaned_tx)
    email_match = ' '.join([str(elem) for elem in email_match])
    cleaned_tx = cleaned_tx.replace(email_match, '')

    # Further cleaning using texthero
    resume_df = pd.DataFrame([cleaned_tx], columns=['resume'])
    df2 = pd.DataFrame()

    custom_pipeline = [preprocessing.lowercase,
                       preprocessing.remove_digits,
                       preprocessing.remove_punctuation,
                       preprocessing.remove_diacritics,
                       preprocessing.remove_whitespace]
    # preprocessing.stem]

    df2['cleaned'] = hero.clean(resume_df['resume'],
                                pipeline=custom_pipeline)
    pd.set_option('max_colwidth', 100000)
    cleaned_resume = df2['cleaned'].to_string(index=False)

    return cleaned_resume
