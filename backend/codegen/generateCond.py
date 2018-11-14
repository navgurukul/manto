import random
"""
Our current vocab

CONDITION
and
or
not
BRACKET
number
CONDITIONAL_OPERATOR
WHILE
"""

GLEVEL = 0
CONCEPT_ARRAYS =  ["BRACKET", "and", "or", "not", "CONDITIONAL_OPERATOR", \
                  "BASIC_OOPERATORS", "MODULUS_OPERATOR", \
                  "VAR_ASSIGNMENT", "IFELSE", "WHILE"]

BASIC_OOPERATORS = ["+", "-", "*", "/"]
MODULUS_OPERATOR = "%"
CONDITIONAL_OPERATORS = ["==", "!=", "<", ">", ">=", "<="]
BOOLEAN_VALUES = ["True", "False"]
VARIABLES_ARRAY = ["caboVerde", "costaRica", "dominicanRepublic", "elSalvador", "guineaBissau", "holySee", "koreaSouth",
                   "newZealand", "palestinianTerritories", "sanMarino", "solomonIslands", "sriLanka", "timorLeste", "unitedKingdom", "southSudan"]
INDEX_VARIABLES_NAMES = ["ctr", "index", "i", "n"]

# Kaun kaun se variables, kis type se define kiye hai
# [{name: "shivam", type: "bool"}]
variable_map = []

def makeBoolean():
    return random.choice(BOOLEAN_VALUES)

def makeString():
    return '"' + random.choice(VARIABLES_ARRAY) + '"'

def selectWeightedRandom(container, weights):
    total_weight = float(sum(weights))
    rel_weight = [w / total_weight for w in weights]

    # Probability for each element
    probs = [sum(rel_weight[:i + 1]) for i in range(len(rel_weight))]

    slot = random.random()*1
    for (i, element) in enumerate(container):
        if slot <= probs[i]:
            break

    return element


def prepareForWeightedSelection(selectionList):
    cases = []
    weights = []
    for obj in selectionList:
        cases.append(obj['name'])
        weights.append(obj['weight'])

    return selectWeightedRandom(cases, weights)


def makeList(level=3):
    casesWithWeights = [{"name": "NUMBER", "weight": 3}, {
        "name": "STRING", "weight": 4}, {"name": "BOOLEAN", "weight": 1}]

    if level > 1:
        casesWithWeights.append({"name": 'LIST', "weight": 2})

    rcase = prepareForWeightedSelection(casesWithWeights)

    new_case = '['
    num_elements = int(random.random()*5)

    if num_elements == 0:
        return "[]"

    for i in range(num_elements):
        if rcase == 'NUMBER':
            new_case = new_case + makeNumber() + ', '
        elif rcase == 'STRING':
            new_case = new_case + makeString() + ', '
        elif rcase == 'BOOLEAN':
            bool_val = str(makeBoolean())
            new_case = new_case + bool_val + ', '
        elif rcase == 'LIST':
            new_case = new_case + makeList(level=level-2) + ', '
            # ast.literal_eval(makeList(level=level-2)) + ', '

    new_case = new_case[:-2]
    new_case += ']'
    return new_case

def makeConstant(level=2):
    cases = ['NUMBER', 'STRING', 'BOOLEAN', "LIST"]
    weights = [3, 4, 1, 3]
    casesWithWeights = [{"name": "NUMBER", "weight": 3}, {"name": "STRING", "weight": 4}, {"name": "BOOLEAN", "weight": 1}, {"name": "LIST", "weight": 3}]

    #TDOD - MAKE A FUNCTION TO FIND INTERSECTION OF CASES WITH CONCEPT_ARRAY INPUT TO CREATE A NEW CASE ARRAY

    rcase = prepareForWeightedSelection(casesWithWeights)

    if rcase == 'NUMBER':
        new_case = makeNumber()
    elif rcase == 'STRING':
        new_case = makeString()
    elif rcase == 'BOOLEAN':
        bool_val = str(makeBoolean())
        new_case = bool_val
    elif rcase == 'LIST':
        new_case = makeList(2)

    return new_case

