import os
import re
import pickle
import json
import nltk
import nltk.classify.util
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

lang_files = []

def read_from_reference_corpus():
	for filename in os.listdir("./europarl/txt"):
		lang_files.append(filename)

	lang_data = dict()
	i = "en"
	#for i in lang_files:
	if(i=="en"):
		dir_name = "./europarl/txt/" + i
		lang_data[i] = list()
		m = 0
		for filename in os.listdir(dir_name):
			lang_fname = dir_name + "/" + filename
			with open(lang_fname,'r',encoding = 'utf-8') as f:
				output = f.readlines()
				data_in = list()
				for line in output:
					line =  re.sub(r'<.*?>$',"",line)
					if(line != "\n"):
						data_in.append(line.lower())
				data_in = ''.join(data_in)
				#output = re.sub(r'<.+?>','',output)
				lang_data[i].append(data_in)

		lang_data[i] = ''.join(lang_data[i])

	return lang_data

def counting_occurences(lang_data):
	word_occurence = dict()
	stopwords = nltk.corpus.stopwords.words('english')
	for keys in lang_data.keys():
		lang_data[keys] = lang_data[keys].split("\n")
		for line in lang_data[keys]:
			tokenizer = nltk.RegexpTokenizer('[a-zA-Z]\w+\'?\w*')
			tokens = tokenizer.tokenize(line)
			useful_words = [word for word in tokens if word not in stopwords]
			for i in range(len(useful_words)):
				#k = i+1
				if(useful_words[i] in word_occurence):
					word_occurence[useful_words[i]] += 1
				else:
					word_occurence[useful_words[i]] = 1

				'''if(k < len(useful_words)):
					s = useful_words[k-1] + ' ' + useful_words[k]
					if(s in word_occurence):
						word_occurence[s] += 1
					else:
						word_occurence[s] = 1 

				if(k+1 < len(useful_words)):
					p = useful_words[k-1] + ' ' + useful_words[k] + ' ' +useful_words[k+1]
					if(p in word_occurence):
						word_occurence[p] += 1
					else:
						word_occurence[p] = 1'''
			

	#List Object 
	word_occurence = sorted(word_occurence.items(),key=lambda kv:kv[1],reverse = True)
	return word_occurence

def rank_freq_data(word_occurence):
	word_ranking = dict()
	in_p = 0
	rank = 1
	value = 0
	for i in range(len(word_occurence)):
		keys = word_occurence[i][0]
		val = int(word_occurence[i][1])
		if(in_p==0):
			in_p = 1
			value = int(word_occurence[0][1])
		if(value>val):
			rank += 1
			value = val

		word_ranking[keys] = rank

	return word_ranking

lang_data = read_from_reference_corpus()

#Loading pickle file for once to use it further queries
#with open('ref_data.pickle','rb') as file:
	#lang_data = pickle.load(file)

word_occurence = counting_occurences(lang_data)
with open('ref_data.pickle','wb') as file:
	pickle.dump(word_occurence,file)

ranking_data = rank_freq_data(word_occurence)
print(ranking_data)

with open('ranked_dict_pic.pickle','wb') as file:
	pickle.dump(ranking_data,file)

with open('ranked_dict.txt','w') as file:
	file.write(json.dumps(ranking_data))


