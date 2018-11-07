from agent import Agent
from work import Work
from random_gen import RandomGenerator as rg

import argparse
import xml.etree.ElementTree as ET
import numpy as np

import os
import sys

def createAgents(numOfAgents, theList, config):
    credit = float(config.get("credit")) + float(config.get("std_credit"))
    activity = float(config.get("activity"))
    quality = float(config.get("mean_mean_quality")) + float(config.get("std_mean_quality"))
    std_quality = float(config.get("mean_std_quality")) + float(config.get("std_std_quality"))

    for i in range(0, numOfAgents + 1):
        ag = Agent(i, 
                   credit * rg.granf(),
                   activity,
                   quality * rg.granf(),
                   std_quality * rg.granf())

        theList.append(ag)

def createNetwork(numOfAgents, theList, config):
    thr = float(config.get("threshold"))
    printMarker = int(numOfAgents / 10)
    for k in range(0, numOfAgents + 1):
        if k % printMarker == 0:
            print("#", end = "")
            sys.stdout.flush()
            
        ### get two random Ids
        i = 0
        j = 0
        while(i == j):
            i = rg.iranx(numOfAgents) - 1
            j = rg.iranx(numOfAgents) - 1

        ### get agent objects for given id
        ag1 = None
        ag2 = None

        ag = list(filter(lambda a: a.Id == i, theList))
        if len(ag) > 0: ag1 = ag[0]

        ag = list(filter(lambda a: a.Id == j, theList))
        if len(ag) > 0: ag2 = ag[0]

        c = thr * rg.ranf()
        
        ag1.addCoworker({"agent": ag2, "prob": c})
        ag2.addCoworker({"agent": ag1, "prob": c})
    print("")

def saveHistogram(iteration, hist):
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    fName = os.path.join(fileDir, "results/hist{}.dat".format(iteration))
    with open(fName, "w") as f:
        for i, val in enumerate(hist):
            if val != 0:
                f.write("{} {}\n".format(i, float(val) / hist.sum()))

def saveHistogramStats(counter, hist):    
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    fName = os.path.join(fileDir, "results/w.dat")
    with open(fName, "a") as f:
        f.write("{} {} {} {}\n".format(counter, hist.mean(), hist.std(), hist.sum() ))

def saveConfig(iteration, theList):
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    fName = os.path.join(fileDir, "results/config{}.dat".format(iteration))
    with open(fName, "w") as f:
        for ag in theList:
            f.write("{} {} {}\n".format(ag.Credit, ag.Quality, ag.NumberOfCoworkers))

def saveProbabilitiesStats(iteration, theList):
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    probFName = os.path.join(fileDir, "results/probabilities{}.dat".format(iteration))
    probConfName = os.path.join(fileDir, "results/prob_conf{}.dat".format(iteration))
    with open(probFName, "w") as probF, open(probConfName, "w") as probConfF:
        for ag in theList:
            probF.write("{}".format(ag.Id))
            for coWorker in ag.ListOfCoworkers:
                probF.write("{} {}".format(coWorker.get("agent").Id, coWorker.get("prob")))
                probConfF.write("{}\n".format(coWorker.get("prob")))
            
            probF.write("\n")

def main(args):
    
    worldConfig = {}
    agentsList = list()
    worksList = list()
    
    CONST_MAX_AUTHORS = 200  # Max numbers of coauthors we expect

    xmlTree = ET.parse(args.inputFile)
    root = xmlTree.getroot()
    if root.tag != "AuthorsWorldConfig":
        print("Config file corrupted. Terminating...\n")

    for child in root:
        worldConfig[child.tag] = child.text   
    

    ### Here we have config in dictonary
    ### We cann start the init part

    ### Init the agents
    print("Creating authors")
    createAgents(int(worldConfig.get("number_of_agents")), agentsList, worldConfig)
    
    ### Creat the network of agents in world
    print("Connecting agents into the network ", end = "")
    sys.stdout.flush()
    createNetwork(int(worldConfig.get("number_of_agents")), agentsList, worldConfig)

    print("Starting the simulation")
    ### Run the world
    for period in range(0, int(worldConfig.get("max_period"))):
        stepText = "\tStep {:^4} / {}".format(period, int(worldConfig.get("max_period")))
        print(len(stepText) * "\b", end = "")
        sys.stdout.flush()
        print(stepText, end = "")
        sys.stdout.flush()

        ### Lower the agents credits
        ### Generate the works
        for ag in agentsList:
            ag.Credit = ag.Credit - float(worldConfig.get("credit_decrese"))
            work = ag.submitWork()
            if work.NumberOfAuthors > 0:
                worksList.append(work)
        
        ### Works evolution
        worksList.sort()
        for l, work in enumerate(worksList):

            ### calculate the profit
            p = 2.0 * float(worldConfig.get("credit_decrese")) * \
                ( 1.0 - ( float(l) + 0.5 ) / float(len(worksList)) ) / \
                float(len(worksList)) * float(len(agentsList))

            ### calculate new probability
            d = float(worldConfig.get("step")) - 2.0 * \
                float(l * float(worldConfig.get("step"))) / \
                float(len(worksList))

            ### Asign new credit for each author of work                
            for auth in work.Authors:
                auth.Credit += p / float(work.NumberOfAuthors)

            ### Adjust the probability of cooperation
            for i in range(0, len(work.Authors) - 1):
                b = work.Authors[0].getProbabilityOfCooperation(work.Authors[i + 1])
                c = work.Authors[i + 1].getProbabilityOfCooperation(work.Authors[0])
                work.Authors[0].setProbabilityOfCooperation(work.Authors[i + 1], b + d)
                work.Authors[i + 1].setProbabilityOfCooperation(work.Authors[0], c + d)

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