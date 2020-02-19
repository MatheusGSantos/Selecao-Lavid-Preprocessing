from collections import Counter
import re
import json


c = Counter() # dict like data structure, but presumably faster for this situation


with open("corpus-q2.csv", 'r') as input_file:
    next(input_file) # skip first row
    file_text = (line for line in input_file) # creates a generator to iterate over input_file lines
    for each_sentence in file_text: # for each line/sentence
        # check for incorrect spaces between '_'
        while True:
            ocurrence = each_sentence.find(" _")
            if ocurrence == -1:
                break
            else:
                each_sentence = each_sentence[:ocurrence]+each_sentence[ocurrence+1:] # removes the " "

        list_sentence = re.split(r'\W+',each_sentence)

        # count word
        for elem in list_sentence:
            if len(elem) > 1 and not elem[0].isdigit(): # non-digit
                c[elem.lower()] += 1 # count
            else:
                if elem not in ['A','E','O']: # not A, E, O
                    continue    # ignore it
                c[elem.lower()] += 1 # count otherwise


with open("words.json", 'w', encoding="utf-8") as output:   # write to Json file
    json.dump(c, output, ensure_ascii=False, indent=4)
