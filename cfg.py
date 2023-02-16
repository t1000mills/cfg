from sys import argv
import re

ARR = '->'
SEMI = ';'
PIPE = '|'
EPS = ''


# parses doty syntax grammar in file at path and creates
# a list of rule lists in the format [[VAR,RHS],[VAR,RHS],...]
def parse_grammar(path):

    # open file, remove all whitespace, store each rule in list 
    f = open(path, 'r')
    file = f.read()
    file = re.sub(r'\s', '', file)
    file = file[:-1] # remove trailing semicolon before splitting
    gram = file.split(SEMI)

    # split rules at arrows
    rules = [[arg for arg in rule.split(ARR, 1)] for rule in gram]
    return rules


# open file at path containing string and remove trailing newline char
def parse_string(path):

    f = open(path, 'r')
    string = f.read()
    if string[-1] == '\n':
        string = string[:-1]
    return string


# return 1 if pattern found in right hand side of rule, 0 if not
def in_rhs(rule, pattern):
    terms = rule.split(PIPE)
    return 1 if (pattern in terms) else 0


# populate the table with variables for all substring lengths
def populate_table(rules, table, string, n):

    substr_len_1(rules, table, string, n)
    substr_len_geq_2(rules, table, n)
   
# process substrings of length 1
def substr_len_1(rules, table, string, n):
    i = 1
    while i <= n:                           # for each substring of length 1
        for rule in rules:
            if in_rhs(rule[1], string[i-1]):  # if symbol in rule
                table[i-1][i-1].append(rule[0]) # place var in table[i][i]
        i += 1

# process substrings >= 2
def substr_len_geq_2(rules, table, n):
    l = 2
    while l <= n:           # for each substr of length >= 2
        i = 1
        while i <= n-l+1:   # i is start pos of substr
            j = i+l-1       # j is end pos of the substr
            k = i           # k is split pos of the substr
            while k <= j-1:
                for rule in rules:
                    rhs = rule[1].split(PIPE)
                    for s in rhs:
                        if len(s) == 2:
                            if s[0] in table[i-1][k-1] and s[1] in table[k][j-1]:
                                if rule[0] not in table[i-1][j-1]:
                                    table[i-1][j-1].append(rule[0])
                k += 1
            i += 1
        l += 1



# return 0 if grammar in g_file recognizes string in s_file; otherwise return 1
def is_accepted(g_file, s_file):

    # get string from s_file
    string = parse_string(s_file)

    # parse the .cfg file
    rules = parse_grammar(g_file)

    # case of empty string
    if string == EPS:
        return 0 if in_rhs(rules[0][1], EPS) else 1
    
    # create an nxn table
    n = len(string)
    table = [[[] for x in range(n)] for x in range(n)]

    # fill the table with variables 
    populate_table(rules, table, string, n)

    # check if cell (0,n-1) contains start variable
    if rules[0][0] in table[0][n-1]:
        return 0
    else:
        return 1



if __name__ == '__main__':
    is_accepted(argv[1], argv[2])
