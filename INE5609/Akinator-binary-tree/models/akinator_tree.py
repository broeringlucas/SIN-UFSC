class AkinatorTree:
    def __init__(self, root=None): 
        self.__root = root 

    @property
    def root(self):
        return self.__root 
    
    @root.setter
    def root(self, new_root):
        self.__root = new_root
    