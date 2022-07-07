from simulator import Simulator

# class to find required values for unknown points in circuit


class FindPoints:
    def __init__(self, F_circuit, G_circuit, input_file, output_file, debug_file, unknown_file):
        self.F_circuit = F_circuit
        self.G_circuit = G_circuit
        self.input_file = input_file
        self.output_file = output_file
        self.debug_file = debug_file
        self.unknown_file = unknown_file
        self.final_output = None
        self.zero_output = None
        self.one_output = None
        self.unknowns = []

    def run(self):

        simulator = Simulator(self.F_circuit, self.input_file, self.output_file,
                              self.debug_file, unknown=0, debug_mode=True, random_input=False)
        _, self.zero_output, _, unknown_points, _ = simulator.run_simulation()

        simulator = Simulator(self.F_circuit, self.input_file, self.output_file,
                              self.debug_file, unknown=1, debug_mode=True, random_input=False)
        _, self.one_output, _, unknown_points, _ = simulator.run_simulation()
        
        simulator = Simulator(self.G_circuit, self.input_file, self.output_file,
                              self.debug_file, unknown=0, debug_mode=True, random_input=False)
        _, self.final_output, _, unknown_points, _ = simulator.run_simulation()

    def find(self):
        self.run()

        for id, key in enumerate(self.final_output.keys()):
            if ((self.final_output[key] == self.zero_output[key]) and (self.final_output[key] == self.one_output[key])):
                if(len(self.unknowns) == 0 and id == len(self.final_output.keys())-1):
                    unknown = []
                    for idx, item in enumerate(self.final_output[key]):
                        unknown.append(2)
                    self.unknowns.append(unknown)
            else:
                unknown = []
                for idx, item in enumerate(self.final_output[key]):
                    if (self.zero_output[key][idx] == self.one_output[key][idx]):
                        unknown.append(2)
                    elif (item == self.zero_output[key][idx]):
                        unknown.append(0)
                    elif (item == self.one_output[key][idx]):
                        unknown.append(1)
                if ((unknown not in self.unknowns) and (sum(unknown) != 2*len(unknown))):
                    self.unknowns.append(unknown)

    def write(self):
        self.find()
        for unknown in self.unknowns:
            with open(self.unknown_file, 'w') as unknown_file:
                unknown_file.write(str(unknown)+"\n")


if __name__ == "__main__":
    find = FindPoints("test-cases/unit15/F.v", "test-cases/unit15/G.v", "solution/text_files/input.txt",
                      "solution/text_files/output.txt", "solution/text_files/debug.txt", "solution/text_files/unknown.txt")

    find.write()
