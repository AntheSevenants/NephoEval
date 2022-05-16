from pathlib import Path
import os

def create_filename(original_filename, lemma, suffix="", extension="npy"):
    filename_no_ext = Path(original_filename).stem
    folder = f"{MATRICES_PATH}/{lemma}"
    
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    filename_no_ext = filename_no_ext.replace(".tcmx.soc", "")
        
    if suffix:
        suffix = f".{suffix}"
        
    filename = f"{folder}/{filename_no_ext}{suffix}.{extension}"
    
    return filename