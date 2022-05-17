import json
import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances
import scipy.stats
from nephosem import TypeTokenMatrix

class Pipeline:
    def __init__(self, soc_filename, is_bert=False):
        if not is_bert:
            self.tt_matrix = TypeTokenMatrix.load(soc_filename)
            self.token_ids = self.tt_matrix.row_items
            self.soc_matrix = self.tt_matrix.matrix.A
        else:
            self.soc_matrix = np.load(soc_filename)
        
        self.reduced_soc_matrix = None
        
    def load_token_ids(self, token_ids_filename):
        with open(token_ids_filename, "rt") as reader:
            self.token_ids = json.loads(reader.read())
        
    # Apply the given dimension reduction technique to this matrix
    def reduce(self, dimension_reduction_technique):
        self.reduced_soc_matrix = dimension_reduction_technique.reduce(self.soc_matrix)
        
    def compute_distance_matrix(self):
        matrix = self.reduced_soc_matrix if self.reduced_soc_matrix is not None else self.soc_matrix
        self.distance_matrix = pairwise_distances(matrix, metric="cosine")
        
    def log_transform(self):
        ranks = scipy.stats.rankdata(self.distance_matrix)
    
        transform_func = lambda rank: np.log(1 + np.log(rank))
        transform_func = np.vectorize(transform_func)
    
        transformed_vector = transform_func(ranks)
        self.distance_matrix = transformed_vector
        
    def save_matrix(self, filename):
        np.save(filename, self.soc_matrix.astype(np.float64))
    
    def save_distance_matrix(self, filename):
        np.save(filename, self.distance_matrix.astype(np.float64))
        
    def save_token_ids(self, filename):
        data = { "_id": self.token_ids }
        df = pd.DataFrame(data)
        df.to_csv(filename, sep="\t", index=False)