import numpy as np


def BDF_4(
        order: float,
        States: np.array,
        matA: np.matrix,
        matB: np.matrix,
        h: float
) -> np.matrix:
    '''
        4-order Backward Differential Formula:

        Args:
            1.order
            2.State (List of last 4 states)
            3.MatA (Power source matrix A of the circuit)
            4.MatB (CircuitMatB_Inv matrix B)
            5.h (Step size per one step)

        Returns:
            result: The state of the next data point
    '''
    # Order = np.size(MatA,0)
    matB = matB * h - 25.0 / 12.0 * np.identity(order)
    matA = -h * matA - States[0] * 4.0 + States[1] * 3.0 - States[2] * (4.0 / 3.0) + States[3] * 0.25
    MatB_Inv = np.linalg.inv(matB)
    result = np.dot(MatB_Inv, matA)
    return result
