import numpy as np
import numba
from numba import jit
from .ClassDef import Circuit
from math import pi as π
from .ErrorDefine import *
import numpy as np

@jit(nopython=True)
def Simulator(
    Circuit:Circuit,
    θ_Interval:tuple,
    Initial_State:np.matrix,
    Step=100,
    Output_Record=True):
    '''
    Run simulation for this circuit.
    '''
    Record=np.hstack((0.0,Initial_State))
    Start_θ, Record_θ, End_θ = 0.0, θ_Interval[0], θ_Interval[1] 
    if Record_θ > End_θ:
        raise CircuitParameterError("Record_θ cannot be larger than End_θ!")
    Period = End_θ / (2.0 * π)
    TotalStep = int(Period * Step)
    θSpace, StepSize = np.linspace(Start_θ,End_θ,num=TotalStep,retstep=True)
    States=[Initial_State]*4
    
    for θ in θSpace:
        Mat_A=Circuit.MatA(θ)
        Mat_B=Circuit.MatB(θ,States[0])
        States = [BDF_4(States,Mat_A,Mat_B,StepSize)] + States
        if Output_Record and θ > Record_θ:
            Line=np.hstack(([θ],States[0]))
            Record.append(Line)
        States.pop

    if not Output_Record:
        Record+=[θ]+States[0]
    #Adjust the order of output record
    return Record
@jit(nopython=True)
def BDF_4(
        States:list,
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
        Order = 7
        Diag=-25.0/12.0*np.identity(Order)
        MatB = MatB * h + Diag
        MatA = -h*MatA-States[0]*4.0+States[1]*3.0-States[2]*(4.0/3.0)+States[3]*0.25
        MatB_Inv = np.linalg.inv(MatB)
        Result = np.dot(MatB_Inv,MatA)
        return Result