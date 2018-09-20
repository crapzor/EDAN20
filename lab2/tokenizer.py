"""
Tokenizers
Usage: python tokenizer.py < corpus.txt
"""
__author__ = "Pierre Nugues"

import sys
import regex as re

text = """Tell me, O muse, of that ingenious hero who
travelled far and wide after he had sacked the famous
town of Troy. NOOOOOOO. Why."""


def tokenize(text):
    """uses the nonletters to break the text into words
    returns a list of words"""
    # words = re.split('[\s\-,;:!?.’\'«»()–...&‘’“”*—]+', text)
    # words = re.split('[^a-zåàâäæçéèêëîïôöœßùûüÿA-ZÅÀÂÄÆÇÉÈÊËÎÏÔÖŒÙÛÜŸ’\-]+', text)
    # words = re.split('\W+', text)
    words = re.split('\P{L}+', text)
    words.remove('')
    return words


def tokenize2(text):
    """uses the letters to break the text into words
    returns a list of words"""
    # words = re.findall('[a-zåàâäæçéèêëîïôöœßùûüÿA-ZÅÀÂÄÆÇÉÈÊËÎÏÔÖŒÙÛÜŸ’\-]+', text)
    # words = re.findall('\w+', text)
    words = re.findall('\p{L}+', text)
    return words


def tokenize3(text):
    """uses the punctuation and nonletters to break the text into words
    returns a list of words"""
    # text = re.sub('[^a-zåàâäæçéèêëîïôöœßùûüÿA-ZÅÀÂÄÆÇÉÈÊËÎÏÔÖŒÙÛÜŸ’'()\-,.?!:;]+', '\n', text)
    # text = re.sub('([,.?!:;)('-])', r'\n\1\n', text)
    text = re.sub(r'[^\p{L}\p{P}]+', '\n', text)
    text = re.sub(r'(\p{P})', r'\n\1\n', text)
    text = re.sub(r'\n+', '\n', text)
    return text.split()


def tokenize4(text):
    """uses the punctuation and symbols to break the text into words
    returns a list of words"""
    spaced_tokens = re.sub('([\p{S}\p{P}])', r' \1 ', text)
    one_token_per_line = re.sub('\s+', '\n', spaced_tokens)
    tokens = one_token_per_line.split()
    return tokens


def normalize(tokens):
    norm_list = list()
    words = list()
    words.append('<s>')
    for i in range(len(tokens)):
        if tokens[i] == '.':
            if i == len(tokens) - 1:
                words.append('</s>')
                norm_list.append(words)
            elif bool(re.match('\p{Lu}\p{L}+', tokens[i+1])):
                words.append('</s>')
                norm_list.append(words)
                words = list()
                words.append('<s>')
        elif bool(re.match('\p{L}+', tokens[i])):
            words.append(tokens[i].lower())
    return norm_list


if __name__ == '__main__':
    #text = sys.stdin.read()
    text = open(sys.argv[1]).read()
    #words = tokenize(text)
    #for word in words:
    #    print(word)
    #words = tokenize2(text)
    #print(words)
    #print('\n')
    #words = tokenize2(text)
    #print(words)
    words = tokenize4(text)
    norm_li = normalize(words)
    for i in range(5):
        conc = ' '.join(norm_li[i-5])
        print(conc)