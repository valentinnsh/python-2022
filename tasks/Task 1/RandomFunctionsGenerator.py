import enum
import sympy
import time
from numpy import random
from sympy.calculus.util import continuous_domain


def generate_and_dump_to_files(count, filename='functions.dat'):
    with open(filename, 'w') as f:
        for i in range(count):
            func = generate(random.randint(4, 7))
            print(func)
            if not is_reasonably_solvable(func):
                continue
            f.write(func + '\n')


def generate(length):
    delimiters = ['+', '-', '*', '/']
    terms = [Term(random.randint(0, 3), random.choice([Term.TermType.NUMBER, Term.TermType.VARIABLE, Term.TermType.FUNCTION])).generate() for _ in range(length)]
    result = terms[0]
    for i in range(len(terms) - 1):
        result += random.choice(delimiters) + terms[i+1]
    return result.replace('+-', '-').replace('--', '-')


def is_reasonably_solvable(function_str):
    x = sympy.symbols('x', real=True)
    parsed = sympy.parse_expr(function_str, locals())
    try:
        tm = time.time()
        domain = continuous_domain(parsed, x, sympy.S.Reals)
        tm = time.time() - tm
    except Exception as e:
        print(e)
        return False

    if tm > 5:
        return False
    if type(domain) == sympy.sets.sets.EmptySet:
        return False

    return True

class Term:
    def __init__(self, complexity, term_type):
        # complexity is a number from 0 to 3 indicating how complex the term should be
        # 0 - plain number, variable or function
        # 1 - number coefficient should be added
        # 2 - this term will be multiplied by a random VARIABLE term with complexity 1
        # 3 - this term will be multiplied by a random FUNCTION term with complexity 1
        self.complexity = complexity
        self.term_type = term_type
        self.unacceptable_values = []

    class TermType(enum.Enum):
        NUMBER = 1  # plain number, unaffected by complexity parameter
        VARIABLE = 2  # variable, can be multiplied by a number or another variable and have a power of a number
        FUNCTION = 3  # sin, cos, log functions. may contain another whole term inside if happen to have complexity of 3, otherwise it will be a variable term
        SUMM = 4  # summ of 2-5 random terms
        POLYNOM = 5  # polynom of degree 2-4

    def generate(self):
        functions = ('sin', 'cos', 'log')
        if self.term_type == Term.TermType.NUMBER:
            # Decided to use random integers instead of floats since it would be easier to look at and should not make tests worse
            return str(random.choice([i for i in range(-10, 11) if i not in [0]]))

        elif self.term_type == Term.TermType.VARIABLE:
            if self.complexity > 0:
                var_term = f'{random.choice([i for i in range(-10, 11) if i not in [0]])}*x'
            else:
                var_term = 'x'

            if self.complexity == 2:
                var_term += f'*{Term(random.choice([0,1]), Term.TermType.VARIABLE).generate()}'
            elif self.complexity == 3:
                var_term += f'*{Term(random.choice([0,1]), Term.TermType.FUNCTION).generate()}'
            return var_term

        elif self.term_type == Term.TermType.FUNCTION:
            func = random.choice(functions)

            # exp grows too fast, often ruining tests. I COULD have tried to limit it in some way,
            # but I decided to prioritize other tasks over this optimization and remove exp from generator
            # if func == 'exp':
            #    return f'{Term(random.choice([0,1]), Term.TermType.NUMBER).generate()}*exp(x)'

            func_term = f'{func}('
            if self.complexity == 0:
                func_term += f'{Term(random.choice([0,1]), Term.TermType.VARIABLE).generate()})'

            if self.complexity == 1:
                func_term += f'{Term(random.choice([0,1]), Term.TermType.POLYNOM).generate()})'

            if self.complexity == 2:
                func_term += f'{Term(random.choice([0,3]), Term.TermType.FUNCTION).generate()})'

            if self.complexity == 3:
                func_term += f'{Term(random.choice([0,3]), Term.TermType.SUMM).generate()})'

            return func_term

        elif self.term_type == Term.TermType.SUMM:
            terms = [Term(random.randint(0, 3), random.choice(
                [Term.TermType.NUMBER, Term.TermType.VARIABLE, Term.TermType.FUNCTION])).generate() for _ in
                     range(random.randint(1, 5))]
            summ = terms[0]
            for i in range(len(terms) - 1):
                summ += '+' + terms[i + 1]

            return summ

        elif self.term_type == Term.TermType.POLYNOM:
            degree = random.randint(2, 4)
            polynom = [f'{random.choice([i for i in range(-10, 11) if i not in [0]])}*x**{i}' for i in range(1, degree)]
            return '+'.join(polynom)+f'+{random.randint(-10, 10)}'

