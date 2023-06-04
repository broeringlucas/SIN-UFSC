class NodeQuestion:
    def __init__(self, question, yesQ=None, noQ=None):
        self.__question = question 
        self.__yesQ = yesQ
        self.__noQ = noQ 

    @property
    def question(self):
        return self.__question
    
    @property
    def yesQ(self):
        return self.__yesQ
    
    @property
    def noQ(self):
        return self.__noQ 
    
    @yesQ.setter
    def yesQ(self, new_yesQ):
        self.__yesQ = new_yesQ

    @noQ.setter
    def noQ(self, new_noQ):
        self.__noQ = new_noQ
    