# -*- coding: utf-8 -*-
#!/bin/usr/python3

import sys
import random
import math
import numpy
sys.path.append('../..')
from MyCrypto.Classical_cipher.Substitution_Cipher import encrypt, decrypt

Table = 'abcdefghijklmnopqrstuvwxyz'
Frequency_Table = {}
Dice = [0,1] #the dice determine run or not
article = ''

#initial part
GENERATION = 1000
POPULATION_SIZE = 500
TOURNAMENT_SIZE = 20
TOURNAMENT_PROB = 0.75
CROSSOVER_PROB = 0.65
CROSSOVER_POINT = 5
MUTATION_PROB = 0.2
ELITISM_NUM = 125

def format_s(line):
    s_list = []
    for e in line:
        if e.isalpha():
            s_list.append(e.lower())
    return ''.join(s_list)

def get_Frequency_Table(frame):
    with open(frame, 'r') as f:
        head = 0
        tail = 0
        buff = []
        for line in f:
            head = 0
            tail = head + 3
            format_line = format_s(line)
            while tail <= len(format_line):
                for e in format_line[head:tail]:
                    if len(buff) < 3:
                        buff.append(e)
                    else:
                        s_temp = ''.join(buff)
                        if s_temp in Frequency_Table.keys():
                            Frequency_Table[s_temp] += 1
                        else:
                            Frequency_Table[s_temp] = 1
                        buff = []
                head += 1
                tail += 1
        f.close()
    return


def get_Frequency(article, key_table):
    fre_dic = {}
    head = 0
    tail = 0
    buff = []
    head = 0
    tail = head + 3
    plain = decrypt(Table, key_table, article)
    while tail <= len(plain):
        for e in plain[head:tail]:
            if len(buff) < 3:
                buff.append(e)
            else:
                s_temp = ''.join(buff)
                if s_temp in fre_dic.keys():
                    fre_dic[s_temp] += 1
                else:
                    fre_dic[s_temp] = 1
                buff = []
        head += 1
        tail += 1
    return fre_dic

def init_poputation():
    poputation = []
    for i in range(POPULATION_SIZE):
        suflist = list(Table)
        random.shuffle(suflist)
        s_temp = ''.join(suflist)
        if not s_temp in poputation:
            poputation.append(''.join(s_temp))
    return poputation


#Ganetic Algorithm part
def getFitness(article, poputation):
    fitness_list = []
    for e in poputation:
        fre_dic = get_Frequency(article, e)
        fitness = 0
        for key in fre_dic.keys():
            if key in Frequency_Table.keys():
                fitness += fre_dic[key] * math.log2(Frequency_Table[key])
        fitness_list.append(fitness)
    return fitness_list

def sortFitness(poputation, fitness_list):
    zipped = zip(poputation, fitness_list)
    sort_zip = sorted(zipped, key=lambda x:x[1], reverse=True)
    result = zip(*sort_zip)
    n_poputation, n_fitness = [list(x) for x in result]
    return n_poputation, n_fitness

def getElitism(s_poputation):
    nextpoputation = []
    for i in range(ELITISM_NUM):
        nextpoputation.append(s_poputation[i])
    return nextpoputation

def crossOver(father, mather):
    child = [0 for i in range(26)]
    for i in range(CROSSOVER_POINT):
        index = random.randint(0, len(Table)-1)
        child[index] = father[index]
    for i in range(26):
        if child[i] == 0:
            for e in mather:
                if not e in child:
                    child[i] = e
    return ''.join(child)

def tournament(s_poputation):
    select_index = random.sample(range(POPULATION_SIZE), TOURNAMENT_SIZE)
    select_index = sorted(select_index)
    probability = [TOURNAMENT_PROB * ((1-TOURNAMENT_PROB)**i) for i in range(TOURNAMENT_SIZE)]
    index = numpy.random.choice(select_index, p = probability)
    return s_poputation[index]

def mutation(individual):
    individual_list = list(individual)
    i = random.randint(0, len(Table) - 1)
    j = random.randint(0, len(Table) - 1)
    temp = individual_list[i]
    individual_list[i] = individual_list[j]
    individual_list[j] = temp
    return ''.join(individual_list)


def GA(fname, n):
    with open(fname, 'r') as f:
        article = f.read()
        f.close()
    f_article = format_s(article)
    get_Frequency_Table('train.txt')
    poputation = []
    fitness_list = []
    next_poputation = []
    for i in range(GENERATION):
        if i == 0:
            poputation = init_poputation()
        else:
            poputation = next_poputation
        fitness_list = getFitness(f_article, poputation)
        poputation, fitness_list = sortFitness(poputation, fitness_list)
        next_poputation = getElitism(poputation)
        print('GENERATION: {}  bestidividual: {}'.format(i, fitness_list[0]))

        #generate next population
        while len(next_poputation) < POPULATION_SIZE:
            run = numpy.random.choice(Dice, p = [1-CROSSOVER_PROB, CROSSOVER_PROB])
            child1 = ''
            child2 = ''
            father = tournament(poputation)
            while True:
                mather = tournament(poputation)
                if mather != father:
                    break
            if run == 1:#crossover
                child1 = crossOver(father, mather)
                child2 = crossOver(mather, father)
            else:
                child1 = father
                child2 = mather
            mu_run = numpy.random.choice(Dice, p = [1-MUTATION_PROB, MUTATION_PROB])
            if mu_run == 1:
                child1 = mutation(child1)
            mu_run = numpy.random.choice(Dice, p = [1-MUTATION_PROB, MUTATION_PROB])
            if mu_run == 1:
                child2 = mutation(child2)
            if not child1 in next_poputation:
                next_poputation.append(child1)
            if not child2 in next_poputation:
                next_poputation.append(child2)

    poputation = next_poputation
    fitness_list = getFitness(f_article, poputation)
    poputation, fitness_list = sortFitness(poputation, fitness_list)
    for i in range(n):
        print('The Key: {}   The Fitness: {}\n{}'.format(poputation[i], fitness_list[i], decrypt(Table, poputation[i], article)))
    return

if __name__ == '__main__':
    GA('out', 5)
