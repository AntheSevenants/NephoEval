from .matrix_processor import MatrixProcessor
from .pipeline import Pipeline
from tqdm.auto import tqdm

import pandas as pd

import shutil

class CountMatrixProcessor(MatrixProcessor):
    def __init__(self, LEMMAS_PATH, TSV_PATH, TEMP_PATH, MATRICES_PATH):
        super().__init__(LEMMAS_PATH, TSV_PATH, MATRICES_PATH)
        self.TEMP_PATH = TEMP_PATH
    
    def process(self, do_reduce=False):
        for lemma in tqdm(self.lemmas):
            models = list(pd.read_csv(f"{self.TSV_PATH}/{lemma}/{lemma}.models.tsv", sep="\t")["_model"])
    
            for model in tqdm(models, leave=False):
                prefix = f"{self.LEMMAS_PATH}/{lemma}/"
                filename = f"{model}.tcmx.soc.pac"
        
                archive_path = f"{prefix}{filename}"
                temp_path = f"{self.TEMP_PATH}{filename}"
            
                # Copy to temp first (I don't have permissions)
                shutil.copyfile(archive_path, temp_path)
        
                # Load the TT-matrix
                pipeline = Pipeline(temp_path)
        
                if do_reduce:
                    pipeline.reduce(dim_tsne)
            
                pipeline.compute_distance_matrix()
            
                # Save the matrix in its entirety
                pipeline.save_matrix(self.create_filename(filename, lemma, suffix="soc"))
        
                # Save the distance matrix
                pipeline.save_distance_matrix(self.create_filename(filename, lemma, suffix="dist"))
            
                # Save token ids
                pipeline.save_token_ids(self.create_filename(filename,
                                                            lemma,
                                                            suffix="ids",
                                                            extension="tsv"))