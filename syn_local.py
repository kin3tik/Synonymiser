'''
Created on 17/11/2012

@author: James White
https://github.com/kin3tik/

Takes a text input from the user and returns it with
each word replaced by a synonym.

thesaurus used:
http://www.gutenberg.org/dirs/etext02/mthes10.zip
'''
import os.path
import pickle
import random
import re

#thesaurus file path
file_path = "mthesaur.txt"

def import_thesaurus(file_path):
    #check for pickled thesaurus
    if os.path.isfile("thes.p"):
        thes = pickle.load(open( "thes.p", "rb" ))
    else:
        #if a pickled thesaurus doesn't exist, create one
        thes = dict()
        file = open(file_path,'r')
        for line in file:
            #for every line (contains a word and its synonyms),
            #split the line at its delim, assign the first word as key,
            #and the synonyms as the value (in a list)
            line_list = line.split(',')
            key = line_list.pop(0)
            value = line_list
            #remove the trailing new line character from the last word
            value[-1] = value[-1].rstrip('\n')
            thes[key] = value
        
        #pickle thesaurus
        pickle.dump(thes, open( "thes.p", "wb" ))
        
    return thes

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

#import a thesaurus from original txt file or pickle file
thes = import_thesaurus(file_path)

#keep prompting and processing until user terminates
while True:
    #text to 'synonymise'
    text = input(">> ")
    processed_text = process(text)
    result = synonymise(processed_text, thes)
    #pretty print the result
    print(''.join(result)+'\n')

