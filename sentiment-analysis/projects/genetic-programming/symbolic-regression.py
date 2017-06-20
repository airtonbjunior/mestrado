# Airton Bordin Junior
# airtonbjunior@gmail.com
# Federal University of Goias (UFG)
# Computer Science Master's Degree
#
# Genetic Programming - First example using deap
# Reference: https://github.com/DEAP/deap/blob/08986fc3848144903048c722564b7b1d92db33a1/examples/gp/symbreg.py
#            https://github.com/DEAP/deap/blob/08986fc3848144903048c722564b7b1d92db33a1/examples/gp/spambase.py

import operator
import math
import random
import re
import numpy
import time

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp


start = time.time()

# The reviews and the scores are global
reviews = []
reviews_scores = []
best_fitness = 0

uses_dummy_function = False

# Define new functions
# Protected Div (check division by zero)
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1


def protectedLog(value):
    try:
        return math.log10(value)
    except:
        return 1    


def protectedSqrt(value):
    try:
        return math.sqrt(value)
    except:
        return 1  


# Return the sum of the word polarities (positive[+1], negative[-1])
# Liu's dicionary of positive and negative words
def polaritySum(phrase):
    words = phrase.split()

    total_sum = 0

    for word in words:
        with open('positive-words.txt', 'r') as inF:
            for line in inF:
                if word in line and len(line.strip()) == len(word.strip()):
                    #print("positive word " + word)
                    total_sum += 1 
                    break


        with open('negative-words.txt', 'r') as inF2:
            for line2 in inF2:
                if word in line2 and len(line2.strip()) == len(word.strip()):
                    #print('negative word ' + word)
                    total_sum -= 1   
                    break                   

    #print(total_sum) # log
    return total_sum


# Positive Hashtags
def positiveHashtags(phrase):
    total = 0
    if "#" in phrase:
        #print("has hashtag")
        hashtags = re.findall(r"#(\w+)", phrase)

        for hashtag in hashtags:
            with open('positive-words.txt', 'r') as inF:
                for line in inF:
                    if hashtag in line and len(line.strip()) == len(hashtag.strip()):
                        #print("positive hashtag " + hashtag)
                        total += 1 
                        break

    return total


# Negative Hashtags
def negativeHashtags(phrase):
    total = 0
    if "#" in phrase:
        #print("has hashtag")
        hashtags = re.findall(r"#(\w+)", phrase)

        for hashtag in hashtags:
            with open('negative-words.txt', 'r') as inF:
                for line in inF:
                    if hashtag in line and len(line.strip()) == len(hashtag.strip()):
                        #print("negative hashtag " + hashtag)
                        total += 1 
                        break

    return total


# logic operators
# Define a new if-then-else function
def if_then_else(input, output1, output2):
    if input: return output1
    else: return output2


def onlyTestFuncion(string1, string2):
    global uses_dummy_function
    uses_dummy_function = True
    return 1


def onlyTestFuncion2(float1, float2):
    return ""


def invertSignal(val):
    return -val

def getReviews():
    global reviews
    global reviews_scores

    review = ""
    score = ""
    start_of_next_review = ""
    end_of_review = False

    with open('reviews.txt', 'r') as inF:
        for line in inF:
            if line.startswith("*"): # comments of the review file
                continue

            if not re.findall(r"\[t\]", line):  # titles start with [t]. I'll not use the titles (check)
                if line.startswith("##"):
                    review += line[line.index('#') + 2: ].strip() # remove the ##
                    #print(review)
                else:
                    score += line[line.index('[') + 1 : line.index(']')].strip()
                    start_of_next_review += line[line.index('#') + 2 : ].strip()  # remove the ##
                    end_of_review = True
                    #print(line)
            

            if end_of_review:
                if len(review) > 0:
                    reviews.append(review.strip())
                
                if len(score) > 0:
                    reviews_scores.append(score.strip())
                    score = ""

                review = start_of_next_review
                start_of_next_review = ""
                
                end_of_review = False    

        reviews.append(review.strip()) # last review


# Parse the review file
getReviews()

pset = gp.PrimitiveSetTyped("MAIN", [str], float)
pset.addPrimitive(operator.add, [float,float], float)
pset.addPrimitive(operator.sub, [float,float], float)
pset.addPrimitive(operator.mul, [float,float], float)
pset.addPrimitive(protectedDiv, [float,float], float)

#pset.addPrimitive(math.pow, [float, float], float)

pset.addPrimitive(math.exp, [float], float)
pset.addPrimitive(math.cos, [float], float)
pset.addPrimitive(math.sin, [float], float)
pset.addPrimitive(protectedSqrt, [float], float)

pset.addPrimitive(protectedLog, [float], float)
pset.addPrimitive(invertSignal, [float], float)

pset.addPrimitive(positiveHashtags, [str], float)
pset.addPrimitive(negativeHashtags, [str], float)
pset.addPrimitive(polaritySum, [str], float)

pset.addPrimitive(onlyTestFuncion, [str, str], float)
pset.addPrimitive(onlyTestFuncion2, [float, float], str)


pset.addEphemeralConstant("rand", lambda: float(random.randint(-2,2)), float)


pset.renameArguments(ARG0='x')

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
#toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=5)

toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)


# evaluation function 
def evalSymbReg(individual):
    global reviews
    global reviews_scores
    global best_fitness
    global uses_dummy_function
    fitnessReturn = 0

    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)

    #logs
    print(str(len(reviews)) + " phrases to evaluate")
    #logs
    
    for index, item in enumerate(reviews):        

        if (func(reviews[index]) > 0 and float(reviews_scores[index]) > 0) or (func(reviews[index]) < 0 and float(reviews_scores[index]) < 0):
            fitnessReturn += 1 

        #logs
        #print(index, item)
        print("[phrase]: " + reviews[index])
        print("[value]: " + reviews_scores[index])
        print("[calculated]:" + str(func(reviews[index])))
        #logs
    
    if uses_dummy_function:
        fitnessReturn = 0
        uses_dummy_function = False

    if best_fitness < fitnessReturn:
        best_fitness = fitnessReturn


    #logs    
    print("[function]: " + str(individual))
    print("[fitness]: " + str(fitnessReturn))
    print("\n\n")   
    #logs

    return fitnessReturn,


toolbox.register("evaluate", evalSymbReg) # , points=[x for x in reviews])


toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genGrow, min_=0, max_=4)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

def main():

    global best_fitness

    random.seed()

    pop = toolbox.population(n=10)
    hof = tools.HallOfFame(1)
    
    
    #stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    #stats_size = tools.Statistics(len)
    #mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    #mstats.register("avg", numpy.mean)
    #mstats.register("std", numpy.std)
    #mstats.register("min", numpy.min)
    #mstats.register("max", numpy.max)


    # Parameters
        # population (list of individuals)
        # toolbox (that contains the evolution operators)
        # Mating probability (two individuals)
        # Mutation probability
        # Number of generations
        # Statistics objetc (updated inplace)
        # HallOfFame object that contain the best individuals
        # Whether or not to log the statistics
    pop, log = algorithms.eaSimple(pop, toolbox, 1.0, 0.7, 15, stats=False,
                                   halloffame=hof, verbose=False)#True)

    #logs
    #print("\n")
    #for i in pop:
    #    print(i)
    print("\n")
    print("[best fitness]: " + str(best_fitness))
    print(hof[0]) 
    #logs 

    return pop, log, hof


if __name__ == "__main__":
    main()


end = time.time()
print("Script ends after " + str(format(end - start, '.3g')) + " seconds")


# TO-DO: uppercasepositive uppercasenegative 
# repeated vowel
# see n-gram dictionary