print("~~~Square Completer!~~~")
print("Enter the terms of your quadratic equation in standard form.")
print("Addition is implied, terms separated by spaces.")
print("Only use one kind of single-letter variable in the whole expression.")
print("Surround computations such as constant multiplication and fractions in parenthesis.\n")
print("DO NOT put variables inside parenthesis!\n")
user_in = input("> ")

# extract the variable
def extract_variable(expression):
    letters = [char for char in expression if char.isalpha()]
    if all(letter == letters[0] for letter in letters):
        return letters[0]
    else:
        raise ValueError("Only use one kind of single-letter variable in the whole expression.")

variable = extract_variable(user_in)

# eval all things in parens and split string into terms
def split_into_terms(expression):
    terms = [str(eval(term)) if '(' in term and ')' in term else term for term in expression.split(' ')]
    print("working with {}".format(' '.join(terms)))
    return terms

terms = split_into_terms(user_in)
print(terms)

# sort terms into bins
def bin_terms(terms):
    squareds, x_es, constants = [], [], []
    for term in terms:
        term = term.strip().lower()
        if term.endswith('**2'):
            squareds.append(term[:-3])
        elif term.endswith(variable):
            x_es.append(term)
        elif term.replace('.', '', 1).isdigit() or term.replace('-', '', 1).replace('.', '', 1).isdigit():
            constants.append(term)
    return squareds, x_es, constants

squareds, x_es, constants = bin_terms(terms)

print('unprocessed:', squareds, x_es, constants, sep='\n')

def sum_bins(squareds, x_es, constants):
    squareds = [squared[:-1] for squared in squareds if squared.endswith(variable)] # 2x -> 2
    print('squareds step1:', squareds, sep='\n')
    squareds = ['1' if squared == variable else squared for squared in squareds] # x -> 1
    print('step2:', squareds)

    print('\nprocessed:', squareds, x_es, constants, sep='\n')

    constant = sum(float(c) for c in constants)
    print('\n ***EXES: ', x_es,'***')
    x = sum(float(el[:-1]) for el in x_es)
    print('\n ***SUMX: ', x,'***')
    squared = sum(float(el) for el in squareds)

    return squared, x, constant

squared, x, constant = sum_bins(squareds, x_es, constants)

def complete_square(a,b,c):
    """
    Complete the square, transforming a quadratic
    of form
    ax^2 + bx + c
    to form
    a(x + p)^2 - q
    """
    p = b/(2*a)
    q = c - (b**2)/(4*a)
    return p, q

p, q = complete_square(squared, x, constant)
a = squared
print('Result is: {}({} + ({}))^2 + ({})'.format(a, variable, p, q))