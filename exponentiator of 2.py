'''This file is created by Haiyue Kang'''
'''The following codes builds a quantum exponentiator that calculates 2^x, where x is within 3 qubits'''
from ibm_quantum_widgets import CircuitComposer
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit.providers.aer import QasmSimulator
from math import pi


def input_translator(circ,x):
    #x is no bigger than 15 as there is only 4 qubits to store multiplier
    x_bin = bin(x)[2:]
    x_bin_lst = [int(i) for i in x_bin]
    x_bin_lst.reverse()
    for i in range(len(x_bin_lst)):
        if x_bin_lst[i] == 1:
            circ.x(2-i)
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

def rotate8b1(circ,x7,x6,x5,x4,x3,x2,x1,x0,control):
    '''use to add 1 via rotation between QFT and IQFT in 8 bits, 
    controlled by a qubit representing 001 digit of a'''
    circ.cp(2*pi/256,control,x7)
    circ.cp(2*pi/128,control,x6)
    circ.cp(2*pi/64,control,x5)
    circ.cp(2*pi/32,control,x4)
    circ.cp(2*pi/16,control,x3)
    circ.cp(2*pi/8,control, x2)
    circ.cp(2*pi/4,control, x1)
    circ.cp(2*pi/2,control, x0)

def rotate8b2(circ,x7,x6,x5,x4,x3,x2,x1,x0,control):
    '''use to add 2 via rotation between QFT and IQFT in 8 bits,
    controlled by a qubit representing 010 digit of a'''
    circ.cp(2*pi/128,control,x7)
    circ.cp(2*pi/64,control,x6)
    circ.cp(2*pi/32,control,x5)
    circ.cp(2*pi/16,control,x4)
    circ.cp(2*pi/8,control,x3)
    circ.cp(2*pi/4,control,x2)
    circ.cp(2*pi/2,control,x1)
    # note beacuse last rotation is 0 degree so no need to apply controlled phase anymore

def rotate8b4(circ,x7,x6,x5,x4,x3,x2,x1,x0,control):
    '''use to add 4 via rotation between QFT and IQFT in 8 bits,
    controlled by a qubit representing 100 digit of a'''
    circ.cp(2*pi/64,control,x7)
    circ.cp(2*pi/32,control,x6)
    circ.cp(2*pi/16,control,x5)
    circ.cp(2*pi/8,control,x4)
    circ.cp(2*pi/4,control,x3)
    circ.cp(2*pi/2,control,x2)
    # note beacuse last 2 rotations is 0 degree so no need to apply controlled phase anymore

def rotate8b8(circ,x7,x6,x5,x4,x3,x2,x1,x0,control):
    '''use to add 8 via rotation between QFT and IQFT in 8 bits'''
    circ.cp(2*pi/32,control,x7)
    circ.cp(2*pi/16,control,x6)
    circ.cp(2*pi/8,control,x5)
    circ.cp(2*pi/4,control,x4)
    circ.cp(2*pi/2,control,x3)
    # last 3 rotations are 0
def rotate8b16(circ,x7,x6,x5,x4,x3,x2,x1,x0,control):
    '''use to add 16 via rotation between QFT and IQFT in 8 bits'''
    circ.cp(2*pi/16,control,x7)
    circ.cp(2*pi/8,control,x6)
    circ.cp(2*pi/4,control,x5)
    circ.cp(2*pi/2,control,x4)
    # last 4 rotations are 0
    
def rotate8b32(circ,x7,x6,x5,x4,x3,x2,x1,x0,control):
    '''use to add 32 via rotation between QFT and IQFT in 8 bits'''
    circ.cp(2*pi/8,control,x7)
    circ.cp(2*pi/4,control,x6)
    circ.cp(2*pi/2,control,x5)
    # last 5 rotations are 0

def rotate8b64(circ,x7,x6,x5,x4,x3,x2,x1,x0,control):
    '''use to add 64 via rotation between QFT and IQFT in 8 bits'''
    circ.cp(2*pi/4,control,x7)
    circ.cp(2*pi/2,control,x6)
    # last 6 rotations are 0
def rotate8b128(circ,x7,x6,x5,x4,x3,x2,x1,x0,control):
    '''use to add 64 via rotation between QFT and IQFT in 8 bits'''
    circ.cp(2*pi/2,control,x7)
    # last 7 rotations are 0

def rotate4b1(circ,x3,x2,x1,x0,control):
    '''use to add 1 via rotation between QFT and IQFT in 4 bits,
    controlled by a qubit representing 001 digit of a'''
    circ.cp(2*pi/16,control,x3)
    circ.cp(2*pi/8,control, x2)
    circ.cp(2*pi/4,control, x1)
    circ.cp(2*pi/2,control, x0)

def rotate4b2(circ,x3,x2,x1,x0,control):
    '''use to add 2 via rotation between QFT and IQFT in 4 bits,
    controlled by a qubit representing 010 digit of a'''

    circ.cp(2*pi/8,control,x3)
    circ.cp(2*pi/4,control,x2)
    circ.cp(2*pi/2,control,x1)
    # note beacuse last rotation is 0 degree so no need to apply controlled phase anymore

