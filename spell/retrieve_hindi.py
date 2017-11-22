
import numpy as np
import nltk
import re
import sys
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
    input_hindi=" "
    for x in hindi:
        input_hindi+=x
    return input_hindi
def lcs(str1,str2,i,j):
    if(i==len(str1) and j==len(str2)):
        return 0

    if(i==len(str1)):
        return len(str2) - j

    if (j == len(str2)):
        return len(str1) - i

    if (dp[i][j] !=-1):
        return dp[i][j]

    ans = sys.maxsize

    if(str1[i]==str2[j]):
        ans = lcs(str1,str2,i+1,j+1)

    ans = min(ans,1 + lcs(str1,str2,i+1,j))
    ans = min(ans,1 + lcs(str1,str2,i,j+1))
    ans = min(ans,1 + lcs(str1,str2,i+1,j+1))

    dp[i][j] = ans

    return ans
def Jacobian(a,b):
    return (len(list(set(a)&set(b)))*1.0/len(list(set(a)|set(b)))*1.0)
def boolean_retrieval(query,inverted_index):
    res = [x for x in range(2286)]
    for word in query:
        word = stem(word)
        if word in inverted_index:
            res = set(res) & set(inverted_index[word])
        else:
            res = []
        res = sorted(res)
    return res
def process(term,bigram):
    term = '$' + term.lower() + '$'
    print("herer\n")
    print(words)
    print("fvhh")
    possibilities = []
    set1 = []
    for i in range(1,len(term)):
        st = term[i-1] + term[i]
        set1.append(st)
        if(st  in bigram):
        	possibilities.extend(bigram[st])
    possibilities = set(possibilities)

    tmp = []

    for i in possibilities:
        word = words[i]
        set2 = []
        for j in range(len(word)-1):
            st = word[j] + word[j+1]
            set2.append(st)
        if(Jacobian(set1,set2)>=0.25):
            tmp.append(word)
    tmp = [x[1:-1] for x in tmp]
    if(len(tmp)<1):
        tmp.append(term[1:-1])
    #print(tmp)
    return tmp
def remove_stopWords(hindi):
	words = word_tokenize(hindi)
	stop_words = set(stopwords.words('hindi'))
	
	filteredtext=[]
	for word in words:
		word = word.lower()
		if '.-' in word:
			word1 = word.split('.-')[0]
			word2 = word.split('.-')[1]
			if (re.match('\d+',word1) is None and re.match('[,.;\':\\(\\)-\\[\\]]',word1) is None):
				filteredtext.append(word1)
			if (re.match('\d+',word2) is None and re.match('[,.;\':\\(\\)-\\[\\]]',word2) is None):
				filteredtext.append(word2)
		else:
			if word.endswith('-'):
				word = word.split('-')[0]
			if word.startswith('-'):
				word = word.split('-')[1]
			if re.match('\d+',word) is None and re.match('[,.;\':\\(\\)-\\[\\]]',word) is None:
				filteredtext.append(word)
	filteredtext=[word for word in filteredtext if word not in stop_words]
	return filteredtext
if __name__=="__main__":
    manish="jnsjn"
    words = []
    bigram = {}
    input_text=take_input( )
    words=remove_stopWords(input_text)
    words=['$' + word + '$' for word in words]
    # print(words)
    for idx,word in enumerate(words):
        if(len(word)<=2):
            continue
        for x in range(len(word)-1):
            st = word[x] + word[x+1]
            if st not in bigram:
                bigram[st] = [idx]
            else :
                if idx not in bigram[st]:
                    bigram[st].append(idx)
    print(bigram)
    file = open('query.txt','r+')
    query = []
    for line in file:
        line = line.split('\n')[0]
        query = line.split(' ')
    #print(query)
    query = [x.lower() for x in query]
    
    word_corrections = {}
    for term in query:
        print(term)
        possibilities = process(term,bigram)
        print(possibilities)
        r = len(term)
        closest = []
        dist = sys.maxsize
        for word in possibilities:
            str1 = term
            str2 = word
            c = len(word)
            dp = [[-1 for x in range(c)] for y in range(r)]
            if(lcs(str1,str2,0,0)<dist):
                dist = lcs(str1,str2,0,0)
                closest = [word]
            elif (lcs(str1,str2,0,0)==dist and word not in closest):
                closest.append(word)

        word_corrections[term] = closest
       
    print(word_corrections)
    corrected_query=[]
    output_file = open("OUT_hindi.txt","w+")
    output_file.write("correct_query: " )
    for key in query:
        value=word_corrections[key][0]
        output_file.write(str(value)+" ")
        corrected_query.append(value)

    print(corrected_query)
    output_file.write("\nrelated_doc: ")
    read = open('inverted_index_hindi.txt', 'r+')
    inverted_index = {}
    for line in read:
        token = line.split(' : ')[0]
        list = line.split(' : ')[1]
        list = list.split(',')
        inverted_index[token] = [int(x) for x in list]
    read.close()
    res=boolean_retrieval(corrected_query,inverted_index)
    for word in res:
    	output_file.write(str(word)+" ")
    output_file.close( )
    print(res)