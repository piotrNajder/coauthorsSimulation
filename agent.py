from random_gen import RandomGenerator as rg
from work import Work

class Agent():    
    """The class representing the agent in the network of cooperators"""

    def __init__(self, id, credit, activity, quality, sdQuality):
        self._id = id
        self._credit = credit
        self._activity = activity
        self._quality = quality
        self._sdQuality = sdQuality
        self._listOfCoworkers = list()

    @property
    def Id(self):
        return self._id

    @property
    def Credit(self):
        return self._credit

    @Credit.setter
    def Credit(self, newVal):
          self._credit = newVal

    @property
    def Activity(self):
        return self._activity

    @Activity.setter
    def Activity(self, newVal):
        self._activity = newVal

    @property
    def Quality(self):
        return self._quality

    @Quality.setter
    def Quality(self, newVal):
        self._quality = newVal

    @property
    def SdQuality(self):
        return self._sdQuality

    @property
    def NumberOfCoworkers(self):
        return len(self._listOfCoworkers)

    @property
    def ListOfCoworkers(self):
        return self._listOfCoworkers
    
    def getProbOfCoop(self, agent):        
        ag = next((x for x in self._listOfCoworkers if x.Agent.Id == agent.Id), None)
        if ag != None:
            return ag.Prob
        return 0.0

    def setProbOfCoop(self, agent, newVal):
        ag = next((x for x in self._listOfCoworkers if x.Agent.Id == agent.Id), None)
        if ag != None:
            p = newVal
            if p < 0.0: p = 0.0
            elif p > 1.0: p = 1.0
            ag.Prob = p

    def addCoworker(self, cowrker):       
        self._listOfCoworkers.append(cowrker)

    def returnMe(self):
        return self

    def submitWork(self):
        q = 0.0

        listOfAgents = list()

        if rg.ranf() < self._activity:
            listOfAgents.append(self)
            q = self._quality + rg.granf(m = self._sdQuality)
            for coWorker in self._listOfCoworkers:                
                if rg.ranf() < coWorker.Prob:
                    q += coWorker.Agent.Quality + rg.granf(m = coWorker.Agent.SdQuality)
                    listOfAgents.append(coWorker.Agent)

        return Work(q, listOfAgents)

class CoWorker():

    def __init__(self, agent, coopProb):
        self._agent = agent
        self._prob = coopProb

    @property
    def Agent(self):
        return self._agent

    @Agent.setter
    def Agent(self, newAg):
          self._agent = newAg

    @property
    def Prob(self):
        return float(self._prob)

    @Prob.setter
    def Prob(self, newProb):
          self._prob = float(newProb)