import numpy as np
from math import pi as π
from CircuitLibrary.ClassE2DCDCISO import ClassE2DCDCISO
from Oscilloscope import Oscilloscope


# Create a new Class-E2 DC DC Converter
# and name it "My_Circuit"
My_Circuit = ClassE2DCDCISO(
    # Basic Quantities:
    Vi=5.0, RL=5.0, fs=1e6,
    # Parameters:
    A=0.9258, B=0.6461, Q1=0.4, H=0.02,
    NTX=1.0, kTX=0.90, J=9.5214, Ds=0.5,
    K=0.02,
    # Parasitic resistances：
    r1=0.01, r2=0.01, rS=0.001, rD=0.001,
    rC=0.001
)

# Initial state (zero 7x1 matrix)
initial_state = np.zeros(7)

# Time to start record and end
# (θ_StartRecord, θ_End)
θInterval = (100. * π, 104. * π)

# Run simulation, let's rock!
# The waveform will be saved in data frame "Record"
Record = My_Circuit.run(θInterval, initial_state)

# Now, see the waveform by the method "Oscilloscope"
Graph = Oscilloscope(Record, ['iC', 'vS', 'i1', 'i2', 'vD', 'vO'])

# You can also output "Record" to csv file
Record.to_csv('Record.csv', encoding='utf_8_sig')
