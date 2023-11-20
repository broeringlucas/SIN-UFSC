import time


class FIFO: 
    def __init__(self, frames, pages, totalPages, accesses):
        self.frames = frames
        self.pages = pages
        self.totalPages = totalPages
        self.pageFaults = 0
        self.frameList = []
        self.totalTime = 0
        self.accessCount = 0    
        self.accesses = accesses

    def remove(self):
        self.frameList.pop(0)

    def add(self, page):
        if len(self.frameList) > self.totalPages:
            print("Error: Page not in range")
        else:
            self.frameList.append(page)

    def pageFault(self, page):
        startTime = time.perf_counter()
        if page not in self.frameList:
            self.pageFaults += 1
            if len(self.frameList) == self.frames:
                self.remove()
                self.add(page)
            else: 
                self.add(page)
        endTime = time.perf_counter()  
        self.totalTime += endTime - startTime
        self.accessCount += 1


    def accessPages(self):
        for page in self.pages:
            self.pageFault(page)

    def results(self): 
        self.accessPages()

        print("-------------------FIFO-------------------")
        print("Page Faults: ", self.pageFaults)
        print("Page Fault Rate: ", self.pageFaults / self.accesses * 100, "%")
        print("Total Time: ", self.totalTime * 1000, "ms")
        print("Average Access Time: ", self.totalTime / self.accessCount * 1000, "ms")


