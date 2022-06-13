# Quick and dirty solution to reformat vocabulary list.

import re

new_vocab_list = []
new_item = []
with open('vocabulary.txt', 'r', encoding='utf8') as vocab:
    vocab_list = vocab.readlines()
    for i in range(0, len(vocab_list)):
        vocab_list[i] = vocab_list[i].rstrip('\r\n')
    for i in range(0, len(vocab_list)):
        new_vocab_list.append(re.findall('[A-Z][^A-Z]*', vocab_list[i]))
    for list in new_vocab_list:
        for item in list:
            new_item.append(item.split(" - "))
    for i in range(0,len(new_item)):
        for j in range(0,len(new_item[i])):
            new_item[i][j] = new_item[i][j].strip()
            new_item[i][j] = new_item[i][j].strip(',')

with open('cleaned_vocab.txt', 'wb') as newvocab:
    newline = '\n'
    for list in new_item:
        counter = 0
        if 3 < len(list[0]):
            for item in list:
                if counter == 1:
                    newvocab.write(newline.encode('utf8'))
                newvocab.write(item.encode('utf8'))
                counter = 1
            newvocab.write(newline.encode('utf8'))

with open('cleaned_vocab.txt', 'r', encoding='utf8') as vocab:
    vocab_list = vocab.readlines()
    vocab_list = [x.strip() for x in vocab_list]

vocab = []

for i in range(0, len(vocab_list)):
    if i != len(vocab_list)-1:
        if i % 2 == 0:
            tuple = (vocab_list[i], vocab_list[i+1])
            vocab.append(tuple)








