# Airton Bordin Junior
# airtonbjunior@gmail.com
# Federal University of Goias (UFG)
# Computer Science Master's Degree
#
# Genetic Programming - First example using deap
# Reference: https://github.com/DEAP/deap/blob/08986fc3848144903048c722564b7b1d92db33a1/examples/gp/symbreg.py
#            https://github.com/DEAP/deap/blob/08986fc3848144903048c722564b7b1d92db33a1/examples/gp/spambase.py

import time
import operator
import random

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

import matplotlib.pyplot as plt

import variables
from functions import *

evaluation_acumulated_time = 0

# log time
start = time.time()

pset = gp.PrimitiveSetTyped("MAIN", [str], float)
pset.addPrimitive(operator.add, [float,float], float)
pset.addPrimitive(operator.sub, [float,float], float)
pset.addPrimitive(operator.mul, [float,float], float)
pset.addPrimitive(protectedDiv, [float,float], float)
pset.addPrimitive(math.exp, [float], float)
pset.addPrimitive(math.cos, [float], float)
pset.addPrimitive(math.sin, [float], float)
pset.addPrimitive(protectedSqrt, [float], float)
pset.addPrimitive(protectedLog, [float], float)
pset.addPrimitive(invertSignal, [float], float)
#pset.addPrimitive(math.pow, [float, float], float)

pset.addPrimitive(positiveHashtags, [str], float)
pset.addPrimitive(negativeHashtags, [str], float)
pset.addPrimitive(positiveEmoticons, [str], float)
pset.addPrimitive(negativeEmoticons, [str], float)
pset.addPrimitive(polaritySum, [str], float)
pset.addPrimitive(hashtagPolaritySum, [str], float)
pset.addPrimitive(emoticonsPolaritySum, [str], float)
pset.addPrimitive(positiveWordsQuantity, [str], float)
pset.addPrimitive(negativeWordsQuantity, [str], float)

pset.addPrimitive(hasHashtag, [str], bool)
pset.addPrimitive(hasEmoticons, [str], bool)

pset.addPrimitive(if_then_else, [bool, float, float], float)

pset.addPrimitive(stemmingText, [str], str)
pset.addPrimitive(removeStopWords, [str], str)
pset.addPrimitive(removeLinks, [str], str)
pset.addPrimitive(removeEllipsis, [str], str)
pset.addPrimitive(removeAllPonctuation, [str], str)
pset.addPrimitive(replaceNegatingWords, [str], str)

pset.addTerminal(True, bool)
pset.addTerminal(False, bool)

pset.addEphemeralConstant("rand", lambda: random.uniform(-2, 2), float)

pset.renameArguments(ARG0='x')

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=10)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)


iterate_count = 1
generation_count = 1

