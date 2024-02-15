from network import Network
import numpy as np
import pickle
import os
from typing import MutableSequence

def checkpoint(population: MutableSequence[Network], generation_number: int, filepath: str) -> None:
    with open(f'{filepath}/{generation_number}.pkl', 'wb') as f:
        pickle.dump(population, f)

def load_checkpoint(filepath:str) -> MutableSequence[Network]:
    with open(f'{filepath}', 'rb') as f:
        population = pickle.load(f)
    
    return population