def makeVarAssignment():
    casesWithWeights = [{"name": ["VARNAME", "=", 'NUMBER'], "weight": 4}, {
        "name": ["VARNAME", "=", 'STRING'], "weight": 2}, {"name": ["VARNAME", "=", 'BOOLEAN'], "weight": 1}, {"name": ["VARNAME", "=", 'LIST'], "weight": 1}, {"name": ["VARNAME", "=", 'CONDITION'], "weight": 2}]

    rcase = prepareForWeightedSelection(casesWithWeights)

    new_case = ""

    for keyword in rcase:
        if keyword == "VARNAME":
            var_name = random.choice(VARIABLES_ARRAY)
            new_case += var_name
            dic = {"name": var_name, "type": rcase[2]}  # MAKE THIS GENERIC
            variable_map.append(dic)

        elif keyword == "NUMBER":
            new_case += makeNumber()
        elif keyword == "BOOLEAN":
            new_case += makeBoolean()
        elif keyword == "STRING":
            new_case += makeString()
        elif keyword == "LIST":
            new_case += makeList()
        elif keyword == "CONDITION":
            new_case += makeCondition()
        else:
            new_case += keyword
        new_case += " "

    return new_case

def makePrintStatement():
    if (len(variable_map)):
        return "print " + random.choice(variable_map)["name"]
    return "print " + makeConstant()

def makeStatement():
    casesWithWeights = [{"name": 'CONDITION', "weight": 3}, {
        "name": 'NUMBER', "weight": 1}, {"name": 'VAR_ASSIGNMENT', "weight": 2}, {"name": 'IFSTATEMENT', "weight": 2}, {"name": 'WHILE', "weight": 4}, {"name": "PRINT_STATEMENT", "weight": 5 }]

    rcase = prepareForWeightedSelection(casesWithWeights)

    new_case = ""

    # TODO SHIFT SUCH IFS TO SWITCH STATEMENTS
    if rcase == "CONDITION":
        new_case += makeCondition()
    elif rcase == "NUMBER":
        new_case += makeNumber()
    elif rcase == "VAR_ASSIGNMENT":
        new_case += makeVarAssignment()
    elif rcase == "IFSTATEMENT":
        new_case += makeIfBlock()
    elif rcase == "WHILE":
        new_case += makeWhileBlock()
    elif rcase == "PRINT_STATEMENT":
        new_case += makePrintStatement()

    #TODO - DO THIS WITH REGEX INSTEAD
    while ("  " in new_case):
        new_case = new_case.replace("  ", " ")

    while ("( " in new_case):
        new_case = new_case.replace("( ", "(")

    while (" )" in new_case):
        new_case = new_case.replace(" )", ")")

    while ("[ " in new_case):
        new_case = new_case.replace("[ ", "[")

    while (" ]" in new_case):
        new_case = new_case.replace(" ]", "]")

    if new_case.startswith(" "):
        new_case = new_case[1:]

    return new_case

def makeSmallInteger():
    return str(int(random.random()*10))

def makeSmallPositiveInteger():
    return str(int(random.random()*9)+1)

def makeNumber(level=3):
    casesWithWeights = [{"name": ["FLOAT"], "weight": 3},
                        {"name": ["INTEGER"], "weight": 1}]

    if "BASIC_OPERATORS" in CONCEPT_ARRAYS and level > 1:
        casesWithWeights += [
                {"name": "NUMBER", "weight": 3}, \
                {"name": "BASIC_OPERATOR", "weight": 3}, \
                {"name": "NUMBER", "weight": 3}
        ]

    if "MODULUS_OPERATOR" in CONCEPT_ARRAYS and level > 2:
        casesWithWeights += [
            {"name": "INTEGER", "weight": 3}, \
            {"name": "MODULUS_OPERATOR", "weight": 3}, \
            {"name": "SMALL_POSITIVE_INTEGER", "weight": 3}
        ]

    # if "BASIC_OPERATORS" in CONCEPT_ARRAYS and level > 1:
    #     casesWithWeights.append(
    #         {"name": ["NUMBER", "BASIC_OPERATOR", "NUMBER"], "weight": 3})

    # if "MODULUS_OPERATOR" in CONCEPT_ARRAYS and level > 2:
    #     casesWithWeights.append(
    #         {"name": ["INTEGER", "MODULUS_OPERATOR", "SMALL_POSITIVE_INTEGER"], "weight": 3})

    rcase = prepareForWeightedSelection(casesWithWeights)

    new_case = ""
    for keyword in rcase:
        if keyword == "FLOAT":
            # TODO DO FLOAT TO STRING HERE
            new_case += str("{:12.2f}".format(random.random()*100))
        elif keyword == "INTEGER":
            new_case += str(int(random.random()*100))
        elif keyword == "SMALL_INTEGER":
            new_case += makeSmallInteger()
        elif keyword == "SMALL_POSITIVE_INTEGER":
            new_case += makeSmallPositiveInteger()
        elif keyword == "NUMBER":
            new_case += makeNumber()
        elif keyword == "BASIC_OPERATOR":
            new_case += random.choice(BASIC_OOPERATORS)
        else:
            new_case += MODULUS_OPERATOR
        new_case += " "

    return new_case


