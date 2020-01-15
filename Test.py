
import numpy as np
from math import pi as π
from CircuitLibrary.ClassEDWPT import ClassEDWPT
from Oscilloscope import Oscilloscope
from Designer import Designer
#Create a new Class-E2 DC DC Converter
#and name it "My_Circuit"
My_Circuit = ClassEDWPT(
                        #Parameters:
                        A=1.005,   B=0.5415,  Q=0.5,    H=20.0,     
                        N=1.0,     k=0.20,    S=0.02,   J=0.7743,
                        Ds=0.5,    U=1.0,
                        #Parasitic resistances：     
                        rL1=0.002,  rL2=0.002,   rS=0.002, rD=0.002  
                        )

#Initial state (zero 8x1 matrix)
Initial_State=np.zeros(8)

#Time to start record and end
#(θ_StartRecord, θ_End)
θInterval=(200.*π,204.*π) 

TargetVo=2.75

My_Circuit2 = Designer(My_Circuit,TargetVo)

#Run simulation, let's rock!
#The waveform will be saved in dataframe "Record"
Record=My_Circuit2.Run(θInterval,Initial_State)

#Now, see the waveform by the method "Oscilloscope"
Graph=Oscilloscope(Record,['iC','vS','i1','i2','vD1','vO'])

#You can also output "Record" to csv file
#Record.to_csv('Data//Record.csv',encoding='utf_8_sig')

