from collections import Counter
import json


def check_spcase(string):
    """
    Returns true if the string is a digit(single digit or first 2 at least) or a single consonant
    """
    if ( (len(string) == 1) and (string not in 'AEIOU') or (string.isdigit() ) or ( string[:2].isdigit() ) ):
        return True
    else:
        return False


skippable_chars = ",:; \\()[]{}…+-.º\n" # string containing each character that doesn't 
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

        for sep in skippable_chars[1:]: # for each separator in skippable_chars string, execept the first one
            each_sentence = each_sentence.replace(sep,skippable_chars[0])   # replace the current character with the first character (,)
        list_sentence = [word for word in each_sentence.split(skippable_chars[0]) if word] # each_sentence is almost a list of actual words

        # count word
        for elem in list_sentence:
            if check_spcase(elem):
                continue    # ignore it
            else:              
                c[elem.lower()] += 1 # count

with open('words.json', "w", encoding='utf-8') as output:   # write to Json file
    json.dump(c, output, ensure_ascii=False, indent=4)
