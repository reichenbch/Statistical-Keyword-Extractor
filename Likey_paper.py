import nltk
import nltk.classify.util
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re,pickle
import json


def read_from_test_corpus(filename):

	lang_data = dict()
	i = "en"
	'''for i in lang_files:
	if(i=="en"):
		#dir_name = "./europarl/txt/" + i
		lang_data[i] = list()
		m = 0
		for filename in os.listdir(dir_name):
			lang_fname = dir_name + "/" + filename'''
	output = filename.readlines()
	data_in = list()
	for line in output:
		line =  re.sub(r'<.*?>$',"",line)
		line = line.lower()
		if(line != "\n"):
			data_in.append(line)
	data_in = ''.join(data_in)
				#output = re.sub(r'<.+?>','',output)
	lang_data[i]= data_in


	return lang_data

def counting_occurences(lang_data):
	word_occurence = dict()
	n_grams = dict()

	
	stopwords = nltk.corpus.stopwords.words('english')
	for keys in lang_data.keys():
		lang_data[keys] = lang_data[keys].split("\n")
		for line in lang_data[keys]:
			tokenizer = nltk.RegexpTokenizer('[a-zA-Z]\w+\'?\w*')
			tokens = tokenizer.tokenize(line)
			useful_words = [word for word in tokens if word not in stopwords]
			for i in range(len(useful_words)):
				k = i+1
				if(useful_words[i] in word_occurence):
					word_occurence[useful_words[i]] += 1
				else:
					word_occurence[useful_words[i]] = 1

				if(k < len(useful_words)):
					s = useful_words[k-1] + ' ' + useful_words[k]
					if(s in n_grams):
						n_grams[s] += 1
						word_occurence[s] += 1
					else:
						n_grams[s] = 1
						word_occurence[s] = 1 

				if(k+1 < len(useful_words)):
					p = useful_words[k-1] + ' ' + useful_words[k] + ' ' +useful_words[k+1]
					if(p in n_grams):
						n_grams[p] += 1
						word_occurence[p] += 1
					else:
						n_grams[p] = 1
						word_occurence[p] = 1
			

	#List Object 
	word_occurence = sorted(word_occurence.items(),key=lambda kv:kv[1],reverse = True)
	return word_occurence,n_grams

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
		if(val<value):
			rank += 1
			value = val

		word_ranking[keys] = rank

	return word_ranking


#Maximum Rank is 3684
def get_rank_ngram(ranking_data):
	with open('ranked_dict_pic.pickle','rb') as file:
		rank_dict = pickle.load(file)

	ratio = dict()
	for keys in ranking_data:
		if(keys in rank_dict):
			rat = ranking_data[keys]/rank_dict[keys]
			rat = float("{0:.6f}".format(rat))
			ratio[keys] = rat
		else:
			rat = ranking_data[keys]/(3685)
			rat = float("{0:.6f}".format(rat))
			ratio[keys] = rat

			#print(keys,rat)


	ratio_values = sorted(ratio.items(),key=lambda kv:kv[1])
	valued_rank = dict()
	with open("out_val_list.txt","w") as file:
		for i in range(len(ratio_values)):
			#print(ratio_values[i][0],ratio_values[i][1])
			if(ratio_values[i][1] < 0.01) :#This value can be tuned
				valued_rank[ratio_values[i][0]] = ratio_values[i][1]
			
				file.write(ratio_values[i][0] + "\t\t\t")
				file.write(str(ratio_values[i][1]) + "\n")

	return valued_rank

'''def generate_ngrams(ranking_data,n_grams):
	ngram_phrase = dict()
	ngram_phrase[2] = []
	ngram_phrase[3] = []


	for key in n_grams:
		ngram_temp = key
		text = ngram_temp.split(" ")
		text_len = len(text)
		init_gram =  text[:-1]
		init_gram = ' '.join(init_gram)
		final_gram = text[1:]
		final_gram = ' '.join(final_gram)


		if((init_gram in ranking_data) and (final_gram in ranking_data)):
			ngram_phrase[text_len].append(ngram_temp)

	with open("likey_ngram.txt","w") as file :
		file.write(json.dumps(ngram_phrase))
	return ngram_phrase'''


#--------------------------------------------------------------------------------------------------------------------
file = open('turing-test.txt')
key_dict = read_from_test_corpus(file)

word_occurence , n_grams = counting_occurences(key_dict)

'''wordnet_lemma = WordNetLemmatizer()
lemma_word = dict()
for i in range(len(word_occurence)):
	key = word_occurence[i][0]
	lemma_key = wordnet_lemma.lemmatize(key)
	if(lemma_key in lemma_word):
		lemma_word[lemma_key] += word_occurence[i][1]
	else:
		lemma_word[lemma_key] = word_occurence[i][1]

with open("lemma-word.txt","w") as file:
	file.write(json.dumps(lemma_word))'''


ranking_data = rank_freq_data(word_occurence)
#print(ranking_data)
valued_rank = get_rank_ngram(ranking_data)
#features = generate_ngrams(valued_rank,n_grams)
with open("overrall_likey.txt","w") as file:
	file.write(json.dumps(valued_rank))
	#file.write(json.dumps(features))