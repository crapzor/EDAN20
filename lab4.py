import os
import operator


def get_files(directory, suffix):
    """
    Returns all the files in a folder ending with suffix
    Recursive version
    :param directory:
    :param suffix:
    :return: the list of file names
    """
    files = []
    for file in os.listdir(directory):
        path = directory + '/' + file
        if os.path.isdir(path):
            files += get_files(path, suffix)
        elif os.path.isfile(path) and file.endswith(suffix):
            files.append(path)
    return files


def read_sentences(file):
    """
    Creates a list of sentences from the corpus
    Each sentence is a string
    :param file:
    :return:
    """
    f = open(file).read().strip()
    sentences = f.split('\n\n')
    return sentences


def split_rows(sentences, column_names):
    """
    Creates a list of sentence where each sentence is a list of lines
    Each line is a dictionary of columns
    :param sentences:
    :param column_names:
    :return:
    """
    new_sentences = []
    root_values = ['0', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', '0', 'ROOT', '0', 'ROOT']
    start = [dict(zip(column_names, root_values))]
    for sentence in sentences:
        rows = sentence.split('\n')
        sentence = [dict(zip(column_names, row.split())) for row in rows if row[0] != '#']
        sentence = start + sentence
        new_sentences.append(sentence)
    return new_sentences


def save(file, formatted_corpus, column_names):
    f_out = open(file, 'w')
    for sentence in formatted_corpus:
        for row in sentence[1:]:
            # print(row, flush=True)
            for col in column_names[:-1]:
                if col in row:
                    f_out.write(row[col] + '\t')
                else:
                    f_out.write('_\t')
            col = column_names[-1]
            if col in row:
                f_out.write(row[col] + '\n')
            else:
                f_out.write('_\n')
        f_out.write('\n')
    f_out.close()


def find_pairs(formatted_corpus):
    tup_dict = {}
    for sentence in formatted_corpus:
        for word in sentence:
            if word["deprel"] == "SS":
                subject = word['form'].lower()
                idx = word['head']
                verb = sentence[int(idx)]
                verb = verb["form"].lower()
                if (subject, verb) in tup_dict:
                    tup_dict[(subject, verb)] += 1
                else:
                    tup_dict[(subject, verb)] = 1
    sorted_x = sorted(tup_dict.items(), key=operator.itemgetter(1))
    return sorted_x


def find_triplets(formatted_corpus):
    trip_dict = {}
    for sentence in formatted_corpus:
        for word in sentence:
            if word["deprel"] == "SS":
                for obj in sentence:
                    if obj["deprel"] == "OO" and word['head'] == obj['head']:
                        subject = word['form'].lower()
                        idx = word['head']
                        verb = sentence[int(idx)]
                        verb = verb["form"].lower()
                        ob = obj['form'].lower()
                        if (subject, verb, ob) in trip_dict:
                            trip_dict[(subject, verb, ob)] += 1
                        else:
                            trip_dict[(subject, verb, ob)] = 1
    sorted_x = sorted(trip_dict.items(), key=operator.itemgetter(1))
    return sorted_x


def find_pairs_u(formatted_corpus):
    tup_dict = {}
    for sentence in formatted_corpus:
        for word in sentence:
            if word["deprel"] == "nsubj":
                subject = word['form'].lower()
                for i in sentence:
                    if i['id'] == word['head']:
                        verb = i['form'].lower()
                if (subject, verb) in tup_dict:
                    tup_dict[(subject, verb)] += 1
                else:
                    tup_dict[(subject, verb)] = 1
    sorted_x = sorted(tup_dict.items(), key=operator.itemgetter(1))
    return sorted_x


def find_triplets_u(formatted_corpus):
    trip_dict = {}
    for sentence in formatted_corpus:
        for word in sentence:
            if word["deprel"] == "nsubj":
                for obj in sentence:
                    if obj["deprel"] == "obj" and word['head'] == obj['head']:
                        subject = word['form'].lower()
                        for i in sentence:
                            if i['id'] == word['head']:
                                verb = i['form'].lower()
                        ob = obj['form'].lower()
                        if (subject, verb, ob) in trip_dict:
                            trip_dict[(subject, verb, ob)] += 1
                        else:
                            trip_dict[(subject, verb, ob)] = 1
    sorted_x = sorted(trip_dict.items(), key=operator.itemgetter(1))
    return sorted_x

if __name__ == '__main__':
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']
    column_names_u = ['id', 'form', 'lemma', 'upostag', 'xpostag', 'feats', 'head', 'deprel', 'deps', 'misc']

    train_files = [
        'ud-treebanks-v2.2/UD_German-GSD/de_gsd-ud-train.conllu',
        'ud-treebanks-v2.2/UD_French-GSD/fr_gsd-ud-train.conllu',
        'ud-treebanks-v2.2/UD_Danish-DDT/da_ddt-ud-train.conllu']


    train_file = 'corpus/swedish_talbanken05_train.conll'
    # train_file = 'test_x'
    test_file = 'corpus/swedish_talbanken05_test_.conll'

    sentences = read_sentences(train_file)
    formatted_corpus = split_rows(sentences, column_names_2006)
    print(train_file, len(formatted_corpus))
    print(formatted_corpus[0])
    sorted_tup = find_pairs(formatted_corpus)
    print(sorted_tup[-5:])
    sorted_trip = find_triplets(formatted_corpus)
    print(sorted_trip[-5:])

    print('\n')
    for file in train_files:
        sentences = read_sentences(file)
        formatted_corpus = split_rows(sentences, column_names_u)
        #print(file, len(formatted_corpus))
        #print(formatted_corpus[0])
        print(find_pairs_u(formatted_corpus)[-5:])
        print(find_triplets_u(formatted_corpus)[-5:])
        print("==================================")
