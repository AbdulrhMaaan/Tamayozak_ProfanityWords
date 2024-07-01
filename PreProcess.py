from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd
from scipy.stats import zscore
import re

import inflect
def Feature_Encoder(X,cols):
    for c in cols:
        lbl = LabelEncoder()
        lbl.fit(list(X[c].values))
        X[c] = lbl.transform(list(X[c].values))
    return X

def Feature_Scaling(X, a, b):
    X = np.array(X)
    Normalized_X = np.zeros((X.shape[0], X.shape[1]))
    for i in range(X.shape[1]):
        min_val = min(X[:, i])
        max_val = max(X[:, i])
        if min_val == max_val:  # Check if feature has zero variability
            Normalized_X[:, i] = a  # Assign a constant value if zero variability
        else:
            Normalized_X[:, i] = ((X[:, i] - min_val) / (max_val - min_val)) * (b - a) + a
    return Normalized_X

def delete_Row_Of_Missing_Values(rental_data):
    return rental_data.dropna();


def replace_Missing_Value_with_Mean(rental_data):
    return rental_data.fillna(rental_data.mean())

def Remove_Outliers(rental_data) :
    z_scores = zscore(rental_data)
    rental_data = pd.DataFrame(rental_data)
    # print(z_scores[100:][:]) # so max abs(zscore value) >2  so threshold 1.7 or 3
    threshold = 3
    outlier_indices = np.where(np.abs(z_scores) > threshold)[0]
    return rental_data.drop(index=outlier_indices)

# Test
#ob=LabelEncoder()
#ob.fit(["pp","pp","to","am","pp"])
#print(ob.classes_)
#print (ob.transform(["am","to","to","pp"]) )


#ARABIC LANGUAGE PREPROCESSING

def Arabic_normalize_chars(text):
    text = re.sub(r'[إأٱآا]', r'ا', text)
    text = re.sub(r"ى", r"ي", text)
    text = re.sub(r"ة", r"ه", text)
    text = re.sub(r"ؤ",r"ء",text)
    text = re.sub(r"ئ", r"ء", text)
    return text


#remove tashkeel from the text
def Arabic_remove_tashkeel(text):
    tashkeel_pattern = r'[\u064B-\u065F\u0610-\u061A\u0656-\u065F]'
    cleaned_text = re.sub(tashkeel_pattern, '', text)
    return cleaned_text


#REMOVE يا  from the beginning of the word
def Arabic_remove_Ya(text):
    prefix_to_remove = "يا"
    if text.startswith(prefix_to_remove):
        return text[len(prefix_to_remove):]
    else:
       return text

def Arabic_remove_AL(text):
    prefix_to_remove = "ال"
    if text.startswith(prefix_to_remove):
        return text[len(prefix_to_remove):]
    else:
       return text

def Arabic_remove_H(text):
    suffix_to_remove = "ه"
    if text.endswith(suffix_to_remove):
        return text[:-len(suffix_to_remove)]
    else:
        return text


#English LANGUAGE PREPROCESSING
# to make the word singular , return the word singular
def en_singularize_word(word):
    p = inflect.engine()
    singular_form = p.singular_noun(word)
    return singular_form if singular_form else word


#ENGLISH & ARABIC LANGUAGE PREPROCESSING
def en_ar_remove_punctuation(text):
    punctuation_pattern = r'[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]'
    # Remove 's from words
    text = re.sub(r"'s\b", '', text)
    # Use the re.sub() function to replace punctuation (except emojis) with a space
    cleaned_text = re.sub(punctuation_pattern, ' ', text)
    return cleaned_text




# remove repeating characters more than 1 times  pattern = r'(.)\1{this controled,}'
def en_ar_remove_repeating_characters(text):
    pattern = r'(.)\1{1,}'
    cleaned_text = re.sub(pattern, r'\1', text)
    return( cleaned_text)



# if sentence has a www. or http:// or https:// will return true
def has_url(text):
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.search(url_pattern, text) is not None  or re.search(r'www\.[^ ]+', text) is not  None

