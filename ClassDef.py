from ErrorDefine import *
from Solver import *
from math import pi
import numpy as np
import pandas as pd
from tqdm import tqdm
class Circuit(object):
    def Para_Check(self,Para_Dict):
        '''
        Check if parameters are enough to create a circuit.
        '''
        for Para in self.Para_List:
            if Para not in Para_Dict:
                raise CircuitParameterError("Parameters are not enough. Check your input.")
    
    def Run(
        self,
        θ_Interval:tuple,
        Initial_State:np.matrix,
        Step=200,
        Output_Record=True,
        Silent=False):
        '''
        Run simulation for this circuit.
        '''
        Record=pd.DataFrame()
        Start_θ, Record_θ, End_θ = 0.0, θ_Interval[0], θ_Interval[1] 
        if Record_θ > End_θ:
            raise CircuitParameterError("Record_θ cannot be larger than End_θ!")
        Period = End_θ / (2.0 * pi)
        TotalStep = int(Period * Step)
        θSpace, StepSize = np.linspace(Start_θ,End_θ,num=TotalStep,retstep=True)
        if not Silent:
            θSpace = tqdm(θSpace)
        States=[Initial_State]*4
        
        for θ in θSpace:
            Mat_A=self.MatA(θ)
            Mat_B=self.MatB(θ,States[0])
            States = [BDF_4(States,Mat_A,Mat_B,StepSize)] + States
            if Output_Record and θ > Record_θ:
                Record=self.CreateDataFrame(θ,States[0],Record)
            States.pop

        if not Output_Record:
            Record=self.CreateDataFrame(θ,States[0],Record)
        #Adjust the order of output record
        Record=Record[self.Output_List]
        return Record


class _State(list):
    pass