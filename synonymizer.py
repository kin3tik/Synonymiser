'''
Created on 17/11/2012

@author: James White
https://github.com/kin3tik/

Takes a text input from the user and returns it with
each word replaced by a synonym.

thesaurus used:
http://www.gutenberg.org/dirs/etext02/mthes10.zip
'''
import random
import re

#thesaurus file path
file_path = "THESAURUS FILE PATH"
#text to 'synonymise'
text = input("Enter text to synonymise: ")

def import_thesaurus(file_path):
    d = dict()
    file = open(file_path,'r')
    for line in file:
        #for every line (contains a word and its synonyms),
        #split the line at its delim, assign the first word as key,
        #and the synonyms as the value (in a list)
        line_list = line.split(',')
        key = line_list[0]
        del line_list[0]
        value = line_list
        d[key] = value
    return d

def pick(word_list):
    #pick a random list item
    return random.choice(word_list)

def synonymise(word_list, thes):
    #build a list of synonyms in result from the given word_list
    result = list()
    for word in word_list:
        #for every word, replace it with its synonym (if one exists)
        l_word = word.lower()
        if l_word in thes:
            synonyms = thes[l_word]
            #randomly pick a possible synonym
            syn = pick(synonyms)
            result.append(syn)
        else:
            #if a synonym doesnt exist, just use the original word
            result.append(word)
    return result

def process(string):
    #splits a string using regex - splits into words, punctuation and whitespace
    result = re.findall(r"[\w']+|[\s.,!?;]", string)
    return result


thes = import_thesaurus(file_path)
processed_text = process(text)
result = synonymise(processed_text, thes)

print(''.join(result))

