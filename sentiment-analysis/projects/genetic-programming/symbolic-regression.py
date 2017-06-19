# Airton Bordin Junior
# airtonbjunior@gmail.com
# Federal University of Goias (UFG)
# Computer Science Master's Degree
#
# Genetic Programming - First example using deap
# Reference: https://github.com/DEAP/deap/blob/08986fc3848144903048c722564b7b1d92db33a1/examples/gp/symbreg.py

import operator
import math
import random
import re
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp


# The reviews and the scores are global
reviews = []
reviews_scores = []


# Define new functions
# Protected Div (check division by zero)
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
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


def onlyTestFuncion(string1, string2):
    return 0


def onlyTestFuncion2(float1, float2):
    return "abc"


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

pset.addPrimitive(math.cos, [float], float)
pset.addPrimitive(math.sin, [float], float)

pset.addPrimitive(positiveHashtags, [str], float)
pset.addPrimitive(negativeHashtags, [str], float)
pset.addPrimitive(polaritySum, [str], float)

pset.addPrimitive(onlyTestFuncion, [str, str], float)
pset.addPrimitive(onlyTestFuncion2, [float, float], str)


pset.addEphemeralConstant("rand1to5", lambda: float(random.randint(1,3)), float)
#pset.addTerminal(1.0, float)
#pset.addTerminal(2.0, float)
#pset.addTerminal(3.0, float)
#pset.addTerminal(4.0, float)
#pset.addTerminal(5.0, float)
#pset.addTerminal(6.0, float)
#pset.addTerminal(7.0, float)
#pset.addTerminal(8.0, float)



pset.renameArguments(ARG0='x')

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset=pset, min_=1, max_=5)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)


# evaluation function 
def evalSymbReg(individual): #, points):    
    global reviews
    global reviews_scores
    fitnessReturn = 0

    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)

    #logs
    print(str(len(reviews)) + " phrases to evaluate")
    #logs
    
    for index, item in enumerate(reviews):        

        #sqerrors = (func(reviews[index]) - float(reviews_scores[index]) for review in reviews)
        if func(reviews[index]) == float(reviews_scores[index]):
            fitnessReturn += 1 

        #logs
        #print(index, item)
        print("[phrase]: " + reviews[index])
        print("[value]: " + reviews_scores[index])
        print("[calculated]:" + str(func(reviews[index])))
        #logs
    
    #logs    
    print("[fitness]: " + str(fitnessReturn))
    print("\n\n")   
    #logs

    #return math.fsum(sqerrors) / len(reviews),  
    return fitnessReturn,
    

    #reviews_samp = random.sample(reviews, 1)
    #print(reviews_samp)

    # Evaluate the mean squared error between the expression
    # and the real function : x**4 + x**3 + x**2 + x
    #sqerrors = ((func(x) - x**4 - x**3 - x**2 - x)**2 for x in points)
    #return math.fsum(sqerrors) / len(points),



#toolbox.register("evaluate", evalSymbReg, points=[x/10. for x in range(-10,10)])
toolbox.register("evaluate", evalSymbReg) # , points=[x for x in reviews])


toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

def main():
    #random.seed(318)

    pop = toolbox.population(n=20)
    hof = tools.HallOfFame(1)
    
    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)


    # Parameters
        # population (list of individuals)
        # toolbox (that contains the evolution operators)
        # Mating probability (two individuals)
        # Mutation probability
        # Number of generations
        # Statistics objetc (updated inplace)
        # HallOfFame object that contain the best individuals
        # Whether or not to log the statistics
    pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 40, stats=mstats,
                                   halloffame=hof, verbose=False)#True)


    #polaritySum("instantly I good nice bad love this camera so much hate")
    #positiveHashtags("instantly I #good nice #bad love this camera so much #hate so")
    #negativeHashtags("instantly I #good nice #bad love this camera so much #hate so")

    #getReviews()

    
    #logs
    #print("\n")
    #for i in reviews:
        #print(i)
        #print("\n")


    #print("\n\n")
    #print(reviews)
    #print(len(reviews))
    #print("\n\n")
    #print(reviews_scores)
    #print(len(reviews_scores))
    #logs

    #logs
    #print("\n")
    #for i in pop:
    #    print(i)
    print("\n")
    print(hof[0]) 
    #logs 


    # UNCOMENT
    return pop, log, hof
    # UNCOMENT

if __name__ == "__main__":
    main()




# TO-DO: uppercasepositive uppercasenegative 
# repeated vowel
# see n-gram dictionary