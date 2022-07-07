import random
N = 20

class InputGenerator:
    def __init__(self, input_file_path, number_of_inputs, number_of_test_cases = N):
        self.input_file_path = input_file_path
        self.number_of_inputs = number_of_inputs
        self.number_of_test_cases = number_of_test_cases
    
    def _generate_input_sequence(self):
        for _ in range(self.number_of_inputs):
            L = [ random.randint(0, 1) for i in range(self.number_of_test_cases)]
        test = " ".join(str(x) for x in L if x not in ['[', ']', ','])
        # print(test)
        return test
    
    def write_input(self):
        with open(self.input_file_path, 'w') as input_file:
            for _ in range(self.number_of_inputs):
                input_file.write(str(self._generate_input_sequence())+"\n")
    
