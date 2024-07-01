# Description: This file contains functions to detect and clean offensive content from reviews
from profanity_check import predict
from PreProcess import *
import string
import os

"""
# List of predefined bad words (both English and Arabic)
bad_words = []
with open("Profan_Words.txt", 'r',encoding='utf-8') as file:
    content = file.read()
bad_words = content.split(",")
#print(bad_words)

#remove the " from the list
bad_words=[item.strip(" '") for item in bad_words]
#print(bad_words)
#print(len(bad_words))
#remove lastitem from list bad_words , to remove the /n string
#bad_words.pop()
#print(bad_words)
#print(len(bad_words))
"""

# Regular expression to detect Arabic letters
def detect_language_mix(sentence):
    arabic_pattern = re.compile(r'[\u0600-\u06FF]+')
    english_pattern = re.compile(r'[\u0020-\u007E]+')
    emoji_pattern = re.compile(r'[\U0001F300-\U0001F64F\U0001F600-\U0001F680\U00002600-\U000026FF]+')

    arabic_parts = []
    english_parts = []
    emoji_parts = []

    sentence_words = sentence.split()

    for word in sentence_words:
        contains_arabic = bool(arabic_pattern.search(word))
        contains_english = bool(english_pattern.search(word))
        contains_emoji = bool(emoji_pattern.search(word))

        if contains_arabic and contains_english:
            arabic_parts.append(' '.join(arabic_pattern.findall(word)))
            english_parts.append(' '.join(english_pattern.findall(word)))
        elif contains_english and contains_emoji:
            english_parts.append(' '.join(english_pattern.findall(word)))
            emoji_parts.append(' '.join(emoji_pattern.findall(word)))
        elif contains_arabic and contains_emoji:
            arabic_parts.append(' '.join(arabic_pattern.findall(word)))
            emoji_parts.append(' '.join(emoji_pattern.findall(word)))
        elif contains_arabic:
            arabic_parts.append(word)
        elif contains_emoji:
            if len(emoji_pattern.findall(word)[0]) >= 2:
                for emoji in emoji_pattern.findall(word)[0]:
                    emoji_parts.append(emoji)
            else:
                emoji_parts.append(word)
        elif contains_english:
            english_parts.append(word)




    return arabic_parts, english_parts, emoji_parts


#print(detect_language_mix(" تماااام   kk👹  كككك👹 😈 💩🖕  woow ازيكgood  ليهa7a   gg  طيب"))

#splitting file profen into 3 parts
"""
output_file_path=r"ar_profan_words.txt"
output_file=open(output_file_path, "w", encoding="utf-8")

output2_file_path = r"en_profan_words.txt"
output2_file= open(output2_file_path, "w", encoding="utf-8")


output3_file_path =r"emoji_profan_words.txt"
output3_file=open(output3_file_path, "w", encoding="utf-8")

output4_file_path =r"RESULLTTTT_profan_words.txt"
output4_file=open(output4_file_path, "w", encoding="utf-8")
ar_counter=0
en_counter=0
emji_counter=0
result_counter=0
for word in bad_words:
    if is_arabic(word):
        output_file.write("'" +word+"'"+",")
        ar_counter=ar_counter+1
    elif is_english(word):
        output2_file.write("'" +word+"'"+",")
        en_counter = en_counter + 1
    elif is_emoji(word):
        output3_file.write("'" +word+"'"+",")
        emji_counter = emji_counter + 1
    else :
        output4_file.write("'" +word+"'"+",")
        result_counter=result_counter + 1

print("DONEEEEEEE")
print(ar_counter+en_counter+result_counter+emji_counter)
print(ar_counter)
print(en_counter)
print(result_counter)
print(emji_counter)
print(len(bad_words))

"""
# Construct the absolute path to the file
file_path = os.path.join(os.path.dirname(__file__), 'ar_profan_words.txt')

# Initialize an empty list to store bad words
ar_bad_words = []

# Open the file using the absolute path
with open(file_path, 'r', encoding='utf-8') as file:
    # Read the content of the file
    content = file.read()
    # Split the content by commas
    ar_bad_words = [word.strip(" '") for word in content.split(",")]
#print(ar_bad_words)
#remove lastitem from list bad_words , to remove the /n string
#ar_bad_words.pop()
#print(ar_bad_words)
file_path = os.path.join(os.path.dirname(__file__), 'en_profan_words.txt')

# Initialize an empty list to store bad words
en_bad_words = []

# Open the file using the absolute path
with open(file_path, 'r', encoding='utf-8') as file:
    # Read the content of the file
    content = file.read()
    # Split the content by commas
    en_bad_words = [word.strip(" '") for word in content.split(",")]

#print(en_bad_words)
#remove lastitem from list bad_words , to remove the /n string
#en_bad_words.pop()
#print(en_bad_words)

# Construct the absolute path to the file
file_path = os.path.join(os.path.dirname(__file__), 'emoji_profan_words.txt')

# Initialize an empty list to store bad words
emoji_bad_words = []

# Open the file using the absolute path
with open(file_path, 'r', encoding='utf-8') as file:
    # Read the content of the file
    content = file.read()
    # Split the content by commas
    emoji_bad_words = [item.strip(" '") for item in content.split(",")]


