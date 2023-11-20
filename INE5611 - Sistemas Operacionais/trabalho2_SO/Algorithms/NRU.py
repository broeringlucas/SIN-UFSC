import random 
import time
import json

class NRU: 
    def __init__(self, frames, pages, totalPages, accessTohReset, accesses):
        self.frames = frames
        self.pages = pages
        self.totalPages = totalPages
        self.pageFaults = 0
        self.frameList = []
        self.ref = []
        self.mod = []
        self.totalTime = 0
        self.accessCount = 0
        self.resetCount = 0 
        self.accessTohReset = accessTohReset
        self.full = False
        self.class0 = []
        self.class1 = []
        self.class2 = []
        self.class3 = []
        self.accesses = accesses

    def add(self, page):
        if page > self.totalPages:
            print("Error: Page not in range")
        else:
            self.frameList.append(page)

    def pageFault(self, page):
        startTime = time.perf_counter()

        full = False

        if page not in self.frameList:
            self.pageFaults += 1
            if len(self.frameList) == self.frames:
                full = True
            else: 
                self.add(page)
                self.ref.append(0)
                self.mod.append(0)
        else:
            self.ref[self.frameList.index(page)] = 1
            self.mod[self.frameList.index(page)] = 1

        if full:
            if len(self.class0) > 0:
                random_page = random.choice(self.class0)
                index = self.frameList.index(random_page)
                self.frameList[index] = page
                self.ref[index] = 0
                self.mod[index] = 0
                self.class0.remove(random_page)

            elif len(self.class1) > 0:
                random_page = random.choice(self.class1)
                index = self.frameList.index(random_page)
                self.frameList[index] = page
                self.ref[index] = 0
                self.mod[index] = 0
                self.class1.remove(random_page)
            
            elif len(self.class2) > 0:
                random_page = random.choice(self.class2)
                index = self.frameList.index(random_page)
                self.frameList[index] = page
                self.ref[index] = 0
                self.mod[index] = 0
                self.class2.remove(random_page)

            elif len(self.class3) > 0:
                random_page = random.choice(self.class3)
                index = self.frameList.index(random_page)
                self.frameList[index] = page
                self.ref[index] = 0
                self.mod[index] = 0
                self.class3.remove(random_page)

        for i in range(len(self.frameList)):
            if self.ref[i] == 0 and self.mod[i] == 0:
                if self.frameList[i] in self.class0:
                   pass
                else:
                    self.class0.append(self.frameList[i])
            elif self.ref[i] == 0 and self.mod[i] == 1:
                if self.frameList[i] in self.class1:
                   pass
                else:
                    self.class1.append(self.frameList[i])
            elif self.ref[i] == 1 and self.mod[i] == 0:
                if self.frameList[i] in self.class2:
                   pass
                else:
                    self.class2.append(self.frameList[i])
            elif self.ref[i] == 1 and self.mod[i] == 1:
                if self.frameList[i] in self.class3:
                   pass
                else:
                    self.class3.append(self.frameList[i])


        endTime = time.perf_counter()  
        self.totalTime += endTime - startTime
        self.accessCount += 1
        self.resetCount += 1

        if self.resetCount == self.accessTohReset:
            for i in range(len(self.frameList)):
                self.ref[i] = 0
            self.resetCount = 0 

    def accessPages(self):
        for page in self.pages:
            self.pageFault(page)

    def results(self): 
        self.accessPages()

        print("-------------------NRU-------------------")
        print("Page Faults: ", self.pageFaults)
        print("Page Fault Rate: ", self.pageFaults / self.accesses * 100, "%")
        print("Total Time: ", self.totalTime * 1000, "ms")
        print("Average Access Time: ", self.totalTime / self.accessCount * 1000, "ms")

        