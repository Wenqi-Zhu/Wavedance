from ..ClassDef import Circuit
import math
import numpy as np
import pandas as pd

class ClassE2DCDCISO(Circuit):
    BodyDiode=True

    Order=7
    Number_of_Para=14 #Number of parameters it has.

    Para_List=['A','B','H','J','Ds','Q1','kTX','NTX','K','rS','rD','rC','r1','r2']
    State_List=['iC','vS','vC0','i1','i2','vD','vO']
    Output_List=['θ','iC','vS','vC0','i1','i2','vD','vO']
    def __init__(self,**kw):
        '''
        Initialize the circuit.
        '''
        self.Para_Check(kw)
        #Read parameters
        self.A,   self.B,   self.H  = kw['A']   , kw['B'],   kw['H']
        self.J,   self.Ds,  self.Q1 = kw['J']   , kw['Ds'],  kw['Q1']
        self.kTX, self.NTX, self.K  = kw['kTX'] , kw['NTX'], kw['K']
        #Read parasitic resistances
        self.rD, self.rC, self.rS  = kw['rD'], kw['rC'], kw['rS']
        self.r1, self.r2  = kw['r1'], kw['r2']

        if 'BodyDiode' in kw: self.BodyDiode=kw['BodyDiode']
        

    def Switching(self,θ:float,State:np.matrix) -> tuple:
        """
        This function decides the state of every switches in the circuit.

        Parameters:
            1.θ (angular time)
            2.State (current state of the circuit)
        It returns:
            an tuple with 0 or 1, indicating each switch is ON or OFF
        e.g. (0,1,0) means (OFF,ON,OFF)
        """
        π=math.pi
        rS , rD = 1e10 , 1e10
        if math.fmod(θ,2*π) < 2*π*self.Ds:#When switch is ON:
            rS = self.rS
        elif self.BodyDiode and State[1] < 0.0:
            rS = self.rS

        if State[5] > 0.0:#When diode is ON:
            rD=self.rD
        return rS,rD

    def MatA(self,θ:float) -> np.matrix:
        '''
        Calculating the power source matrix (MatA)

        Parameters:
            1.θ:float (Angular time of the input (unused for this circuit))
        It returns:
            MatA:A matrix with size 1x7
        '''
        H,Q1=self.H,self.Q1
        #Matrix A of power source with size 1x7:
        return np.array([H/Q1,0.0,0.0,0.0,0.0,0.0,0.0])

    def MatB(self,θ:float,State:np.matrix) -> np.matrix:
        '''
        Calculating the differentiation of states.

        Parameters:
            θ: Current angular time.
            State: Current State
        It returns:
            A _State, including the differentiation of states (dx/dθ)
        '''
        #Read temperaly variables from the circuit:
        A2,B,H,J,Q1,kTX,NTX,K=self.A**2,self.B,self.H,self.J,self.Q1,self.kTX,self.NTX,self.K
        rC,r1,r2 = self.rC,self.r1,self.r2
        #Resistances of switches are determined by method "Switching"
        rS,rD=self.Switching(θ,State) 

        T1=1.0/(1.0-kTX**2)/Q1
        T2=kTX*NTX/(1.0-kTX**2)/Q1
        T3=NTX*NTX/(1.0-kTX**2)/Q1

        #Matrix B with size 7x7:
        Mat_B=np.array([#iC      vS           vC0     i1        i2       vD      vO
                      [-rC*H/Q1, -H/Q1,       0.0,    0.0,      0.0,     0.0,         0.0     ],#d iC/dθ
                      [A2*B*Q1,  -A2*B*Q1/rS, 0.0,    -A2*B*Q1, 0.0,     0.0,         0.0     ],#d vS/dθ
                      [0.0,      0.0,         0.0,    A2*Q1,    0.0,     0.0,         0.0     ],#d vC0/dθ
                      [0.0,      T1,          -T1,    -r1*T1,   -T2*r2,   -T2,        -T2     ],#d i1/dθ
                      [0.0,      T2,          -T2,    -r1*T2,   -T3*r2,   -T3,        -T3     ],#d i2/dθ
                      [0.0,      0.0,         0.0,    0.0,      A2*J*Q1, -A2*J*Q1/rD, 0.0     ],#d vD/dθ
                      [0.0,      0.0,         0.0,    0.0,      A2*K*Q1,   0.0,       -A2*K*Q1] #d vO/dθ
                      ])
        return Mat_B

    def CreateDataFrame(self,θ:float,State:np.matrix,DataFrame:pd.DataFrame)->pd.DataFrame:
        #Writing dataframe according to the state matrix.
        DataFrame=DataFrame.append({'θ':θ,
                          'iC':  State[0],
                          'vS':  State[1],
                          'vC0': State[2],
                          'i1':  State[3],
                          'i2':  State[4],
                          'vD':  State[5],
                          'vO':  State[6]},
                          ignore_index=True)
        return DataFrame
        