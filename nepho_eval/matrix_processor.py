import os

class MatrixProcessor:
    def __init__(self, LEMMAS_PATH):
        self.lemmas = os.listdir(LEMMAS_PATH)
        self.lemmas.sort()
        
    def process(self):
        raise NotImplementedError("MatrixProcessor is not meant to be used as-is. Please build upon this method in a child of this class.")