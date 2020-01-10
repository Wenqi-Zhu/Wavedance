import numpy as np
import pandas as pd
import numba
from numba import jit
from tqdm import tqdm
class Circuit(object):
    def Para_Check(self,Para_Dict):
        '''
        Check if parameters are enough to create a circuit.
        '''
        for Para in self.Para_List:
            if Para not in Para_Dict:
                raise CircuitParameterError("Parameters are not enough. Check your input.")
    


class _State(list):
    pass