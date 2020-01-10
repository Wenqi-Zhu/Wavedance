from ..ClassDef import Circuit
import math
import numpy as np
import pandas as pd

class ClassE2DCDC(Circuit):
    BodyDiode=True

    Order=7
    Number_of_Para=13 #Number of parameters it has.

    Para_List=['A','B','H','J','D','Q0','K','Qf','rS','rD','rC','rF','r0']
    State_List=['iC','vS','vC0','iL0','vD','iF','vF']
    Output_List=['θ','iC','vS','vC0','iL0','vD','iF','vF']
    def __init__(self,**kw):
        '''
        Initialize the circuit.
        '''
        self.Para_Check(kw)

        self.A,  self.B,  self.H   = kw['A'] , kw['B'],  kw['H']
        self.J,  self.D,  self.Q0  = kw['J'] , kw['D'],  kw['Q0']
        self.K,  self.Qf, self.rS  = kw['K'] , kw['Qf'], kw['rS']
        self.rD, self.rC, self.rF  = kw['rD'], kw['rC'], kw['rF']
        self.r0 = kw['r0']

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
        if math.fmod(θ,2*π) < 2*π*self.D:#When switch is ON:
            rS = self.rS
        elif self.BodyDiode and State[1] < 0.0:
            rS = self.rS

        if State[4] < 0.0:#When diode is ON:
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
        H,Q0=self.H,self.Q0
        #Matrix A of power source with size 1x7:
        return np.array([H/Q0,0.0,0.0,0.0,0.0,0.0,0.0])

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
        A,B,H,J,Q0,K,Qf,rC,rF,r0=self.A,self.B,self.H,self.J,self.Q0,self.K,self.Qf,self.rC,self.rF,self.r0

        #Resistances of switches are determined by method "Switching"
        rS,rD=self.Switching(θ,State) 

        #Matrix B with size 7x7:
        Mat_B=np.array([
                      [-rC*H/Q0, -H/Q0,        0.0,       0.0,     0.0,          0.0,       0.0    ],
                      [A*A*B*Q0, -A*A*B*Q0/rS, -A*A*B*Q0, 0.0,     0.0,          0.0,       0.0    ],
                      [0.0,      1.0/Q0,       -r0/Q0,    -1.0/Q0, -1.0/Q0,      0.0,       0.0    ],
                      [0.0,      0.0,          A*A*Q0,    0.0,     0.0,          0.0,       0.0    ],
                      [0.0,      0.0,          A*A*J*Q0,  0.0,     -A*A*J*Q0/rD, -A*A*J*Q0, 0.0    ],
                      [0.0,      0.0,          0.0,       0.0,     1.0/Qf,       -rF/Qf,    -1.0/Qf],
                      [0.0,      0.0,          0.0,       0.0,     0.0,          Qf*K*K,    -Qf*K*K]
                      ])
        return Mat_B

    def CreateDataFrame(self,θ:float,State:np.matrix,DataFrame:pd.DataFrame)->pd.DataFrame:
        #Writing dataframe according to the state matrix.
        DataFrame=DataFrame.append({'θ':θ,
                          'iC':  State[0],
                          'vS':  State[1],
                          'vC0': State[2],
                          'iL0': State[3],
                          'vD':  State[4],
                          'iF':  State[5],
                          'vF':  State[6]},
                          ignore_index=True)
        return DataFrame