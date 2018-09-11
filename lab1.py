import os
import sys
import regex as re
import pickle

def get_files(dir, suffix):
    files = []
    for file in os.listdir(dir):
        if file.endswith(suffix):
            files.append(file)
    return files


def find_words(file_name):
    text = open('Selma/' + file_name).read().lower()
    iterations = re.finditer(r'\p{L}+', text)
    return list(iterations)


def idx_of_words(file_name, all_words):
    iterations = find_words(file_name)
    for words in iterations:
        if words.group() in all_words:
            all_words[words.group()].append(words.start())
        else:
            all_words[words.group()] = [words.start()]



#def indexer(fn, all_words):
#    files = get_files(fn, '.txt')
#    print(files)
#    for f in files:



# Takes in a list and a string: the list contains words and their index, and the
# string contains a word to be searched if required
# returns: a dictionary (key = string of words , Value = list of indexes)
# of word is inserted then list of indexes will be returned
def indexer(words, word = None):
    idx = {}
    for i in words:
        if i.group() in idx:
           idx[i.group()].append(i.start())
        else:
            idx[i.group()] = [i.start()]
    if word in idx:
        return idx[word]
    else:
        return idx


def word_index(file_name):
    text = open(fn + '/' + file_name).read().lower()
    list1 = list(re.finditer('\p{L}+', text))
    return list1



def master_indexer(word=None):
    word_dict = {}  # {'file_name' : [0, 10, 23]}
    #word_dict[] = {}  #{'word' : {'file_name' : [0, 10, 23]}}
    all_files = get_files(fn, '.txt')  # list containing file names
    for file in all_files:  # loopas 2 ggr
        word_index2 = indexer(word_index(file))  # {'word' : [0, 10, 23]}
        for w in word_index2:
            #word_dict[w] = {}  # {'word' : {'file_name' : [0, 10, 23]}}
            if w in word_dict:
                word_dict[w][file] = word_index2[w]
            else:
                word_dict[w] = {}
                word_dict[w][file] = word_index2[w]

    if word in word_dict:
        return word_dict[word]
    else:
        return word_dict



all_words = {}
fn = sys.argv[1]
#files = get_files(fn, '.txt')
#print(files)

#idx_of_words(files[0], all_words)
#print(all_words['gjord'])
#print(all_words['uppklarnande'])
#print(all_words['stjärnor'])

print(master_indexer('nils'))


#master_indexer()