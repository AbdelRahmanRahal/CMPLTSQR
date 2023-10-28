import re

print(
	"~~~Square Completer!~~~\n"
	"Enter the terms of your quadratic equation in standard form.\n"
	"Addition is implied, terms separated by spaces.\n"
	"Only use one kind of single-letter variable in the whole expression.\n"
	"Surround computations such as constant multiplication and fractions in parenthesis.\n"
	"DO NOT put variables inside parenthesis!\n"
)
user_in = input("> ")


# extract the variable
def extract_variable(expression):
    letters = re.findall(r'[a-z]', expression) # all the letters
    if all(match == letters[0] for match in letters): # if all letters == the first one
        return letters[0] # we have our variable
    else:
        raise ValueError("Only use one kind of single-letter variable in the whole expression.")

variable = extract_variable(user_in)


# eval all things in parens and split string into terms
def split_into_terms(expression):
    expression = re.sub(r"\([^{0}\)]+\)".format(variable), lambda m: str(eval(m.group())), expression)
    print(f"working with {expression}")
    return expression.split(' ')

terms = split_into_terms(user_in)
print(terms)


# sort terms into bins
def bin_terms(terms):
    squareds, x_es, constants = [], [], []
    for term in terms:
        term = term.strip().lower()
        if term.endswith('^2'):
            squareds.append(term[:-2]) # without trailing '^2'
        elif term.endswith(variable):
            x_es.append(term)
        elif bool(re.search(r"^-?[0-9\.]+$", term)): # if the term contains only numbers
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
print(f'Result is: {a}({variable} + ({p}))^2 + ({q})')