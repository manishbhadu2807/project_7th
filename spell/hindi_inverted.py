
import numpy as np
import nltk
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

suffixes = {
    1: ["ो", "े", "ू", "ु", "ी", "ि", "ा"],
    2: ["कर", "ाओ", "िए", "ाई", "ाए", "ने", "नी", "ना", "ते", "ीं", "ती", "ता", "ाँ", "ां", "ों", "ें"],
    3: ["ाकर", "ाइए", "ाईं", "ाया", "ेगी", "ेगा", "ोगी", "ोगे", "ाने", "ाना", "ाते", "ाती", "ाता", "तीं", "ाओं", "ाएं", "ुओं", "ुएं", "ुआं"],
    4: ["ाएगी", "ाएगा", "ाओगी", "ाओगे", "एंगी", "ेंगी", "एंगे", "ेंगे", "ूंगी", "ूंगा", "ातीं", "नाओं", "नाएं", "ताओं", "ताएं", "ियाँ", "ियों", "ियां"],
    5: ["ाएंगी", "ाएंगे", "ाऊंगी", "ाऊंगा", "ाइयाँ", "ाइयों", "ाइयां"],
}

def stem(word):
    for L in 5, 4, 3, 2, 1:
        if len(word) > L + 1:
            for suf in suffixes[L]:
                if word.endswith(suf):
                    return word[:-L]
    return word
def remove_stopWords(hindi):
    words = word_tokenize(hindi)
    stop_words = set(stopwords.words('hindi'))
    
    filteredtext=[]
    for word in words:
        word = word.lower()
        
        if word.endswith('-'):
            word = word.split('-')[0]
        if word.startswith('-'):
                word = word.split('-')[1]
        if word not in stop_words:
            if re.match('\d+',word) is None and re.match('[,.;\':\\(\\)-\\[\\]]',word) is None and len(word)>1:
            
                filteredtext.append(word)
    return filteredtext
def take_input( ):
    idx=0
    file=open('sim.txt','r')
    worksheet = file.read ().split("\n")
	# print(worksheet)
    hindi=[]
    for row in worksheet:
        hindi.append(row)
        idx+=1
    print(idx)
    return hindi
if __name__== "__main__":
    token_file = open("inverted_index_hindi.txt","w+")
    hindi=take_input( )
    inverted_index=dict( )
    for idx in range(0,len(hindi)):
        hindi[idx]=remove_stopWords(hindi[idx])
        for word1 in hindi[idx]:
            if word1 not in inverted_index:
                    inverted_index[word1]=[]
                    inverted_index[word1].append(idx)
            elif inverted_index[word1][-1]!=idx:
                inverted_index[word1].append(idx)
    print(inverted_index)
    for key in inverted_index:
        entry=inverted_index[key]
        token_file.write(key+" : ")
        for x in entry:
            token_file.write(str(x))
            if(x==entry[-1]):
                token_file.write("\n")
            else:
                token_file.write(",")