def makeCondition(level=3):
    casesWithWeights = []
    if level == 2 or level == 1:
        casesWithWeights.append({"name": "True", "weight": 2})
        casesWithWeights.append({"name": "False", "weight": 1})

    if "BRACKET" in CONCEPT_ARRAYS and level > 1:
        casesWithWeights.append({"name": ["(", "CONDITION", ")"], "weight": 2})

    if "and" in CONCEPT_ARRAYS and level > 1:
        casesWithWeights.append(
            {"name": ["CONDITION", "and", "CONDITION"], "weight": 4})

    if "or" in CONCEPT_ARRAYS and level > 1:
        casesWithWeights.append(
            {"name": ["CONDITION", "or", "CONDITION"], "weight": 3})

    if "not" in CONCEPT_ARRAYS and level > 1:
        casesWithWeights.append({"name": ["not", "CONDITION"], "weight": 1})

    if "CONDITIONAL_OPERATOR" in CONCEPT_ARRAYS and level > 1:
        casesWithWeights.append(
            {"name": ["(", "NUMBER", "CONDITIONAL_OPERATOR", "NUMBER", ")"], "weight": 5})

    rcase = prepareForWeightedSelection(casesWithWeights)

    if len(rcase) == 1:
        return rcase[0]

    else:
        new_case = ""
        for keyword in rcase:
            if keyword == "CONDITION":
                new_case += makeCondition(level=level-1)
            elif keyword == "NUMBER":
                new_case += makeNumber()
            elif keyword == "CONDITIONAL_OPERATOR":
                new_case += random.choice(CONDITIONAL_OPERATORS)
            else:
                new_case += keyword
            new_case += " "

        return new_case

    return 'BUG'


def getBiggerBlock(num=2):
    block = makeBlock(num=2)
    block = map(lambda x: x.split('\n'), block)
    block = reduce(lambda x, y: x+y, block)
    return block

def makeWhileCondition(index_variable):
    condition = index_variable + " " + random.choice(["<", "<=", "!="]) + " " + makeSmallInteger()
    return condition

def incrementCondition(index_variable):
    return random.choice([index_variable + " += 1", index_variable + " = " + index_variable + " + 1"])

def makeWhileBlock(level=2):
    index_variable = random.choice(INDEX_VARIABLES_NAMES)

    return "while ("+makeWhileCondition(index_variable)+") :\n\t" + \
            "\n\t".join(getBiggerBlock()) + \
            "\n\t" + incrementCondition(index_variable)

def makeIfBlock(level=2):
    casesWithWeights = [{"name": "IF", "weight": 3}, {
        "name": "IFELSE", "weight": 2}]

    if level > 1:
        casesWithWeights.append({"name": "IFELIFSE", "weight": 2})

    rcase = prepareForWeightedSelection(casesWithWeights)

    if rcase == "IF":
        return "if ("+makeCondition(level=1)+") :\n\t" + \
            "\n\t".join(getBiggerBlock()) + \
            "\n"

    elif rcase == "IFELSE":
        return "if ("+makeCondition(level=1)+") :\n\t" + \
            "\n\t".join(getBiggerBlock()) + \
            "\nelse:\n\t" + \
            "\n\t".join(getBiggerBlock())

    elif rcase == "IFELIFSE":
        return "if ("+makeCondition(level=1)+") :\n\t" + \
            "\n\t".join(getBiggerBlock()) + \
            "\nelif ("+makeCondition(level=1)+") :\n\t" + \
            "\n\t".join(getBiggerBlock()) + \
            "\nelse:\n\t" + \
            "\n\t".join(getBiggerBlock())


def makeBlock(num=5):
    statements = []
    num_statements = int(random.random()*num)+1
    for _ in range(num_statements):
        statements.append(makeStatement())
    return statements

def generateCode(concept_arrays = ["BRACKET", "and", "or", "not", "CONDITIONAL_OPERATOR", \
                  "BASIC_OOPERATORS", "MODULUS_OPERATOR", \
                  "VAR_ASSIGNMENT", "IFELSE", "WHILE"]):
                
    # CONCEPT_ARRAYS = concept_arrays
    for i in makeBlock():
        print i

    for var in variable_map:
        print "print "+var["name"]

if __name__ == "__main__":
    generateCode()