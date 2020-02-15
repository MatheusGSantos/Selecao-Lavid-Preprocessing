def get_inner_words(string):
    """
    Return string without directional
    """
    return string[3:-3]


def verb_check(string):
    """
    Returns true if string contains a verb
    """
    string = string.split('_')
    for word in string:
        if word[-1] == 'R':
            return True    
    return False


# load possibilities
direcionais = open("direcionais.txt", 'r')
dire_lst = [l[:-1].split(',') for l in direcionais]
direcionais.close()

def string_filter_and_swap(sentence, filt_l, out_f):
    """Compose and write all the possible strings containing the pattern. Supports recursive calls for multiple ocurrences in the same sentence.
    
    Arguments:
        sentence {string}
        filt_l {list of strings that correspond to pattern}
        out_f {output file}
    """
    for each_element in filt_l:
        word = get_inner_words(each_element)
        if verb_check(word):
            for i in range(36): # 36 casos
                start = sentence.find(each_element) - 1
                end = len(each_element)+start+1
                sent = sentence[:start+1]+dire_lst[i][0]+'_'+word+'_'+dire_lst[i][1]+sentence[end:]
                if each_element == filt_l[len(filt_l)-1]:
                    output.write(sent)
                else:
                    string_filter_and_swap(sent, filt_l[1:], out_f)
                


output = open("output.txt", 'w')

with open("corpus-q3.csv", 'r') as input_file:
    next(input_file) # skip first row
    file_text = (line for line in input_file) # creates a generator to iterate over input_file lines
    for each_sentence in file_text:
        filtered = [x for x in each_sentence.split(' ') if x[0].isdigit()] # split in " " and get only the elements that start with a digit
        string_filter_and_swap(each_sentence,filtered,output)

output.close()