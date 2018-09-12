import os
import sys
import regex as re
import math

fn = sys.argv[1]
# print(fn) # read from command prompt

# takes in string object of a directory
# returns list of files in directory
def files(fn, function=False):
    if os.path.exists(fn):  # if such path exist
        files = []
        for file_name in os.listdir(fn):    # for each file in the directory fn
            files.append(file_name)     # lista av all filer i Selma
        if function:
            return len(files)   # number of documents
        else:
            return files

#print(files(fn,True))

# takes in a file name
# returns list of all internal word-index pairs
def file_index(file_name , function = False):
    text = open(fn + '/' + file_name).read().lower()
    list1 = list(re.finditer('\p{L}+', text))
    if function:
        return len(list1) # total words in a document
    else:
        return list1

#print(word_index('test.txt',True))


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
            return len(idx[word]) # frequency of a specific word in a doc
        else:
            return idx[word]
    else:
        if function:
            return 0.0 # if word does not exist retunn 0 in function form
        else:
            return idx

#print(organized_indexer(file_index('test.txt'),'a',True))




#
def master_indexer(word = None, function=False):
    word_dict = {}  #{'file_name' : [0, 10, 23]}
    #word_dict[] = {}  #{'word' : {'file_name' : [0, 10, 23]}}
    all_files = files(fn) # list containing file names
    #print(all_files)
    for file in all_files: #loopas 2 ggr
        word_index2 = organized_indexer(file_index(file)) # {'word' : [0, 10, 23]}
        #print(word_index2)
        for w in word_index2:
            #word_dict[w] = {}
            if w in word_dict:
                word_dict[w][file] = word_index2[w]
            else:
                word_dict[w] = {}
                word_dict[w][file] = word_index2[w] # {'word' : {'file_name' : [0, 10, 23]}}

    if word in word_dict:
        if function:
            return len(word_dict[word])  # number of docs containing word w
        else:
            return word_dict[word]
    else:
        if function:
            return 0.0
        else:
            return word_dict

#print(master_indexer('samlar'))

#calculates the tf if a document contains no words return 0
def t_f(doc , word):
    words = file_index(doc, True) # all words in document doc
    if words == 0:
        return 0.0
    ordet = organized_indexer(file_index(doc), word, True) # frequency of a word
    return ordet/words

# print(t_f('test.txt','a'))

#calculates the idf, if no document contains word return 0
def i_df(word):#,documents):
    docs = files(fn,True) # total number of documents
    #print(docs)
    doc_containing_word = master_indexer(word,True)
    if doc_containing_word == 0:
        return 0.0
    #print(doc_containing_word)
    idf = math.log10((docs / doc_containing_word))
    return idf

#print(i_df('a') )



def tf_idf(docs, words):
    for doc in docs:
        print('\n' + doc)
        for w in words:
            tf = t_f(doc, w)
            idf = i_df(w)
            mul = tf*idf
            print(w + ' ' + str(mul))



documents = files(fn)
#print(documents)
words_to_process = ['känna', 'gås','nils', 'et']


tf_idf(documents , words_to_process)