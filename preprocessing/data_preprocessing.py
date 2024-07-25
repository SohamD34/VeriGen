import re
import random
import sys
import os
import pandas as pd 
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.functions import comment_lines, randomize_operators, randomize_variable_names

data = pd.read_csv('../data/df.csv')
mini_data = data.sample(n=5000)
