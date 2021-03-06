from gensim import corpora
import numpy as np
import nltk
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import defaultdict
from pprint import pprint
from gensim import corpora, models, similarities
import sys
suffixes = {
    1: ["ो", "े", "ू", "ु", "ी", "ि", "ा"],
    2: ["कर", "ाओ", "िए", "ाई", "ाए", "ने", "नी", "ना", "ते", "ीं", "ती", "ता", "ाँ", "ां", "ों", "ें"],
    3: ["ाकर", "ाइए", "ाईं", "ाया", "ेगी", "ेगा", "ोगी", "ोगे", "ाने", "ाना", "ाते", "ाती", "ाता", "तीं", "ाओं", "ाएं", "ुओं", "ुएं", "ुआं"],
    4: ["ाएगी", "ाएगा", "ाओगी", "ाओगे", "एंगी", "ेंगी", "एंगे", "ेंगे", "ूंगी", "ूंगा", "ातीं", "नाओं", "नाएं", "ताओं", "ताएं", "ियाँ", "ियों", "ियां"],
    5: ["ाएंगी", "ाएंगे", "ाऊंगी", "ाऊंगा", "ाइयाँ", "ाइयों", "ाइयां"],
}
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
def lcs(str1,str2,i,j,dp):
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
        ans = lcs(str1,str2,i+1,j+1,dp)

    ans = min(ans,1 + lcs(str1,str2,i+1,j,dp))
    ans = min(ans,1 + lcs(str1,str2,i,j+1,dp))
    ans = min(ans,1 + lcs(str1,str2,i+1,j+1,dp))

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
def process(term,bigram,words):
    term = '$' + term.lower() + '$'
    
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
def stem(word):
    for L in 5, 4, 3, 2, 1:
        if len(word) > L + 1:
            for suf in suffixes[L]:
                if word.endswith(suf):
                    return word[:-L]
    return word
def spellcorrection( line ):
	words = []
	bigram = {}
	input_text=take_input( )
	words=remove_stopWords(input_text)
	words=['$' + word + '$' for word in words]
	for idx,word in enumerate(words):
		if(len(word)<2):
			continue
		for x in range(len(word)-1):
			st = word[x] + word[x+1]
			if st not in bigram:
				bigram[st] = [idx]
			else :
				if idx not in bigram[st]:
					bigram[st].append(idx)
	print(bigram)
	query = line.split(' ')
	query = [x.lower() for x in query]
	word_corrections = {}
	for term in query:
		print(term)
		possibilities = process(term,bigram,words)
		print(possibilities)
		r = len(term)
		closest = []
		dist = sys.maxsize
		for word in possibilities:
			str1 = term
			str2 = word
			c = len(word)
			dp = [[-1 for x in range(c)] for y in range(r)]
			if(lcs(str1,str2,0,0,dp)<dist):
				dist = lcs(str1,str2,0,0,dp)
				closest = [word]
			elif (lcs(str1,str2,0,0,dp)==dist and word not in closest):
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
	return value
def remove_stopWords(hindi):
	words = word_tokenize(hindi)
	stop_words = set(stopwords.words('hindi'))
	
	filteredtext=[]
	for word in words:
		word = word.lower()
		if '-' in word:
			word1 = word.split('-')[0]
			word2 = word.split('-')[1]
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
if __name__== "__main__":
	file = open("/home/manish/project/sim.txt","r")
	input=file.read( )
	hindi=input.split("\n")
	input_corpus=input.split("\n")
	# print(input_corpus[0])
	texts=[]
	print("..............................removing stop words and applying porter stemmer from the corpus................................................\n")
	for idx in range(0,len(hindi)):
		hindi[idx]=remove_stopWords(hindi[idx])
		texts.append([])
		for word in hindi[idx]:
			texts[idx].append(stem(word))
	frequency = defaultdict(int)
	for text in texts:
		for token in text:
			frequency[token] += 1
	texts = [[token for token in text if frequency[token] > 0]for text in texts]
	dictionary = corpora.Dictionary(texts)
	corpus = [dictionary.doc2bow(text) for text in texts]
	for text in texts:
		print(text)
	print(".........TfidfModel..........\n")
	tfidf = models.TfidfModel(corpus)
	print(tfidf)
	file.close( );
	
	print("\n.............................building lsi model ............................................\n")
	corpus_tfidf=tfidf[corpus]

	lsi = models.LdaModel(corpus, id2word=dictionary, num_topics=15)
	corpus_lsi = lsi[corpus_tfidf]
	print(lsi.print_topics())

	print("\n..............................reading input for file .....................................................\n")
	file=open("/home/manish/project/input.txt","r")
	qu=file.read( );
	print(qu)
	# qu="लैब में कब आ जा सकते हैं ?"
	print("\n..............................removing stop words and applying porter stemmer from the input................................................\n")
	qu=remove_stopWords(qu)
	print(qu)
	for i in range(0,len(qu)):
		if frequency[qu[i]] <=0:
			x=spellcorrection(qu[i])
			if x is not None:
				qu[i]=x;
	print(qu)

	print("\n..............................finding similarities.........................................\n")
	vec_bow = dictionary.doc2bow(qu)
	#print(new_vec)

	vec_lsi = lsi[vec_bow]

	index = similarities.MatrixSimilarity(lsi[corpus])

	sims = index[vec_lsi]

	print(list(enumerate(sims))) 
	sim=list(enumerate(sims))
	max=0;
	i=-1;
	count=0;
	for x in sim:
		if(x[1]>max):
			max=x[1]
			i=count;
		count+=1;
	# print(corpus)
	print("\nsentence: ["+input_corpus[i]+ "] is "+str(max*100) +" % similar") 
	# print(input_corpus[i])
	file.close( )
	file=open("query_sparql.txt","w")
	file.write("sentence: ["+input_corpus[i]+ "] is "+str(max*100) +" % similar\n")
	file.write(str(i))
	file.close()