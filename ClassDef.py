from ErrorDefine import *
from Solver import *
from math import pi
import numpy as np
import pandas as pd
from tqdm import tqdm


class Circuit(object):
    Vi = 1.0,
    RL = 1.0,
    fs = 1e6,

    def Para_Check(self, Para_Dict):
        '''
        Check if parameters are enough to create a circuit.
        '''
        for Para in self.Para_List:
            if Para not in Para_Dict:
                raise CircuitParameterError("Parameters are not enough. Check your input.")

    def run(
            self,
            θ_interval: tuple,
            initial_state: np.matrix,
            step=200,
            output_record=True,
            silent=False):
        '''
        Run simulation for this circuit.
        '''
        record = pd.DataFrame()
        start_θ, record_θ, end_θ = 0.0, θ_interval[0], θ_interval[1]
        if record_θ > end_θ:
            raise CircuitParameterError("Record_θ cannot be larger than End_θ!😯")
        period = end_θ / (2.0 * pi)
        total_step = int(period * step)
        θ_space, step_size = np.linspace(start_θ, end_θ, num=total_step, retstep=True)
        if not silent:
            θ_space = tqdm(θ_space)
        states = [initial_state] * 4

        for θ in θ_space:
            Mat_A = self.MatA(θ)
            Mat_B = self.MatB(θ, states[0])
            states = [BDF_4(self.order,states, Mat_A, Mat_B, step_size)] + states
            if output_record and θ > record_θ:
                record = self.CreateDataFrame(θ, states[0], record)
            states.pop()

        if not output_record:
            record = self.CreateDataFrame(θ, states[0], record)
        # Adjust the order of output record
        record = record[self.Output_List]
        return record


class _State(list):
    pass
