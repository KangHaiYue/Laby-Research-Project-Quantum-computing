'''This file is created by Haiyue Kang'''
'''general multiplier that can multiply 2 numbers within 4 qubits, product within 1 qubyte'''
from ibm_quantum_widgets import CircuitComposer
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit.providers.aer import QasmSimulator
from math import pi

def input_translator_b(circ,x):
    #x is no bigger than 15 as there is only 4 qubits to store multiplier
    x_bin = bin(x)[2:]
    x_bin_lst = [int(i) for i in x_bin]
    x_bin_lst.reverse()
    for i in range(len(x_bin_lst)):
        if x_bin_lst[i] == 1:
            circ.x(3-i)

def input_translator_a(circ,x):
    #x is no bigger than 15 as there is only 4 qubits to store multiplier
    x_bin = bin(x)[2:]
    x_bin_lst = [int(i) for i in x_bin]
    x_bin_lst.reverse()
    for i in range(len(x_bin_lst)):
        if x_bin_lst[i] == 1:
            circ.x(7-i)
def output_translator(x):
    '''translate the counts from binary to decimal'''
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

def rotate1(circ,x7,x6,x5,x4,x3,x2,x1,x0,control):
    '''use to add 1 via rotation between QFT and IQFT, controlled by a qubit representing 001 digit of a'''
    circ.cp(2*pi/256,control,x7)
    circ.cp(2*pi/128,control,x6)
    circ.cp(2*pi/64,control,x5)
    circ.cp(2*pi/32,control,x4)
    circ.cp(2*pi/16,control,x3)
    circ.cp(2*pi/8,control, x2)
    circ.cp(2*pi/4,control, x1)
    circ.cp(2*pi/2,control, x0)

def rotate2(circ,x7,x6,x5,x4,x3,x2,x1,x0,control):
    '''use to add 2 via rotation between QFT and IQFT, controlled by a qubit representing 010 digit of a'''
    circ.cp(2*pi/128,control,x7)
    circ.cp(2*pi/64,control,x6)
    circ.cp(2*pi/32,control,x5)
    circ.cp(2*pi/16,control,x4)
    circ.cp(2*pi/8,control,x3)
    circ.cp(2*pi/4,control,x2)
    circ.cp(2*pi/2,control,x1)
    # note beacuse last rotation is 0 degree so no need to apply controlled phase anymore

def rotate4(circ,x7,x6,x5,x4,x3,x2,x1,x0,control):
    '''use to add 4 via rotation between QFT and IQFT, controlled by a qubit representing 100 digit of a'''
    circ.cp(2*pi/64,control,x7)
    circ.cp(2*pi/32,control,x6)
    circ.cp(2*pi/16,control,x5)
    circ.cp(2*pi/8,control,x4)
    circ.cp(2*pi/4,control,x3)
    circ.cp(2*pi/2,control,x2)
    # note beacuse last 2 rotations is 0 degree so no need to apply controlled phase anymore

def rotate8(circ,x7,x6,x5,x4,x3,x2,x1,x0,control):
    '''use to add 8 via rotation between QFT and IQFT'''
    circ.cp(2*pi/32,control,x7)
    circ.cp(2*pi/16,control,x6)
    circ.cp(2*pi/8,control,x5)
    circ.cp(2*pi/4,control,x4)
    circ.cp(2*pi/2,control,x3)
    # last 3 rotations are 0
def rotate16(circ,x7,x6,x5,x4,x3,x2,x1,x0,control):
    '''use to add 16 via rotation between QFT and IQFT'''
    circ.cp(2*pi/16,control,x7)
    circ.cp(2*pi/8,control,x6)
    circ.cp(2*pi/4,control,x5)
    circ.cp(2*pi/2,control,x4)
    # last 4 rotations are 0
def rotate32(circ,x7,x6,x5,x4,x3,x2,x1,x0,control):
    '''use to add 32 via rotation between QFT and IQFT'''
    circ.cp(2*pi/8,control,x7)
    circ.cp(2*pi/4,control,x6)
    circ.cp(2*pi/2,control,x5)
    # last 5 rotations are 0

def rotate64(circ,x7,x6,x5,x4,x3,x2,x1,x0,control):
    '''use to add 64 via rotation between QFT and IQFT'''
    circ.cp(2*pi/4,control,x7)
    circ.cp(2*pi/2,control,x6)
    # last 6 rotations are 0
def multiplier(a,b):
    '''multiply 2 numbers from 0-15(4bits), and answer should be from 0-255(8bits) purely quantum mechanically'''
    '''both inputs and outputs are just normal decimals, the function will translate them into
    and back from binary for you'''
    circuit = QuantumCircuit(20,8)#create 14 qubits, 0-3 for number a, 4-7 for number b,
    #8-11 create room for controlled operations, rest store the answer
    
    #set b
    input_translator_b(circuit,a)
    
    #set a
    input_translator_a(circuit,b)
    
    QFT(circuit,12,19)
    #multiply by repeated addition on 1st digit of b (quibit 3)
    for i in range(4):
        circuit.toffoli(3,7-i,11-i)
    rotate1(circuit,12,13,14,15,16,17,18,19, 11)
    rotate2(circuit,12,13,14,15,16,17,18,19, 10)
    rotate4(circuit,12,13,14,15,16,17,18,19, 9)
    rotate8(circuit,12,13,14,15,16,17,18,19, 8)
    for i in range(4):
        circuit.toffoli(3,7-i,11-i)

    #multiply by repeated addition on 2nd digit of b (quibit 2)
    for i in range(4):
        circuit.toffoli(2,7-i,11-i)
    rotate2(circuit,12,13,14,15,16,17,18,19, 11)
    rotate4(circuit,12,13,14,15,16,17,18,19, 10)
    rotate8(circuit,12,13,14,15,16,17,18,19, 9)
    rotate16(circuit,12,13,14,15,16,17,18,19, 8)
    for i in range(4):
        circuit.toffoli(2,7-i,11-i)
    
    #multiply by repeated addition on 3rd digit of b (quibit 1)
    for i in range(4):
        circuit.toffoli(1,7-i,11-i)
    rotate4(circuit,12,13,14,15,16,17,18,19, 11)
    rotate8(circuit,12,13,14,15,16,17,18,19, 10)
    rotate16(circuit,12,13,14,15,16,17,18,19, 9)
    rotate32(circuit,12,13,14,15,16,17,18,19, 8)
    for i in range(4):
        circuit.toffoli(1,7-i,11-i)
    
    #multiply by repeated addition on 4th digit of b (quibit 0)
    for i in range(4):
        circuit.toffoli(0,7-i,11-i)
    rotate8(circuit,12,13,14,15,16,17,18,19, 11)
    rotate16(circuit,12,13,14,15,16,17,18,19, 10)
    rotate32(circuit,12,13,14,15,16,17,18,19, 9)
    rotate64(circuit,12,13,14,15,16,17,18,19, 8)
    for i in range(4):
        circuit.toffoli(0,7-i,11-i)
    
    IQFT(circuit,12,19)
    
    #measure the final result
    circuit.measure(19,0)
    circuit.measure(18,1)
    circuit.measure(17,2)
    circuit.measure(16,3)
    circuit.measure(15,4)
    circuit.measure(14,5)
    circuit.measure(13,6)
    circuit.measure(12,7)
    #after set up the circuit, run it on simulator
    backend = QasmSimulator()
    qc_compiled = transpile(circuit, backend)
    job = backend.run(qc_compiled, shots = 1)
    result = job.result()
    counts = result.get_counts(qc_compiled)
    
    return output_translator(counts)