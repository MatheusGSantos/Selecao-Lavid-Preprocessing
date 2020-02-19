import re


def string_dir_swap(sentence, matches, out_f):
    """Compose and write all the possible strings containing the pattern.
    Arguments:
        sentence {string}
        matches {list of matches to pattern}
        out_f {output file}
    """
    for each_element in matches:
        start = ''
        end = ''
        for j in range(4): # first and last S or P
            for k in range(1,4): # first 1, 2 or 3
                for l in range(1,4): # last 1, 2 or 3
                    if j<2: # first S or P
                        start = 'S'
                    else:
                        start = 'P'
                    if j % 2: # last S or P
                        end = 'P'
                    else:
                        end = 'S'
                    start = str(k)+start+'_'
                    end = '_'+str(l)+end
                    final_ver = sentence[ : each_element.span()[0]-3 ] + start + sentence[ each_element.span()[0] : each_element.span()[1] ] + end + sentence[ each_element.span()[1]+3:]
                    out_f.write(final_ver)

                


output = open("output.txt", 'w')

with open("corpus-q3.csv", 'r') as input_file:
    next(input_file) # skip first row
    file_text = (line for line in input_file) # creates a generator to iterate over input_file lines
    for each_sentence in file_text:
        matches = list(re.finditer(r'(?<=(1|2|3)(S|P)_)[A-Z_]+R(?=_(1|2|3)(S|P))',each_sentence)) # find directional pattern matches
        string_dir_swap(each_sentence,matches,output)

output.close()