# evaluation function 
def evalSymbRegTweetsFromSemeval(individual):
    start = time.time()
    global iterate_count
    global generation_count

    if iterate_count <= variables.POPULATION:
        print("[individual " + str(iterate_count) + " of the generation " + str(generation_count) + "]")
        iterate_count += 1
    else:
        generation_count += 1
        iterate_count = 0
        print("\n[new generation][start generation " + str(generation_count) + "]\n")

    global evaluation_acumulated_time
    correct_evaluations = 0

    fitnessReturn = 0

    is_positive = 0
    is_negative = 0
    is_neutral  = 0
    
    # parameters to calc the metrics
    true_positive  = 0
    true_negative  = 0
    true_neutral   = 0
    false_positive = 0
    false_negative = 0
    false_neutral  = 0

    accuracy = 0

    precision_positive = 0
    precision_negative = 0
    precision_neutral  = 0
    precision_avg = 0

    recall_positive = 0
    recall_negative = 0
    recall_neutral  = 0
    recall_avg = 0

    f1_positive = 0
    f1_negative = 0
    f1_neutral  = 0
    f1_avg = 0
    f1_positive_negative_avg = 0

    breaked = False

    # Transform the tree expression in a callable function
    func = toolbox.compile(expr=individual)

    for index, item in enumerate(variables.tweets_semeval):        

        if variables.generations_unchanged >= variables.max_unchanged_generations:
            breaked = True
            break

        if index == 0:
            print("\n[New cicle]: " + str(len(variables.tweets_semeval)) + " phrases to evaluate [" + str(variables.positive_tweets) + " positives, " + str(variables.negative_tweets) + " negatives and " + str(variables.neutral_tweets) + " neutrals]")

        try:
            if float(variables.tweets_semeval_score[index]) > 0:
                if float(func(variables.tweets_semeval[index])) > 0:
                    correct_evaluations += 1 
                    is_positive   += 1
                    true_positive += 1
                else:
                    if float(func(variables.tweets_semeval[index])) == 0:
                        false_neutral += 1
                    else:
                        false_negative += 1

            elif float(variables.tweets_semeval_score[index]) < 0:
                if float(func(variables.tweets_semeval[index])) < 0:
                    correct_evaluations += 1 
                    is_negative   += 1
                    true_negative += 1
                else:
                    if float(func(variables.tweets_semeval[index])) == 0:
                        false_neutral += 1
                    else:
                        false_positive += 1

            elif float(variables.tweets_semeval_score[index]) == 0:
                if float(func(variables.tweets_semeval[index])) == 0:
                    correct_evaluations += 1 
                    is_neutral   += 1
                    true_neutral += 1
                else:
                    if float(func(variables.tweets_semeval[index])) < 0:
                        false_negative += 1
                    else:
                        false_positive += 1


        except Exception as e: 
            print(e)
            continue

        #logs
        if variables.log_all_messages:
            print("[phrase]: " + variables.tweets_semeval[index])
            print("[value]: " + str(variables.tweets_semeval_score[index]))
            print("[calculated]:" + str(func(variables.tweets_semeval[index])))


    if true_positive + false_positive + true_negative + false_negative > 0:
        accuracy = (true_positive + true_negative + true_neutral) / (true_positive + false_positive + true_negative + false_negative + true_neutral + false_neutral)

    if accuracy > variables.best_accuracy:
        variables.best_accuracy = accuracy 

    # Begin PRECISION
    if true_positive + false_positive > 0:
        precision_positive = true_positive / (true_positive + false_positive)
        if precision_positive > variables.best_precision_positive:
            variables.best_precision_positive = precision_positive


    if true_negative + false_negative > 0:
        precision_negative = true_negative / (true_negative + false_negative)
        if precision_negative > variables.best_precision_negative:
            variables.best_precision_negative = precision_negative
    

    if true_neutral + false_neutral > 0:
        precision_neutral = true_neutral / (true_neutral + false_neutral)
        if precision_neutral > variables.best_precision_neutral:
            variables.best_precision_neutral = precision_neutral
    # End PRECISION

    # Begin RECALL
    if variables.positive_tweets > 0:
        recall_positive = true_positive / variables.positive_tweets
        if recall_positive > variables.best_recall_positive:
            variables.best_recall_positive = recall_positive


    if variables.negative_tweets > 0:
        recall_negative = true_negative / variables.negative_tweets
        if recall_negative > variables.best_recall_negative:
            variables.best_recall_negative = recall_negative

    if variables.neutral_tweets > 0:
        recall_neutral = true_neutral / variables.neutral_tweets
        if recall_neutral > variables.best_recall_neutral:
            variables.best_recall_neutral = recall_neutral
    # End RECALL

    # Begin F1
    if precision_positive + recall_positive > 0:
        f1_positive = 2 * (precision_positive * recall_positive) / (precision_positive + recall_positive)
        if f1_positive > variables.best_f1_positive:
            variables.best_f1_positive = f1_positive


    if precision_negative + recall_negative > 0:
        f1_negative = 2 * (precision_negative * recall_negative) / (precision_negative + recall_negative)        
        if f1_negative > variables.best_f1_negative:
            variables.best_f1_negative = f1_negative

    if precision_neutral + recall_neutral > 0:
        f1_neutral = 2 * (precision_neutral * recall_neutral) / (precision_neutral + recall_neutral)        
        if f1_neutral > variables.best_f1_neutral:
            variables.best_f1_neutral = f1_neutral            
    # End F1

    # Precision, Recall and f1 means
    precision_avg = (precision_positive + precision_negative + precision_neutral) / 3
    if precision_avg > variables.best_precision_avg:
        variables.best_precision_avg = precision_avg
        variables.best_precision_avg_function = str(individual)

    recall_avg = (recall_positive + recall_negative + recall_neutral) / 3
    if recall_avg > variables.best_recall_avg:
        variables.best_recall_avg = recall_avg
        variables.best_recall_avg_function = str(individual)

    f1_avg = (f1_positive + f1_negative + f1_neutral) / 3
    if f1_avg > variables.best_f1_avg:
        variables.best_f1_avg = f1_avg
        variables.best_f1_avg_function = str(individual)

    f1_positive_negative_avg = (f1_positive + f1_negative) / 2
    if f1_positive_negative_avg > variables.best_f1_positive_negative_avg:
        variables.best_f1_positive_negative_avg = f1_positive_negative_avg

    # The metric that represent the fitness
    # fitnessReturn = accuracy
    fitnessReturn = f1_positive_negative_avg


    if variables.best_fitness < fitnessReturn:
        if variables.best_fitness != 0:
            variables.best_fitness_history.append(variables.best_fitness)
        variables.best_fitness = fitnessReturn
        variables.fitness_positive = is_positive
        variables.fitness_negative = is_negative
        variables.fitness_neutral  = is_neutral
        is_positive = 0
        is_negative = 0
        is_neutral  = 0
        variables.generations_unchanged = 0
    else:
        variables.generations_unchanged += 1


    variables.all_fitness_history.append(fitnessReturn)

    restartCacheVariables()

    #logs   
    if variables.log_parcial_results and not breaked: 
        print("[function]: " + str(individual))
        print("[accuracy]: " + str(round(accuracy, 3)))
        print("[precision positive]: " + str(round(precision_positive, 3)))
        print("[precision negative]: " + str(round(precision_negative, 3)))
        print("[precision neutral]: " + str(round(precision_neutral, 3)))
        print("[precision avg]: " + str(round(precision_avg, 3)))
        print("[recall positive]: " + str(round(recall_positive, 3)))
        print("[recall negative]: " + str(round(recall_negative, 3)))
        print("[recall neutral]: " + str(round(recall_neutral, 3)))
        print("[recall avg]: " + str(round(recall_avg, 3)))
        print("[f1 positive]: " + str(round(f1_positive, 3)))
        print("[f1 negative]: " + str(round(f1_negative, 3)))
        print("[f1 neutral]: " + str(round(f1_neutral, 3)))        
        print("[f1 avg]: " + str(round(f1_avg, 3)))
        print("[f1 avg SemEval (positive and negative)]: " + str(round(f1_positive_negative_avg, 3)))
        print("[fitness (F1 +/-)]: " + str(round(fitnessReturn, 3)))
        print("[best fitness]: " + str(round(variables.best_fitness, 3)))
        print("[generations unmodified]: " + str(variables.generations_unchanged))
        print("[true_positive]: " + str(true_positive))
        print("[false_positive]: " + str(false_positive))
        print("[true_negative]: " + str(true_negative))
        print("[false_negative]: " + str(false_negative))
        print("[true_neutral]: " + str(true_neutral))
        print("[false_neutral]: " + str(false_neutral))   
        print("[cicle ends after " + str(format(time.time() - start, '.3g')) + " seconds]")     
        print("\n")   
    #logs

    evaluation_acumulated_time += time.time() - start

    return fitnessReturn,



