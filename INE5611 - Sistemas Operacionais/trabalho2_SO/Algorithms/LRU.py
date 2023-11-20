import time
import json

class LRU: 
    def __init__(self, frames, pages, totalPages, accesses):
        self.frames = frames
        self.pages = pages
        self.totalPages = totalPages
        self.pageFaults = 0
        self.frameList = []
        self.indexes = {}
        self.accesses = accesses
        self.totalTime = 0
        self.accessCount = 0

    def add(self, page):
        if len(self.frameList) > self.frames:
            print("Error: Page not in range")
        else:
            self.frameList.append(page)
            self.indexes[page] = len(self.frameList) - 1 

    def pageFault(self, page):
        startTime = time.perf_counter()
        if page not in self.frameList:
            self.pageFaults += 1
            if len(self.frameList) == self.frames:
                lru = float('inf')
                pageToRemove = None
                for existing_page in self.frameList:
                    if self.indexes[existing_page] < lru:
                        lru = self.indexes[existing_page]
                        pageToRemove = existing_page

                if pageToRemove is not None:
                    self.frameList.remove(pageToRemove)
                    self.add(page)
            else: 
                self.add(page)
        else:
            self.indexes[page] = len(self.frameList) - 1

        endTime = time.perf_counter()
        self.totalTime += endTime - startTime
        self.accessCount += 1

    def accessPages(self):
        for page in self.pages:
            self.pageFault(page)

    def results(self): 
        self.accessPages()

        print("-------------------LRU-------------------")
        print("Page Faults: ", self.pageFaults)
        print("Page Fault Rate: ", self.pageFaults / self.accesses * 100, "%")
        print("Total Time: ", self.totalTime * 1000, "ms")
        print("Average Access Time: ", self.totalTime / self.accessCount * 1000, "ms")


