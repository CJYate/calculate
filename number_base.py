import re 


class BaseCalc(object):
    

    def __init__(self, string_input):
        self.string_input = string_input
        self._parse()
        
    def _parse(self):
        match = re.match('\[(.*)\]([0-9]+)', self.string_input)
        if not match:
            raise ValueError('Incorrect input %s' % self.string_input)
        
        self.input_value = match.groups()[0]
        self.base = int(match.groups()[1])
    
    def Solve(self):
        return "No solution"
    