#print(emoji_bad_words)
#remove lastitem from list bad_words , to remove the /n string
#emoji_bad_words.pop()
#print(emoji_bad_words)


def Offensive_Or_Not(review):
    offensive = False
    #print(len(words))
    ar_cleaned_words = []
    en_cleaned_words = []
    arabic_content = []
    english_content = []
    emoji_content = []

    arabic_content,english_content,emoji_content=detect_language_mix(review)

    # Detect URLs in the review
    if has_url(review):
        offensive = True

    #ASK IF MORE THAN ONE WORD IS OFFENSIVE
    separator = ' '
    if separator.join(arabic_content) in ar_bad_words or predict([separator.join(arabic_content)])[0] == 1 :
        offensive=True
    if separator.join(english_content) in en_bad_words or predict([separator.join(english_content)])[0] == 1 :
        offensive=True
    if separator.join(emoji_content) in emoji_bad_words or predict([separator.join(emoji_content)])[0] == 1 :
        offensive=True

    accumlative_ar_words=[]
    # Detect bad arabic words in the review
    for i,word in enumerate(arabic_content):
        if word in ar_bad_words or predict([word])[0] == 1:
            offensive =True
            break

        accumlative_ar_words.append(word)
        if separator.join(accumlative_ar_words) in ar_bad_words or predict([separator.join(accumlative_ar_words)])[0] == 1:
            offensive = True


        text=Arabic_remove_tashkeel(word)
        if text in ar_bad_words or predict([text])[0] == 1:
            offensive =True
            break

        text = Arabic_normalize_chars(text)
        if text in ar_bad_words or predict([text])[0] == 1:
            offensive =True
            break

        text = en_ar_remove_punctuation(text)
        if text in ar_bad_words or predict([text])[0] == 1:
            offensive = True
            break

        text = en_ar_remove_repeating_characters(text)
        if text in ar_bad_words or predict([text])[0] == 1:
            offensive = True
            break

        text = Arabic_remove_Ya(text)
        if text in ar_bad_words or predict([text])[0] == 1:
            offensive = True
            break

        text = Arabic_remove_H(text)
        if text in ar_bad_words or predict([text])[0] == 1:
            print(word, "  ", i, "  ", ar_bad_words[i])
            offensive = True
            break

        text = Arabic_remove_AL(text)
        if text in ar_bad_words or predict([text])[0] == 1:
            offensive = True
            break


        else:
            #continue
            ar_cleaned_words.append(text)
            # ASK IF MORE THAN ONE WORD IS OFFENSIVE after text is preproccessed
            separator = ' '
            if separator.join(ar_cleaned_words) in ar_bad_words or predict([separator.join(ar_cleaned_words)])[0] == 1:
                offensive = True


    accumlative_en_words=[]
    # Detect bad english words in the review
    for i,word in enumerate(english_content):
        if word in en_bad_words or predict([word])[0] == 1:
            offensive =True
            break

        # ASK IF MORE THAN ONE WORD IS OFFENSIVE before text is preproccessed word then 2 words then 3 words and so on
        accumlative_en_words.append(word)
        if separator.join(accumlative_en_words) in en_bad_words or predict([separator.join(accumlative_en_words)])[0] == 1:
            offensive = True

        text = word.lower()
        if text in en_bad_words or predict([text])[0] == 1:
            offensive =True
            break

        # remove punctuation
        text = en_ar_remove_punctuation(text)
        if text in en_bad_words or predict([text])[0] == 1:
            offensive =True
            break

        text = en_singularize_word(text)
        if text in en_bad_words or predict([text])[0] == 1:
            offensive = True
            break

        # remove repeating chars
        text = en_ar_remove_repeating_characters(text)
        if text in en_bad_words or predict([text])[0] == 1:
            offensive =True
            break



        else:
            en_cleaned_words.append(text)
            # ASK IF MORE THAN ONE WORD IS OFFENSIVE after text is preproccessed
            separator = ' '
            if separator.join(en_cleaned_words) in en_bad_words or predict([separator.join(en_cleaned_words)])[0] == 1:
                offensive = True



    for i, word in enumerate(emoji_content):
        if word in emoji_bad_words or predict([word])[0] == 1:
            offensive = True
            break
    #print(cleaned_review)
    if offensive:
        return "Offensive"
    else:
        return "Not Offensive"

# Example usage
#input_review = "This is a سييييئة محممممد  mohammmed  !!! ???? review with some badword2 words."
#input_review ="هذا المكان  very very beautiful"
#input_review ="هذا المكان  قحبة   و ممتاز جدا   ؟؟؟ very very beautiful"
#cleaned_review = Offensive_Or_Not(input_review)
#print("Original Review:", input_review)
#print("Cleaned Review:", cleaned_review)

""""
output_file_path = "newdata.txt"
# Write the combined term data to the text file with comma separators
with open(output_file_path, "r", encoding="utf-8") as output_file:
    data2=output_file.read().split("\n")

words=[]
for line in data2:
    if Offensive_Or_Not(line) =="Not Offensive":
        words.append(line)
"""

#words="💩🖕"
#words="armond rizzo"
#print(Offensive_Or_Not(words))