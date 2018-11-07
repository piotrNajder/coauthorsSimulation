from agent import Agent
from work import Work
import argparse
import xml.etree.ElementTree as ET
import numpy as np

worldConfig = {}
agentsList = list()
worksList = list()

CONST_MAX_AUTHORS = 200  # Max numbers of coauthors we expect
coauthorsHistogram = np.zeros(CONST_MAX_AUTHORS)     

def granf():
    pass

def iranx():
    pass

def ranf():
    pass

def createAgents(numOfAgents):
    credit = float(worldConfig.get("credit")) + float(worldConfig.get("std_credit"))
    activity = float(worldConfig.get("activity"))
    quality = float(worldConfig.get("mean_mean_quality")) + float(worldConfig.get("std_mean_quality"))
    std_quality = float(worldConfig.get("mean_std_quality")) + float(worldConfig.get("std_std_quality"))

    for i in range(0, numOfAgents + 1):
        ag = Agent(i, 
                   credit * granf(),
                   activity,
                   quality * granf(),
                   std_quality * granf())

        agentsList.append(ag)

def createNetwork(numOfAgents):
    for k in range(0, numOfAgents + 1):
        ### get two random Ids
        i = 0
        j = 0
        while(i == j):
            i = iranx(numOfAgents) - 1
            j = iranx(numOfAgents) - 1

        ### get agent objects for given id
        ag1 = None
        ag2 = None

        ag = list(filter(lambda a: a.Id == i, agentsList))
        if len(ag > 0): ag1 = ag[0]

        ag = list(filter(lambda a: a.Id == j, agentsList))
        if len(ag > 0): ag2 = ag[0]

        c = float(worldConfig.get("threshold")) * ranf()
        
        ag1.addCoworker({"agent": a2, "prob": c})
        ag2.addCoworker({"agent": a1, "prob": c})   


def main(args):    
    
    xmlTree = ET.parse(args.inputFile)
    root = xmlTree.getroot()
    if root.tag != "AuthorsWorldConfig":
        print("Config file corrupted. Terminating...\n")

    for child in root:
        worldConfig[child.tag] = child.text

    ### Here we have config in dictonary
    ### We cann start the init part

    ### Init the agents
    createAgents(int(worldConfig.get("number_of_agents")))
    
    ### Creat the network of agents in world
    createNetwork(int(worldConfig.get("number_of_agents")))

    ### Run the world
    for period in range(0, int(worldConfig.get("max_period"))):
        print("Step {}".format(period))

        ### Lower the agents credits
        ### Generate the works
        for ag in agentsList:
            ag.Credit = ag.Credit - float(worldConfig.get("credit_decrese"))
            work = ag.submitWork()
            if work.NumberOfAuthors > 0: worksList.append(work)
        
        ### Works evolution
        worksList.sort()
        for l, work in enumerate(worksList):

            ### calculate the profit
            p = 2.0 * float(worldConfig.get("credit_decrese") *
                ( 1.0 - ( float(l) + 0.5 ) / float(len(worksList)) ) /
                float(len(worksList)) * float(len(agentsList))

            ### calculate new probability
            d = float(worldConfig.get("step") - 2.0 *
                float(l * worldConfig.get("step")) / 
                float(len(worksList))

            ### Asign new credit for each author of work                
            for auth in work.Authors:
                auth.Credit += p / float(work.NumberOfAuthors)

            ### Adjust the probability of cooperation
            for i in range(0, len(work.Authors) - 1):
                b = auth[0].getProbabilityOfCooperation(auth[i + 1])
                c = auth[i + 1].getProbabilityOfCooperation(auth[0])
                auth[0].setProbabilityOfCooperation(auth[i + 1], b + d)
                auth[i + 1].setProbabilityOfCooperation(auth[0], c + d)

        ### Data evaluation       
        if period % int(worldConfig.get("n_test")) == 0:
            coauthorsHistogram.fill(0)

            for work in worksList:
                coauthorsHistogram[work.NumberOfAuthors] += 1

            fName = "hist{}.dat".format(period / int(worldConfig.get("n_test")))

            with open(fName, "w") as f:
                for i, val in enumerate(coauthorsHistogram):
                    if val != 0:
                        f.write("{} {}\n".format(i, float(val) / coauthorsHistogram.sum()))

            


            


        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile", help=".xml file with input data", type = str)
    args = parser.parse_args()
    main(args)