from ..ClassDef import Circuit
import math
import numpy as np
import pandas as pd

class ClassEDWPT(Circuit):
    BodyDiode=True

    Order=8
    Number_of_Para=14 #Number of parameters it has.

    Para_List=['A','B','Q','H','N','k','U','S','J','Ds','rL1','rL2','rS','rD']
    State_List=['iC','vS','v1','i1','i2','v2','vD1','vO']
    Output_List=['θ','iC','vS','v1','i1','i2','v2','vD1','vD2','vO']
    def __init__(self,**kw):
        '''
        Initialize the circuit.
        '''
        self.Para_Check(kw)
        self.A,   self.B,   self.Q   = kw['A'] ,  kw['B'],   kw['Q']
        self.H,   self.N,   self.k   = kw['H'] ,  kw['N'],   kw['k']
        self.S,   self.J,   self.Ds  = kw['S'] ,  kw['J'],   kw['Ds']
        self.rL1, self.rL2, self.rS  = kw['rL1'], kw['rL2'], kw['rS']
        self.rD,  self.U             = kw['rD'],  kw['U']

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
        rS , rD1, rD2 = 1e10 , 1e10, 1e10
        vS,vD1,vD2=State[1],State[6],-(State[6]+State[7])

        if math.fmod(θ,2*π) < 2*π*self.Ds:#When switch is ON:
            rS = self.rS
        elif self.BodyDiode and vS < 0.0:
            rS = self.rS

        if vD1 > 0.0:#When D1 is ON:
            rD1=self.rD
        if vD2 > 0.0:#When D2 is ON:
            rD2=self.rD
        return rS,rD1,rD2

    def MatA(self,θ:float) -> np.matrix:
        '''
        Calculating the power source matrix (MatA)

        Parameters:
            1.θ:float (Angular time of the input (unused for this circuit))
        It returns:
            MatA:A matrix with size 1x7
        '''
        A,H,Q=self.A,self.H,self.Q
        #Matrix A of power source with size 1x7:
        return np.array([A/(Q*H),0.0,0.0,0.0,0.0,0.0,0.0,0.0])

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
        A,B,Q,H,N,k,U,S,J,rL1,rL2=self.A,self.B,self.Q,self.H,self.N,self.k,self.U,self.S,self.J,self.rL1,self.rL2
        #A/=f
        #Resistances of switches are determined by method "Switching"
        rS,rD1,rD2=self.Switching(θ,State) 
        T1   =   A/(Q*(1-k**2))
        T2   =   T1*k*math.sqrt(N)
        T3   =   T1 * N
        T4   =   A*J*Q/(2.0+S/J)
        T5   =   A*S*Q/(2.0+S/J)
        T6   =   A*J*S*Q/(2*J+S)
        #Matrix B with size 8x8:
        Mat_B=np.array([
                    #  iC           vS         v1          i1        i2              v2      vD1                           vo
                      [0.0,      -A/(Q*H),    0.0,         0.0,      0.0,            0.0,    0.0,                          0.0             ],#d iC/dθ
                      [A*B*Q,    -A*B*Q/rS,   0.0,         -A*B*Q,   0.0,            0.0,    0.0,                          0.0             ],#d vS/dθ
                      [0.0,      0.0,         0.0,         A*Q,      0.0,            0.0,    0.0,                          0.0             ],#d v1/dθ
                      [0.0,      T1,          -T1,         -rL1*T1,  -rL2*T2,        -T2,    T2,                           0.0             ],#d i1/dθ
                      [0.0,      T2,          -T2,         -rL1*T2,  -rL2*T3,        -T3,    T3,                           0.0             ],#d i2/dθ
                      [0.0,      0.0,         0.0,         0.0,      A*U*Q,          0.0,    0.0,                          0.0             ],#d v2/dθ
                      [0.0,      0.0,         0.0,         0.0,      -T4-T5,         0.0,    -T4*(1.0/rD1+1.0/rD2)-T5/rD1, -T4/rD2+T5      ],#d vD1/dθ
                      [0.0,      0.0,         0.0,         0.0,      -T6,            0.0,    (1.0/rD1-1.0/rD2)*T6,         -(2.0+1/rD2)*T6   ] #d vo/dθ
                      ])
        return Mat_B

    def CreateDataFrame(self,θ:float,State:np.matrix,DataFrame:pd.DataFrame)->pd.DataFrame:
        #Writing dataframe according to the state matrix.
        DataFrame=DataFrame.append({'θ':θ,
                          'iC':   State[0],
                          'vS':   State[1],
                          'v1':   State[2],
                          'i1':   State[3],
                          'i2':   State[4],
                          'v2':   State[5],
                          'vD1':  State[6],
                          'vD2':  -State[7]-State[6],
                          'vO':   State[7],
                          },
                          ignore_index=True)
        return DataFrame