def rotate4b4(circ,x3,x2,x1,x0,control):
    '''use to add 4 via rotation between QFT and IQFT in 4 bits,
    controlled by a qubit representing 100 digit of a'''

    circ.cp(2*pi/4,control,x3)
    circ.cp(2*pi/2,control,x2)
    # note beacuse last 2 rotations is 0 degree so no need to apply controlled phase anymore

def rotate4b8(circ,x3,x2,x1,x0,control):
    '''use to add 8 via rotation between QFT and IQFT in 4 bits'''
    circ.cp(2*pi/2,control,x3)
    # last 3 rotations are 0
def exponentiator_2(x):
    '''exponentiate 2 by x where x is within 3 bits, so 2^x is within a byte'''
    '''both inputs and outputs are just normal decimals, the function will translate them into
    and back from binary for you'''
    #create 24 qubits, 0-2 store x, 3-7 store 2^(2^2*x2),
    #8-10 store 2^(2^1*x1), 11-12 store 2^(2^0*x0), 16-19 create room for controlled operations, 
    # rest are used for QFT addition/multiplication, some qubits will be reused for other purposes
    # in the circuit to save number of qubits required
    circuit = QuantumCircuit(24,8)
    
    #initialize the number to be exponent
    input_translator(circuit,x)
    
    #store 2^(2^2*x2) 
    circuit.cx(0,3)
    circuit.x(0)
    circuit.cx(0,7)
    
    #store 2^(2^1*x1)
    circuit.cx(1,8)
    circuit.x(1)
    circuit.cx(1,10)
    
    #store 2^(2^0*x0)
    circuit.cx(2,11)
    circuit.x(2)
    circuit.cx(2,12)
    
    QFT(circuit,20,23)
    #multiply 2^(2^1*x1) and 2^(2^0*x0)
    #add 2^(2^0*x0)*1st digit of 2^(2^1*x1)
    for i in range(2):
        circuit.toffoli(10,12-i,19-i)
    rotate4b1(circuit,20,21,22,23, 19)
    rotate4b2(circuit,20,21,22,23, 18)
    for i in range(2):
        circuit.toffoli(10,12-i,19-i)

    #add 2^(2^0*x0)*3rd digit of 2^(2^1*x1) (no need care 2nd digit because always 0)
    for i in range(2):
        circuit.toffoli(8,12-i,19-i)
    rotate4b4(circuit,20,21,22,23, 19)
    rotate4b8(circuit,20,21,22,23,18)
    for i in range(2):
        circuit.toffoli(8,12-i,19-i)
    
    IQFT(circuit,20,23)
    #undo store 2^(2^0*x0), prepare room for next multiplication 
    circuit.cx(2,12)
    circuit.x(2)
    circuit.cx(2,11)
    
    #undo store 2^(2^1*x1), prepare room for next multiplication 
    circuit.cx(1,10)
    circuit.x(1)
    circuit.cx(1,8)
    
    QFT(circuit,8,15)
    #multiply 2^(2^2*x2) and product just calculated
    #add previous product*1st digit of 2^(2^2*x2)
    for i in range(4):
        circuit.toffoli(7,23-i,19-i)
    rotate8b1(circuit,8,9,10,11,12,13,14,15, 19)
    rotate8b2(circuit,8,9,10,11,12,13,14,15, 18)
    rotate8b4(circuit,8,9,10,11,12,13,14,15, 17)
    rotate8b8(circuit,8,9,10,11,12,13,14,15, 16)
    for i in range(4):
        circuit.toffoli(7,23-i,19-i)
    
    #add previous product*5th digit of 2^(2^2*x2)
    for i in range(4):
        circuit.toffoli(3,23-i,19-i)
    rotate8b16(circuit,8,9,10,11,12,13,14,15, 19)
    rotate8b32(circuit,8,9,10,11,12,13,14,15, 18)
    rotate8b64(circuit,8,9,10,11,12,13,14,15, 17)
    rotate8b128(circuit,8,9,10,11,12,13,14,15,16)
    for i in range(4):
        circuit.toffoli(3,23-i,19-i)
    IQFT(circuit,8,15)
    #undo store 2^(2^2*x2), prepare room for next multiplication 
    circuit.cx(0,7)
    circuit.x(0)
    circuit.cx(0,3)
    #measure the final result
    circuit.measure(15,0)
    circuit.measure(14,1)
    circuit.measure(13,2)
    circuit.measure(12,3)
    circuit.measure(11,4)
    circuit.measure(10,5)
    circuit.measure(9,6)
    circuit.measure(8,7)
    #after set up the circuit, run it on simulator
    backend = QasmSimulator()
    qc_compiled = transpile(circuit, backend)
    job = backend.run(qc_compiled, shots = 1)
    result = job.result()
    counts = result.get_counts(qc_compiled)
    return output_translator(counts)