import time
import json

class SegundaChanceEhRelogio: 
    def __init__(self, frames, pages, totalPages, accesses):
        self.frames = frames
        self.pages = pages
        self.totalPages = totalPages
        self.pageFaults = 0
        self.frameList = []
        self.ref = []
        self.totalTime = 0
        self.accessCount = 0
        self.accesses = accesses

    def remove(self):
        self.frameList.pop(0)

    def add(self, page):
        if page > self.totalPages:
            print("Error: Page not in range")
        else:
            self.frameList.append(page)

    def pageFault(self, page):
        startTime = time.perf_counter()
        if page not in self.frameList:
            self.pageFaults += 1
            if len(self.frameList) == self.frames:
                while self.ref[0] == 1:
                    self.ref.pop(0)
                    self.ref.append(0)
                    self.frameList.append(self.frameList.pop(0))

                self.remove()
                self.add(page)
                self.ref.append(1)
                self.ref.pop(0)
            else: 
                self.add(page)
                self.ref.append(1)
        else:
            self.ref[self.frameList.index(page)] = 1
        endTime = time.perf_counter()  
        self.totalTime += endTime - startTime
        self.accessCount += 1

    def accessPages(self):
        for page in self.pages:
            self.pageFault(page)
    
    def results(self): 
        self.accessPages()

        print("-------------------SEGUNDA CHANCE E RELOGIO-------------------")
        print("Page Faults: ", self.pageFaults)
        print("Page Fault Rate: ", self.pageFaults / self.accesses * 100, "%")
        print("Total Time: ", self.totalTime * 1000, "ms")
        print("Average Access Time: ", self.totalTime / self.accessCount * 1000, "ms")

        


