'''This file is created by Haiyue Kang'''
'''multiplier of 3 (3*n), where n is within 4 qubits'''
from ibm_quantum_widgets import CircuitComposer
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit.providers.aer import QasmSimulator
#from qiskit.circuit.library.standard_gates import ZGate
from math import pi

def input_translator(circ,x):
    #x is no bigger than 7 as there is only 3 qubits to store multiplier
    x_bin = bin(x)[2:]
    x_bin_lst = [int(i) for i in x_bin]
    x_bin_lst.reverse()
    for i in range(len(x_bin_lst)):
        if x_bin_lst[i] == 1:
            circ.x(9-i)

def output_translator(x):
    sum_ = list(x.keys())[0]
    sum_ = int(sum_,2)
    return sum_

def QFT(circ,start, end):
    '''quantum fourier transform specifying the index of starting and ending qubits'''
    for i in range(start,end+1):
        circ.h(i)
        for j in range(i, end+1):
            if i!=j:
                circ.cp(pi/(2**(j-i)), j, i)

def IQFT(circ,start, end):
    '''inverse quantum fourier transform specifying the index  of starting and ending qubits'''
    for i in reversed(range(start,end+1)):
        for j in reversed(range(i, end+1)):
            if i!=j:
                circ.cp(-pi/(2**(j-i)), j, i)
        circ.h(i)
        
def multiplier_3(n):
    '''multiply 3*n, where n is within 4 qubits'''
    '''both inputs and outputs are just normal decimals, the function will translate them into
    and back from binary for you'''    
    ### the following is multipiler of 3###
    circuit = QuantumCircuit(10,6)#create 8 qubits, first 5 to store final answer,last 3 store
    #number of times being multiplied
    input_translator(circuit,n)#initialize the last 3 qubits to store n
    
    QFT(circuit,0,5)
    
    #controlled rotation of digit 1000 thus +8a, here use a=3
    circuit.cp(2*pi*(1/4+1/8),6,0)
    circuit.cp(2*pi*(1/2+1/4),6,1)
    circuit.cp(2*pi*(1/2),6,2)

    
    #controlled rotation of digit 0100 thus +4a, here use a=3
    circuit.cp(2*pi*(1/8+1/16),7,0)
    circuit.cp(2*pi*(1/4+1/8),7,1)
    circuit.cp(2*pi*(1/2+1/4),7,2)
    circuit.cp(2*pi*(1/2),7,3)

    
    #controlled rotation of digit 0010 thus +2a, here use a=3
    circuit.cp(2*pi*(1/16+1/32),8,0)
    circuit.cp(2*pi*(1/8+1/16),8,1)
    circuit.cp(2*pi*(1/4+1/8),8,2)
    circuit.cp(2*pi*(1/2+1/4),8,3)
    circuit.cp(2*pi*(1/2),8,4)
    
    #controlled rotation of digit 0001 thus +a, here use a=3
    circuit.cp(2*pi*(1/32+1/64),9,0)
    circuit.cp(2*pi*(1/16+1/32),9,1)
    circuit.cp(2*pi*(1/8+1/16),9,2)
    circuit.cp(2*pi*(1/4+1/8),9,3)
    circuit.cp(2*pi*(1/2+1/4),9,4)
    circuit.cp(2*pi*(1/2),9,5)
    
    IQFT(circuit,0,5)
    #meausre the final result
    circuit.measure(0,5)
    circuit.measure(1,4)
    circuit.measure(2,3)
    circuit.measure(3,2)
    circuit.measure(4,1)
    circuit.measure(5,0)

    #compile the circuit and run it on simulator
    backend = QasmSimulator()
    qc_compiled = transpile(circuit, backend)
    job = backend.run(qc_compiled, shots = 1)
    result = job.result()
    counts = result.get_counts(qc_compiled)
    
    return output_translator(counts)