import os
import sys
import regex as re
import math
import numpy

fn = sys.argv[1]


# print(fn) # read from command prompt

# takes in string object of a directory
# returns list of files in directory
def files(fn, function=False):
    if os.path.exists(fn):  # if such path exist
        files = []
        for file_name in os.listdir(fn):  # for each file in the directory fn
            files.append(file_name)  # lista av all filer i Selma
        if function:
            return len(files)  # number of documents
        else:
            return files




# takes in a file name
# returns list of all internal word-index pairs
def file_index(file_name, function=False):
    text = open(fn + '/' + file_name).read().lower()
    list1 = list(re.finditer('\p{L}+', text))
    if function:
        return len(list1)  # total words in a document
    else:
        return list1



#print(file_index('bannlyst.txt'))


# Takes in a list and a string: the list contains words and their index, and the
# string contains a word to be searched if required
# returns: a dictionary (key = string of words , Value = list of indexes)
# of word is inserted then list of indexes will be returned
def organized_indexer(words, word=None, function=False):
    idx = {}
    for i in words:
        if i.group() in idx:
            idx[i.group()].append(i.start())
        else:
            idx[i.group()] = [i.start()]
    if word in idx:
        if function:
            return len(idx[word])  # frequency of a specific word in a doc
        else:
            return idx[word]
    else:
        if function:
            return 0.0  # if word does not exist retunn 0 in function form
        else:
            return idx



#print(organized_indexer(file_index('bannlyst.txt',),'känna'))


#
def master_indexer(word=None):
    word_dict = {}  # {'file_name' : [0, 10, 23]}
    # word_dict[] = {}  #{'word' : {'file_name' : [0, 10, 23]}}
    all_files = files(fn)  # list containing file names
    # print(all_files)
    for file in all_files:  # loopas 2 ggr
        word_index2 = organized_indexer(file_index(file))  # {'word' : [0, 10, 23]}
        #print(word_index2)
        for w in word_index2:
            # word_dict[w] = {}
            if w in word_dict:
                word_dict[w][file] = word_index2[w]
            else:
                word_dict[w] = {}
                word_dict[w][file] = word_index2[w]  # {'word' : {'file_name' : [0, 10, 23]}}

    if word in word_dict:
        return word_dict[word]
    else:
       return word_dict


master_idx = master_indexer()

words = ['samlar','ände']

for i in words:
    print(i + ': ' + str(master_idx[i]))


#print(master_idx)



# calculates the tf if a document contains no words return 0

#def t_f(freq, words):
#    return freq / words

#print(t_f('bannlyst.txt', 'att'))

# print(t_f('test.txt','a'))

# calculates the idf, if no document contains word return 0
def i_df(word):  # ,documents):
    docs = files(fn, True)  # total number of documents
    #print(str(docs) + '\n')
    doc_containing_word = len(master_idx[word]) #master_indexer(word, True)
    #print(doc_containing_word)
    return math.log10(docs / doc_containing_word)

dict1 = {}
for i in master_idx.keys():
    dict1[i] = i_df(i)

#print(i_df('känna'))


def tf_idf(docs, words, function=False): #3 changes
    matrix = list()
    for doc in docs:
        doc_vector = list()
        all_words = file_index(doc, True)  # nbr of all words in document doc
        word_freq = organized_indexer(file_index(doc)) # len(word_frequency[word]) => frequency of a specific word in doc
        #print('\n' + doc) ### avkommentera
        for w in words:
            if w in word_freq:
                tf = len(word_freq[w])/all_words
            else:
                tf = 0.0

            idf = dict1[w]  #Byt tbx
            mul = tf * idf
            #print(w + ' ' + str(mul)) #avkommentera
            doc_vector.append(mul)
        matrix.append(doc_vector)
    if function:
        return matrix

#kommentera bort
#documents = ['bannlyst.txt', 'gosta.txt', 'herrgard.txt', 'jerusalem.txt', 'nils.txt']
#words_to_process = ['känna', 'gås', 'nils', 'et']
#tf_idf(documents, words_to_process)


documents = files(fn)
words_to_process = master_idx.keys()        # alla ord dvs nycklar från master indexer
grand_matrix = tf_idf(documents, words_to_process, True)

def cosine_similar_matrix(grand_matrix):
    similarity_matrix = list()
    for i in range(len(grand_matrix)):
        norm1 = numpy.linalg.norm(grand_matrix[i])
        doc_row = list()
        for j in range(len(grand_matrix)):
            dot_prod = numpy.dot(grand_matrix[i], grand_matrix[j])
            norm2 = numpy.linalg.norm(grand_matrix[j])
            product = dot_prod / (norm1 * norm2)
            doc_row.append(product)
        similarity_matrix.append(doc_row)
    return similarity_matrix


sim = cosine_similar_matrix(grand_matrix)
print(sim)


temp = 0
for i in range(9):
    for j in range(9):
        if i != j:
            if sim[i][j] > temp:
                temp = sim[i][j]
                row = i
                col = j



print('cosine value: ' + str(temp) + ' document 1: ' + str(documents[row]) + ' document 2: ' + str(documents[col]))

