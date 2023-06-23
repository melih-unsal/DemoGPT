from model import Summarizer
import os
from tqdm import tqdm

ROOT = "../documents/langchain"
summarizer = Summarizer()
for filename in tqdm(os.listdir(ROOT)): 
    path = os.path.join(ROOT, filename)
    summarizer(path)
    