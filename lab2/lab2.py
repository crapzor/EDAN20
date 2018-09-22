import sys
import regex as re
import math


text = """Tell-me, O muse, of that 0.2 ingenious hero who
travelled far and wide after he had sacked the famous
town of Troy. Peace out."""

#input: string of text
#out: list of tokens
def tokenize4(text):
    """uses the punctuation and symbols to break the text into words
    returns a list of words"""
    spaced_tokens = re.sub('([\p{S}\p{P}])', r' \1 ', text)
    one_token_per_line = re.sub('\s+', '\n', spaced_tokens)
    tokens = one_token_per_line.split()
    return tokens

#print(tokenize4(text))

#input: list of tokens
#out1: list(list(words)) a.k.a list of sentances
#out2: number of words in out1
def normalize(tokens):
    norm_list = list()
    words = list()
    words.append('<s>')
    word_sum = 1
    for i in range(len(tokens)):
        if tokens[i] == '.':
            if i == len(tokens) - 1:
                words.append('</s>')
                word_sum += 1
                norm_list.append(words)
            elif bool(re.match('\p{Lu}\p{L}+', tokens[i+1])):
                words.append('</s>')
                norm_list.append(words)
                words = list()
                words.append('<s>')
                word_sum += 2
        elif bool(re.match('\p{L}+', tokens[i])):
            words.append(tokens[i].lower())
            word_sum += 1

    return [norm_list, word_sum]

#[a,b] = normalize(tokenize4(text))

#input: normalize
#out: list of words
def concatenate(norm_list):
    con = []
    for sent in norm_list:
        con += sent
    return con

#print(concatenate(a))

#print(a)
#print(b)


def count_unigrams(words):
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency


def count_bigrams(words):
    bigrams = [tuple(words[inx:inx + 2])
               for inx in range(len(words) - 1)]
    frequencies = {}
    for bigram in bigrams:
        if bigram in frequencies:
            frequencies[bigram] += 1
        else:
            frequencies[bigram] = 1
    return frequencies


if __name__ == '__main__':
    #text = sys.stdin.read()
    text = open(sys.argv[1]).read()



    print('Unigram model')
    print('=====================================================')
    print('wi C(wi) #words P(wi)')
    print('=====================================================')

    tokens = tokenize4(text)
    words = concatenate(normalize(tokens)[0])
    frequency = count_unigrams(words)
    alla_ord = normalize(tokens)[1]

    #for word in sorted(frequency.keys(), key=frequency.get, reverse=True):
    #    alla_ord += frequency[word]
    #    print(word, '\t', frequency[word])

    #print(len(frequency.keys()))

    test = 'Det var en gång en katt som hette Nils.'
    tokens_test = tokenize4(test)
    t = concatenate(normalize(tokens_test)[0])

    prob_unigram = 1
    for i in t:
        if i in frequency:
            prob_unigram *= frequency[i]/alla_ord
            print(str(i) + ' ' + str(frequency[i]) + ' ' + str(alla_ord) + ' ' + str(frequency[i]/alla_ord))
    print('=====================================================')

    print('Prob. unigrams:   ' + str(prob_unigram))

    n = len(t)
    geometric_mean_probability = prob_unigram**(1/float(n))
    print('Geometric mean prob.: ' + str(geometric_mean_probability))

    # den riktiga formeln är -1/n*log2(geometric_mean_prob)
    entropy_rate = -(1/1)*math.log(geometric_mean_probability,2)
    print('Entropy rate:   ' + str(entropy_rate))

    perplexity = 2**entropy_rate
    print('Perplexity:    ' + str(perplexity))



#============================================================================================






    print('\n \n \n Bigram model')
    print('=====================================================')
    print('wi wi+1 Ci,i+1 C(i) P(wi+1|wi)')
    print('=====================================================')

    # dictionary of bigrams
    frequency_bigrams = count_bigrams(words)

    #for word in sorted(frequency.keys(), key=frequency.get, reverse=True):
    #    alla_ord += frequency[word]
    #    print(word, '\t', frequency[word])



    test2 = 'Det var en gång en katt som hette Nils.'
    tokens_test2 = tokenize4(test)
    t = concatenate(normalize(tokens_test2)[0])
    bigrams_t = count_bigrams(t)

    prob_bigram = 1
    for i in bigrams_t:
        if i in frequency_bigrams:
            prob_bigram *= frequency_bigrams[i]/frequency[i[0]]
            print(str(i) + ' ' + str(frequency_bigrams[i]) + ' ' + str(frequency[i[0]]) + ' ' + str(frequency_bigrams[i]/frequency[i[0]]))
        else:
            prob_bigram *= frequency[i[1]]/alla_ord
            print(str(i) + ' ' + str(0) + ' ' + str(frequency[i[0]]) + ' ' + str(0/frequency[i[0]]) + ' *backoff: ' + str(frequency[i[1]]/alla_ord))

    print('=====================================================')

    print('Prob. bigrams:   ' + str(prob_bigram))

    n = len(bigrams_t)
    geometric_mean_probability = prob_bigram**(1/float(n))
    print('Geometric mean prob.: ' + str(geometric_mean_probability))

    #den riktiga formeln är -1/n*log2(geometric_mean_prob)
    entropy_rate = -(1/1)*math.log(geometric_mean_probability,2)
    print('Entropy rate:   ' + str(entropy_rate))

    perplexity = 2**entropy_rate
    print('Perplexity:    ' + str(perplexity))

