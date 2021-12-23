import gc

class FreeResources:
    def __init__(self):
         gc.collect()
         self.free = gc.mem_free()
         self.allocated = gc.mem_alloc()
         self.total = self.free + self.allocated
         self.freePercent = '{0:.2f}%'.format(self.free/self.total*100)
    
    def __recalc(self):
        gc.collect()
        self.free = gc.mem_free()
        self.freePercent = '{0:.2f}%'.format(self.free/self.total*100)

    def memoryStats(self):
        self.__recalc()
        return ('Total:{0} Free:{1} ({2})'.format(self.total,self.free,self.freePercent))
        
    def freeMemoryPercent(self, full=False):
        self.__recalc()
        return self.freePercent
  
