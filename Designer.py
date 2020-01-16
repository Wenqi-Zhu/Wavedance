from ClassDef import Circuit
import math
from math import pi as π
import numpy as np
import pandas as pd
from ErrorDefine import *


def getF(r: pd.DataFrame, Vo: float) -> tuple:
    '''
    This function calculates the F Matrix of the Newton's Method
    based on the waveform.

    Args:
        r: Waveform
        Vo: Target output voltage

    Returns:
        a Tuple F = (F0, F1, F2)
            F0 = vS(2π)
            F1 = iC(2π) - i1(2π)
            F2 = Vo - VoTarget
    '''
    # Step 1: Get vS2π (Last one of the dataframe)
    f0 = r.vS.iloc[-1]

    # Step 2: Get dvS/dtiC
    f1 = r.iC.iloc[-1] - r.i1.iloc[-1]

    # Step 3： Get Vo(Average)
    f2 = r['vO'].mean() - Vo

    return f0, f1, f2

def Designer(C: Circuit, Vo: float) -> Circuit:
    '''
    This function performs the design method

    Args:
        R: Waveform
        Vo: Target output voltage

    Returns:
        C: Designed Circuit
    '''
    Iter = 0
    C.BodyDiode = False
    # Read in parameters to be designed
    λ = np.matrix([[C.A, C.B, C.Q]])

    # A very small delta
    Delta = 1e-6

    # Target tuple
    # When the F1-F3 is smaller than their target,
    # the designer will stop and output.
    target = (5e-3, 1e-2, 5e-3)

    # Time to start record and end
    # (θ_StartRecord, θ_End)
    simulator_intv = (200. * π, 202. * π)

    # Initial state (zero 8x1 matrix)
    initial_state = np.zeros(8)

    while True:
        print('=================================\nIteration:', Iter, '\n=================================\n')
        print('     A:', λ[0, 0], 'B:', λ[0, 1], 'Q:', λ[0, 2], '\n')
        print('     Calculating:F', '\n')

        Iter += 1

        C.A, C.B, C.Q = λ[0, 0], λ[0, 1], λ[0, 2]

        # Run simulator to get waveform
        result = C.run(simulator_intv, initial_state, 200, True, True)

        f1, f2, f3 = getF(result, Vo)
        F = np.mat([[f1, f2, f3]])
        print('     F:', F, '\n')

        # Convergence Detection
        if math.isnan(f1) or abs(f1) > 1e5:
            raise ConvergenceError(
                """
        Oops! Designer failed to convergence!😯
            Please check your initial circuit.
            This problem may caused by that the TargetVo is far from 
            the output voltage of the intial circuit.
            Consider adjust TargetVo a liitle bit once a time.
            e.g. 2.8→2.7→2.6→2.5 instead of 2.8→2.5
            """)
        if abs(f1) < target[0] and abs(f2) < target[1] and abs(f3) < target[2]:
            break
        dF = np.zeros((3, 3))
        print('     Calculating:dF')
        #Calculate jacobian matrix:
        for i in (0, 1, 2):
            λ[0, i] += Delta
            C.A, C.B, C.Q = λ[0, 0], λ[0, 1], λ[0, 2]
            # Run simulator to get waveform
            result = C.run(simulator_intv, initial_state, 200, True, True)
            d_f1, d_f2, d_f3 = getF(result, Vo)
            dF[i] = [(d_f1 - f1) / Delta, (d_f2 - f2) / Delta, (d_f3 - f3) / Delta]
            λ[0, i] -= Delta
        print('     dF:', dF, '\n')
        λ = λ - F * np.linalg.inv(dF)
    print('Design Successful!😁\n')
    print('A:', λ[0, 0], 'B:', λ[0, 1], 'Q:', λ[0, 2], '\n')
    C.BodyDiode = True
    return C