toolbox.register("evaluate", evalSymbRegTweetsFromSemeval)
toolbox.register("select", tools.selTournament, tournsize=4)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genHalfAndHalf, min_=0, max_=10)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=16))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=16))


def main():
    start = time.time()
    global evaluation_acumulated_time
    random.seed()

    pop = toolbox.population(n=variables.POPULATION)
    hof = tools.HallOfFame(3)

    # Parameters
        # population (list of individuals)
        # toolbox (that contains the evolution operators)
        # Mating probability (two individuals)
        # Mutation probability
        # Number of generations
        # Statistics objetc (updated inplace)
        # HallOfFame object that contain the best individuals
        # Whether or not to log the statistics
    pop, log = algorithms.eaSimple(pop, toolbox, 0.8, 0.1, variables.GENERATIONS, stats=False,
                                   halloffame=hof, verbose=False)


    #logs
    print("\n")
    print("## Results ##\n")
    print("[total tweets]: " + str(variables.positive_tweets + variables.negative_tweets + variables.neutral_tweets) + " [" + str(variables.positive_tweets) + " positives, " + str(variables.negative_tweets) + " negatives and " + str(variables.neutral_tweets) + " neutrals]\n")
    print("[best fitness (F1 avg (+/-)]: " + str(variables.best_fitness) + " [" + str(variables.fitness_positive + variables.fitness_negative + variables.fitness_neutral) + " correct evaluations] ["+ str(variables.fitness_positive) + " positives, " + str(variables.fitness_negative) + " negatives and " + str(variables.fitness_neutral) + " neutrals]\n")
    print("[function]: " + str(hof[0]) + "\n")
    print("[best accuracy]: " + str(variables.best_accuracy) + "\n")
    print("[best precision positive]: " + str(variables.best_precision_positive))
    print("[best precision negative]: " + str(variables.best_precision_negative))
    print("[best precision neutral]: "  + str(variables.best_precision_neutral))    
    print("[best precision avg]: " + str(variables.best_precision_avg))
    print("[best precision avg function]: " + variables.best_precision_avg_function + "\n")    
    print("[best recall positive]: " + str(variables.best_recall_positive))    
    print("[best recall negative]: " + str(variables.best_recall_negative))
    print("[best recall avg]: " + str(variables.best_recall_avg))
    print("[best recall avg function]: " + variables.best_recall_avg_function + "\n")
    print("[best f1 positive]: " + str(variables.best_f1_positive))    
    print("[best f1 negative]: " + str(variables.best_f1_negative))
    print("[best f1 avg]: " + str(variables.best_f1_avg))
    print("[best f1 avg (+/-)]: " + str(variables.best_f1_positive_negative_avg))
    print("[best f1 avg function]: " + variables.best_f1_avg_function + "\n")       
    #print(json.dumps(variables.all_fitness_history))
    print("\n")
    #print(set(variables.all_fitness_history))
    #logs 

    end = time.time()
    print("[evaluation function consumed " + str(format(evaluation_acumulated_time, '.3g')) + " seconds]")
    print("[main function ended][" + str(format(end - start, '.3g')) + " seconds]\n")
    
    return pop, log, hof


if __name__ == "__main__":
    loadTrainTweets()
    getDictionary()
    main()

    print(len(variables.all_fitness_history))
    print(variables.all_fitness_history)
    # remove the 0's values to plot
    plt.plot(list(filter(lambda a: a != 0, variables.all_fitness_history)))   
    plt.ylabel('f1')
    plt.show()


end = time.time()
print("Script ends after " + str(format(end - start, '.3g')) + " seconds")