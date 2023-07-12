from model import Explainer
import os
from tqdm import tqdm

ROOT = "docs/"
summarizer = Explainer()
for filename in tqdm(os.listdir(ROOT)): 
    path = os.path.join(ROOT, filename)
    summarizer(path)
    