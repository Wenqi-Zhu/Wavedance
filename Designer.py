from ClassDef import Circuit
import math
from math import pi as π
import numpy as np
import pandas as pd
from ErrorDefine import *
def GetF(R:pd.DataFrame,Vo:float)->tuple:
        #Step 1: Get vS2π (Last one of the dataframe)
        F1=R.vS.iloc[-1]
        
        #Step 2: Get dvS/dtiC
        F2=R.iC.iloc[-1]-R.i1.iloc[-1]

        #Step 3： Get Vo(Average)
        F3=R['vO'].mean()-Vo

        return F1,F2,F3

def Designer(C:Circuit,Vo:float):
    Iter=0
    C.BodyDiode=False
    #Read in parameters to be designed
    λ=np.matrix([[ C.A, C.B, C.Q ]])

    #A very small delta
    Delta=1e-6

    #Target tuple
    #When the F1-F3 is smaller than their target,
    #the designer will stop and output.
    Target=(5e-3,1e-2,5e-3)

    #Time to start record and end
    #(θ_StartRecord, θ_End)
    SimulatorIntv=(200.*π,202.*π)
    
    #Initial state (zero 8x1 matrix)
    Initial_State=np.zeros(8)

    while True:
        print('Iteration:',Iter,'\n')
        print('     A:',λ[0,0],'B:',λ[0,1],'Q:',λ[0,2],'\n')
        print('     Calculating:F','\n')
        
        Iter+=1

        C.A, C.B, C.Q = λ[0,0], λ[0,1], λ[0,2]

        #Run simulator to get waveform
        Result=C.Run(SimulatorIntv, Initial_State,200, True, True)

        F1, F2, F3 = GetF(Result,Vo)
        F=np.mat([[F1, F2, F3]])
        print('     F:',F,'\n')

        #Convergence Detection
        if math.isnan(F1) or abs(F1)>1e5:
            raise ConvergenceError(
        """
        Oops! Designer failed to convergence!😯
            Please check your initial circuit.
            This problem may caused by that the TargetVo is far from 
            the output voltage of the intial circuit.
            Consider adjust TargetVo a liitle bit once a time.
            e.g. 2.8→2.7→2.6→2.5 instead of 2.8→2.5
            """)
        if abs(F1)<Target[0] and abs(F2)<Target[1] and abs(F3)<Target[2]:
            break
        dF=np.zeros((3,3))
        print('     Calculating:dF')
        for i in (0,1,2):

            λ[0,i]+=Delta
            C.A, C.B, C.Q = λ[0,0], λ[0,1], λ[0,2]
            #Run simulator to get waveform
            Result=C.Run(SimulatorIntv,Initial_State,200, True, True)
            dF1, dF2, dF3 = GetF(Result,Vo)
            dF[i]=[(dF1-F1)/Delta, (dF2-F2)/Delta, (dF3-F3)/Delta]
            λ[0,i]-=Delta
        print('     dF:',dF,'\n')
        FInv=np.linalg.inv(dF)
        FNext=F*FInv
        λ=λ-FNext
    print('Design Successful!😁\n')
    print('A:',λ[0,0],'B:',λ[0,1],'Q:',λ[0,2],'\n')
    C.BodyDiode=True
    return C