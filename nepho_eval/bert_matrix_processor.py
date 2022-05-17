from .matrix_processor import MatrixProcessor
from .pipeline import Pipeline
from tqdm.auto import tqdm

import pandas as pd

class BertMatrixProcessor(MatrixProcessor):
    def process(self, do_reduce=False, do_transform=False):
        for lemma in tqdm(self.lemmas):
            models = list(pd.read_csv(f"{self.TSV_PATH}/{lemma}/{lemma}.models.tsv", sep="\t")["_model"])
    
            for model in tqdm(models, leave=False):
                prefix = f"{self.LEMMAS_PATH}/{lemma}/"
                filename = f"{model}.npy"
        
                matrix_path = f"{prefix}{filename}"
                token_ids_path = f"{prefix}token_ids.json"
        
                # Load the TT-matrix
                pipeline = Pipeline(matrix_path, is_bert=True)
            
                # Attach token ids
                pipeline.load_token_ids(token_ids_path)
        
                if do_reduce:
                    pipeline.reduce(do_reduce)
            
                pipeline.compute_distance_matrix()
            
                if do_transform:
                    pipeline.log_transform()
            
                # Save the matrix in its entirety
                pipeline.save_matrix(self.create_filename(filename, lemma, suffix="soc"))
        
                # Save the distance matrix
                pipeline.save_distance_matrix(self.create_filename(filename, lemma, suffix="dist"))
        
                # Save token ids
                pipeline.save_token_ids(self.create_filename(filename,
                                                            lemma,
                                                            suffix="ids",
                                                            extension="tsv"))