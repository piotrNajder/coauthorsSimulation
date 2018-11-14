from agent import Agent, CoWorker
from work import Work
from random_gen import RandomGenerator as rg
from simu_utils import readConfigFile

import argparse

import numpy as np
import matplotlib.pyplot as plt

import math

import os
import sys

CONST_MAX_AUTHORS = 200  # Max numbers of coauthors we expect

def createAgents(numOfAgents, theList, config):
    credit = float(config.get("credit"))
    std_credit = float(config.get("std_credit"))
    activity = float(config.get("activity"))
    quality = float(config.get("mean_mean_quality")) 
    std_mean_quality = float(config.get("std_mean_quality"))
    std_quality = float(config.get("mean_std_quality")) 
    std_std_qualty =  float(config.get("std_std_quality"))

    for i in range(0, numOfAgents):
        theList.append(Agent(i, 
                             credit + std_credit * rg.granf(),
                             activity,
                             quality + std_mean_quality * rg.granf(),
                             std_quality + std_std_qualty * rg.granf()))

       

def createNetwork(numOfAgents, theList, config):
    thr = float(config.get("threshold"))
    loops = int(config.get("neighbours_avg")) * numOfAgents + 1
    printMarker = int(loops / 10)
    for k in range(0, loops):
        ### progress bar 
        if k % printMarker == 0:
            print("#", end = "")
            sys.stdout.flush()
            
        ### get two random Ids
        i = rg.iranx(numOfAgents) - 1
        j = rg.iranx(numOfAgents) - 1
        while(i == j):            
            j = rg.iranx(numOfAgents) - 1

        ### get agent objects for given id
        ag1 = None
        ag2 = None

        ag = list(filter(lambda a: a.Id == i, theList))
        if len(ag) > 0: ag1 = ag[0]

        ag = list(filter(lambda a: a.Id == j, theList))
        if len(ag) > 0: ag2 = ag[0]

        c = thr * rg.ranf()
        
        ag1.addCoworker( CoWorker(ag2, c) )
        ag2.addCoworker( CoWorker(ag1, c) )
    print("")

def saveHistogram(iteration, hist):

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    fName = os.path.join(fileDir, "results/hist{}.dat".format(iteration))
    with open(fName, "w") as f:
        for i, val in enumerate(hist):
            if val != 0:
                f.write("{} {:.3f}\n".format(i, float(val) / hist.sum()))

def saveHistogramStats(counter, hist):    
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    fName = os.path.join(fileDir, "results/w.dat")

    mean = 0.0
    std = 0.0
    l = 0.0

    for i in range(0, CONST_MAX_AUTHORS):
        mean += i * float(hist[i])
        std += i * i * float(hist[i])
        l += hist[i]

    mean /= l
    std /= l
    std = math.sqrt(std - mean * mean)

    with open(fName, "a") as f:
        f.write("{} {:.3f} {:.3f} {}\n".format(counter, mean, std, l ))

def saveConfig(iteration, theList):
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    fName = os.path.join(fileDir, "results/agentStats{}.dat".format(iteration))
    with open(fName, "w") as f:
        for ag in theList:
            f.write("{} {:.3f} {:.3f} {:.3f}\n".format(int(ag.Id), ag.Credit, ag.Quality, ag.NumberOfCoworkers))

def saveProbabilitiesStats(iteration, theList):
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    probFName = os.path.join(fileDir, "results/probabilities{}.dat".format(iteration))
    probConfName = os.path.join(fileDir, "results/prob_conf{}.dat".format(iteration))
    with open(probFName, "w") as probF, open(probConfName, "w") as probConfF:
        for ag in theList:
            probF.write("{}".format(ag.Id))
            for coWorker in ag.ListOfCoworkers:
                probF.write("{} {:.3f}".format(coWorker.Agent.Id, coWorker.Prob))
                probConfF.write("{:.3f}\n".format(coWorker.Prob))
            
            probF.write("\n")

def main(args):
    
    worldConfig = {}
    agentsList = list()
    worksList = list()   

    worldConfig = readConfigFile(args.inputFile)    

    ### Here we have config in dictonary
    ### We cann start the init part

    ### Init the agents
    print("Creating authors")
    createAgents(int(worldConfig.get("number_of_agents")), agentsList, worldConfig)
    
    ### Creat the network of agents in world
    print("Connecting agents into the network ", end = "")
    sys.stdout.flush()
    createNetwork(int(worldConfig.get("number_of_agents")), agentsList, worldConfig)

    
    ### Run the world
    print("Starting the simulation")

    max_period = int(worldConfig.get("max_period"))
    cd = float(worldConfig.get("credit_decrese"))
    s = float(worldConfig.get("step"))

    for period in range(0, max_period + 1):
        stepText = "\tStep {:^4} / {}".format(period, max_period)
        print(len(stepText) * "\b", end = "")
        sys.stdout.flush()
        print(stepText, end = "")
        sys.stdout.flush()

        ### Lower the agents credits
        ### Generate the works        
        for ag in agentsList:
            ag.Credit = ag.Credit - cd
            work = ag.submitWork()
            if work.NumberOfAuthors > 0:
                worksList.append(work)
        
        ### Works evolution
        worksList.sort()

        wc = float(len(worksList))
        ac = float(len(agentsList))

        for l, work in enumerate(worksList):
            l = float(l)
            ### calculate the profit
            p = 2.0 * cd * ( 1.0 - ( l + 0.5 ) / wc ) / wc * ac

            ### calculate new probability
            d = s - 2.0 * l * s / wc

            ### Asign new credit for each author of work  

            newCredit = p / float(work.NumberOfAuthors)         
            for auth in work.Authors:
                auth.Credit += newCredit

            ### Adjust the probability of cooperation
            for i in range(0, len(work.Authors) - 1):
                b = work.Authors[0].getProbOfCoop(work.Authors[i + 1])
                c = work.Authors[i + 1].getProbOfCoop(work.Authors[0])
                work.Authors[0].setProbOfCoop(work.Authors[i + 1], b + d)
                work.Authors[i + 1].setProbOfCoop(work.Authors[0], c + d)

        ### Data evaluation - runs once per n_test simulation's steps
        if period % int(worldConfig.get("n_test")) == 0:    
            saveIteration = int(period / int(worldConfig.get("n_test")))

            ### Calculate the histogram of coauthors
            coauthorsHistogram = np.zeros(CONST_MAX_AUTHORS)
            for work in worksList:
                coauthorsHistogram[work.NumberOfAuthors] += 1            
            
            saveHistogram(saveIteration, coauthorsHistogram)
            saveHistogramStats(period, coauthorsHistogram)
            saveConfig(saveIteration, agentsList)
            saveProbabilitiesStats(saveIteration, agentsList)

        worksList.clear()
        
    print("\nDone :)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile", help=".xml file with input data", type = str)
    args = parser.parse_args()
    main(args)