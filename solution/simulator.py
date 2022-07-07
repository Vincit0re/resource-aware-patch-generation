# A simulator that simulate digital logic circuit

# import the necessary modules
import time
import re
from gates import *
from input_generator import InputGenerator

# define the class for the simulator


class Simulator:
    # use the constructor to initialize the simulator
    def __init__(self, circuit_file_path, input_file_path, output_file_path, debug_file_path, unknown=0, debug_mode=False, random_input=True):
        self.circuit_file_path = circuit_file_path
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.debug_file_path = debug_file_path
        self.debug_mode = debug_mode
        self.unknown = unknown
        self.random_input = random_input
        self.number_of_inputs = None
        self.number_of_unknown_points = None
        self.levels = None
        self.unknown_points = None
        self.founded = None
        self.output = None

    # function to read circuit file
    def _read_circuit(self):
        lines = []
        with open(self.circuit_file_path, 'r') as circuit_file:
            text = circuit_file.read()
            text = text.split(';')
            for _, line in enumerate(text):
                l = line.replace("\n", "")
                l = re.sub("\s\s+", " ", l)
                lines.append(l+";")

        return lines

    # function to read input file
    def _read_input(self):
        with open(self.input_file_path, 'r') as input_file:
            lines = input_file.readlines()

        tests = []
        for line in lines:
            if ('\n' in line):
                idx = line.index('\n')
                tests.append(line[:idx])
            else:
                tests.append(line)

        results = []
        for test in tests:
            test = test.split(' ')
            results.append(test)
        return results

    def _simulate(self, debug):
        # reading the user info
        lines = self._read_circuit()

        Input = {}  # storing the inputs given in the input file
        Output = {}  # will store the output of the circuit
        input_points = []  # input points given in circuit file
        output_points = []  # output points given in circuit file
        wires_points = []  # wires points given in circuit file
        unknown_points = []  # unknown points given in circuit file

        # storing the provided information in the dictionaries
        for line in lines:
            # for unknown points
            if ('t_0' in line and 'wire' in line):
                idx_start = line.index("wire") + 5
                idx_end = line.index(" ;")
                unknowns = line[idx_start:idx_end].split(" , ")
                for unknown in unknowns:
                    unknown_points.append(unknown)
            # for inputs
            if ("input" in line):
                idx_start = line.index("input") + 6
                idx_end = line.index(" ;")
                inputs = line[idx_start:idx_end].split(" , ")
                for input in inputs:
                    input_points.append(input)
            # for outputs
            elif ("output" in line):
                idx_start = line.index("output") + 7
                idx_end = line.index(" ;")
                outputs = line[idx_start:idx_end].split(" , ")
                for output in outputs:
                    output_points.append(output)
            # for wires (intermediate points))
            elif ("wire" in line):
                idx_start = line.index("wire") + 5
                idx_end = line.index(" ;")
                wires = line[idx_start:idx_end].split(" , ")
                for wire in wires:
                    wires_points.append(wire)

        if (self.random_input):
            # randomly generating the input test cases (100 tests)
            self.number_of_inputs = len(input_points)
            inputs = InputGenerator(
                self.input_file_path, number_of_inputs=self.number_of_inputs)
            inputs.write_input()

        # total points given in module
        total_points = input_points + output_points + wires_points
        total_points.append("1'b0")
        total_points.append("1'b1")
        # all the points used in the circuit
        all_used_points = []
        if (self.debug_mode):
            debug.write(f"input_points: {input_points}\n")
            debug.write(f"output_points: {output_points}\n")
            debug.write(f"wires_points: {wires_points}\n")
            debug.write(
                f"total_points: {len(total_points)} | {total_points}\n")

        # reading the input
        tests = self._read_input()
        # initializing the input dictionary
        for i, input in enumerate(input_points):
            Input[input] = [int(item) for item in tests[i]]
        Input["1'b0"] = [0 for _ in tests[0]]
        Input["1'b1"] = [1 for _ in tests[0]]
        # initializing the output dictionary
        for _, output in enumerate(output_points):
            Output[output] = [0 for _ in range(len(tests[0]))]

        # initializing the founded dictionary to keep track of the circuit points that are already founded
        founded = {}
        for point in input_points:
            founded[point] = 1
        for point in wires_points + output_points:
            founded[point] = 0

        # initializing the intermediate_outputs dictionary
        intermediate_outputs = {}
        for input in input_points:
            intermediate_outputs[input] = Input[input]
        for wire in wires_points:
            intermediate_outputs[wire] = 0

        for unknown in unknown_points:
            intermediate_outputs[unknown] = [self.unknown for _ in tests[0]]
            founded[unknown] = 1
            
        self.unknown_points = unknown_points
        self.number_of_unknown_points = len(unknown_points)
        
        gates = []
        # initializing the levels list
        levels = []
        initial_level = {}
        for input in input_points:
            initial_level[input] = Input[input]
        levels.append(initial_level)
        l = 0

        # main algorithm for getting all output and intermediate outputs of files...
        while(1):
            if (self.debug_mode):
                debug.write(f"gates: {gates}\n")
                debug.write(f"Level: {l} | {levels}\n")
                debug.write(f"founded: {sum(founded.values())} | {founded}\n")
                debug.write(
                    f"all_used_points: {len(all_used_points)} | {all_used_points}\n")

            level = {}
            # break when all outputs are found...
            if((sum(founded.values()) == len(all_used_points)) and (l > 0)):
                break

            else:
                for i in range(len(lines)):
                    # stores all lists used in a gate operation.
                    operationlist = []
                    s = lines[i]
                    if ("endmodule" in s):  # if endmodule is found, break the loop
                        break
                    # while reading gates ignore these lines
                    if (("top" in s) or ("input" in s) or ("output" in s) or ("wire" in s)):
                        continue
                    # getting gate and output point
                    idx = s.index(" ( ")
                    idx_s = s.index(" ( ") + 3
                    idx_e = s.index(" , ")
                    gate = s[:idx]
                    appendindex = s[idx_s:idx_e]

                    if (appendindex not in total_points):
                        raise Exception(f"{appendindex} is not a valid point")

                    if ((appendindex in total_points) and (appendindex not in all_used_points)):
                        all_used_points.append(appendindex)
                    if (self.debug_mode):
                        debug.write(f"{gate} | {appendindex}\n")
                    if(gate not in gates):
                        gates.append(gate)

                    # if output is already found then skip the gate
                    if (founded[appendindex] == 1):
                        continue

                    # if output is intermediate type
                    elif(appendindex in wires_points):
                        # algo for iterating operative string.
                        count = 0
                        d = len(s)
                        pr = idx_e
                        while(pr < d):
                            if(s[pr] == ";"):
                                break

                            elif(s[pr] == " " or s[pr] == "," or s[pr] == ")"):
                                pr += 1
                                pass

                            else:
                                index = ""
                                while(s[pr] != "," and s[pr] != ")" and s[pr] != " " and s[pr] != ";"):
                                    index += s[pr]
                                    pr += 1

                                if (index not in total_points):
                                    raise Exception(
                                        f"{index} is not a valid point")
                                if index in ["1'b0", "1'b1"]:
                                    founded[index] = 1
                                if (self.debug_mode):
                                    debug.write(f"{index}\n")

                                if ((index in total_points) and (index not in all_used_points)):
                                    all_used_points.append(index)

                                if(index in input_points + ["1'b0", "1'b1"]):
                                    operationlist.append(Input[index])

                                elif(index in wires_points):
                                    if(intermediate_outputs[index] == 0):
                                        count += 1

                                    else:
                                        operationlist.append(
                                            intermediate_outputs[index])

                        if(count == 0 and len(operationlist) != 0):
                            if (self.debug_mode):
                                debug.write("intermediate_type\n")
                                debug.write(f"{operationlist}\n")

                            if(gate == "and"):
                                Li = AND(operationlist)
                                intermediate_outputs[appendindex] = Li

                            elif(gate == "or"):
                                Li = OR(operationlist)
                                intermediate_outputs[appendindex] = Li

                            elif(gate == "nor"):
                                Li = NOR(operationlist)
                                intermediate_outputs[appendindex] = Li

                            elif(gate == "not"):
                                Li = NOT(operationlist)
                                intermediate_outputs[appendindex] = Li

                            elif(gate == "nand"):
                                Li = NAND(operationlist)
                                intermediate_outputs[appendindex] = Li

                            elif(gate == "xor"):
                                Li = NAND(operationlist)
                                intermediate_outputs[appendindex] = Li

                            elif(gate == "xnor"):
                                Li = XNOR(operationlist)
                                intermediate_outputs[appendindex] = Li

                            elif(gate == "buf"):
                                Li = BUFF(operationlist)
                                intermediate_outputs[appendindex] = Li

                            else:
                                raise Exception(f"Unknown gate: {gate}")
                        else:
                            pass

                        if ((intermediate_outputs[appendindex] != 0) and (count == 0) and len(operationlist) != 0):
                            founded[appendindex] = 1
                            level[appendindex] = intermediate_outputs[appendindex]

                    # if output is of final output type...
                    elif(appendindex in output_points):
                        # iterating string..
                        count = 0
                        d = len(s)
                        pr = idx_e
                        while(pr < d):
                            if(s[pr] == ";"):
                                break

                            elif(s[pr] == " " or s[pr] == "," or s[pr] == ")"):
                                pr += 1
                                pass

                            else:
                                index = ""
                                while(s[pr] != "," and s[pr] != ")" and s[pr] != " " and s[pr] != ";"):
                                    index += s[pr]
                                    pr += 1

                                if (index not in total_points):
                                    raise Exception(
                                        f"{index} is not a valid point")
                                if index in ["1'b0", "1'b1"]:
                                    founded[index] = 1
                                if (self.debug_mode):
                                    debug.write(f"{index}\n")

                                if ((index in total_points) and (index not in all_used_points)):
                                    all_used_points.append(index)

                                if(index in input_points + ["1'b0", "1'b1"]):
                                    operationlist.append(Input[index])

                                elif(index in wires_points):
                                    if(intermediate_outputs[index] == 0):
                                        count += 1

                                    else:
                                        operationlist.append(
                                            intermediate_outputs[index])

                        if(count == 0 and len(operationlist) != 0):
                            if (self.debug_mode):
                                debug.write("final_type\n")
                                debug.write(f"{operationlist}\n")

                            if(gate == "and"):
                                Li = AND(operationlist)
                                Output[appendindex] = Li

                            elif(gate == "or"):
                                Li = OR(operationlist)
                                Output[appendindex] = Li

                            elif(gate == "nor"):
                                Li = NOR(operationlist)
                                Output[appendindex] = Li

                            elif(gate == "not"):
                                Li = NOT(operationlist)
                                Output[appendindex] = Li

                            elif(gate == "nand"):
                                Li = NAND(operationlist)
                                Output[appendindex] = Li

                            elif(gate == "xor"):
                                Li = NAND(operationlist)
                                Output[appendindex] = Li

                            elif(gate == "xnor"):
                                Li = XNOR(operationlist)
                                Output[appendindex] = Li

                            elif(gate == "buf"):
                                Li = BUFF(operationlist)
                                Output[appendindex] = Li

                            else:
                                raise Exception(f"Unknown gate: {gate}")

                        else:
                            pass

                        if (count == 0 and len(operationlist) != 0):
                            founded[appendindex] = 1
                            level[appendindex] = Output[appendindex]

                    else:
                        pass
            # level increased by 1
            l += 1
            levels.append(level)
        if (self.debug_mode):
            debug.write(f"{Output}\n")
        self.founded = founded
        self.levels = levels
        self.output = Output
        return self.output, self.levels, self.unknown_points, self.founded

    def _write_output(self):
        with open(self.debug_file_path, "w") as debug:
            Output = self._simulate(debug)[0]
            with open(self.output_file_path, "w") as output_file:
                for _, output in enumerate(Output.keys()):
                    out = ""
                    for item in Output[output]:
                        if (item != '[' or item != ']'):
                            out += str(item) + " "
                    output_file.write(str(out)+'\n')
                    
        return self.output, self.levels, self.unknown_points, self.founded

    def run_simulation(self):
        start = time.time()
        self._write_output()
        end = time.time()
        total_time = end - start
        return total_time, self.output, self.levels, self.unknown_points, self.founded

