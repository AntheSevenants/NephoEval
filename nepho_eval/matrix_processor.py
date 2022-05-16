from pathlib import Path
import os

class MatrixProcessor:
    def __init__(self, LEMMAS_PATH, TSV_PATH, MATRICES_PATH):
        # Create a listing of all lemmas available
        self.LEMMAS_PATH = LEMMAS_PATH
        self.lemmas = os.listdir(LEMMAS_PATH)
        self.lemmas.sort()
        
        # Save the TSV_PATH and MATRICES_PATH
        self.TSV_PATH = TSV_PATH
        self.MATRICES_PATH = MATRICES_PATH
        
    def create_filename(original_filename, lemma, suffix="", extension="npy"):
        filename_no_ext = Path(original_filename).stem
        folder = f"{self.MATRICES_PATH}/{lemma}"
        
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        filename_no_ext = filename_no_ext.replace(".tcmx.soc", "")
        
        if suffix:
            suffix = f".{suffix}"
        
        filename = f"{folder}/{filename_no_ext}{suffix}.{extension}"
    
        return filename
        
    def process(self):
        raise NotImplementedError("MatrixProcessor is not meant to be used as-is. Please build upon this method in a child of this class.")