import copy

#gates used in file..

# Buffer gate
def BUFF(l1):
    l2 = copy.deepcopy(l1)
    return l2[0]

# AND gate
def AND(l1):
    l2 = copy.deepcopy(l1)
    if (len(l2) < 2):
        raise Exception(f"Invalid number of inputs: {len(l2)}")
    for k in range(len(l2)-1):
        for i in range(len(l2[k])):
            l2[k+1][i]=(l2[k][i] and l2[k+1][i])
    l3 = copy.deepcopy(l2[-1])
    return l3

# OR gate
def OR(l1):
    l2 = copy.deepcopy(l1)
    if (len(l2) < 2):
        raise Exception(f"Invalid number of inputs: {len(l2)}")
    for k in range(len(l2)-1):
        for i in range(len(l2[k])):
            l2[k+1][i]=(l2[k][i] or l2[k+1][i])
    l3 = copy.deepcopy(l2[-1])
    return l3

# NOR gate
def NOR(l1):
    l2 = copy.deepcopy(l1)
    if (len(l2) < 2):
        raise Exception(f"Invalid number of inputs: {len(l2)}")
    l3 = copy.deepcopy([OR(l2)])
    l4 = copy.deepcopy([NOT(l3)])
    return l4[0]

# NOT gate
def NOT(l1):
    l2 = copy.deepcopy(l1)
    if (len(l2) != 1):
        raise Exception(f"Invalid number of inputs: {len(l2)}")
    l3 = []
    for k in l2[0]:
        if(k==0):
            l3.append(1)
        else:
            l3.append(0)
    return l3

# NAND gate
def NAND(l1):
    l2 = copy.deepcopy(l1)
    if (len(l2) < 2):
        raise Exception(f"Invalid number of inputs: {len(l2)}")
    l3 = copy.deepcopy([AND(l2)])
    l4 = copy.deepcopy([NOT(l3)])
    return l4[0]

#XOR gate
def XOR(l1):
    l2 = copy.deepcopy(l1)
    if (len(l2) != 2):
        raise Exception(f"Invalid number of inputs: {len(l2)}")
    l3 = []
    for k in range(len(l2[0])):
        if(l2[0][k]== l2[1][k]):
            l3.append(0)
        else:
            l3.append(1)
    return l3

#XNOR gate
def XNOR(l1):
    l2 = copy.deepcopy(l1)
    if (len(l2) != 2):
        raise Exception(f"Invalid number of inputs: {len(l2)}")
    l3 = copy.deepcopy([XOR(l2)])
    l4 = copy.deepcopy([NOT(l3)])
    return l4[0]