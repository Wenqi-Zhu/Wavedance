import numpy as np
from math import pi as π
import numpy as np

def BDF_4(
        States:np.array,
        MatA:np.matrix,
        MatB:np.matrix,
        h:float
        )-> np.matrix:
        '''
        4-order Backward Differential Formula:

        Parameters:
            1.State (List of last 4 states)
            2.MatA (Power source matrix A of the circuit)
            3.MatB (CircuitMatB_Inv matrix B)
            4.h (Step size per one step)
        '''
        #Order = np.size(MatA,0)
        Order = 8
        MatB = MatB * h - 25.0/12.0*np.identity(Order)
        MatA = -h*MatA-States[0]*4.0+States[1]*3.0-States[2]*(4.0/3.0)+States[3]*0.25
        MatB_Inv = np.linalg.inv(MatB)
        Result = np.dot(MatB_Inv,MatA)
        return Result
