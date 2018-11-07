

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
    
    def getProbabilityOfCooperation(self, agent):
        prob = 0.0
        ag = list(filter(lambda a: a.get("agent").Id == agent.Id, self._listOfCoworkers))
        if len(ag > 0):
            prob = ag[0].get("prob")

        return prob

    def setProbabilityOfCooperation(self, agent, newVal):
        ag = list(filter(lambda a: a.get("agent").Id == agent.Id, self._listOfCoworkers))
        if len(ag > 0):
            p = newVal
            if p < 0.0: p = 0.0
            elif p > 1.0: p = 1.0
            ag[0]["prob"] = p

    def addCoworker(self, cowrker):
        """Adds a new coworker to the list of coworkers
        
        Arguments:
            cowrker {dcit} -- {"agent": agent, "prob": prob}
        """
        self._listOfCoworkers.append(cowrker)

    def returnMe(self):
        return self

    def submitWork(self):
        raise NotImplementedError