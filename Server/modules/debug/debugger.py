class ErrorHandling:
    def __init__(self):
        pass

    def dump_vars(self, var_dict):
        # Take all variables in dict() form and parse the dict and print the variables
        # at the time of the crash from the dying process. This will aid in finding the
        # erroneous data set while developing the application and its interfaces.
        # This can also be enabled based on the inclusion of debugging in the code.
        print("\n\tVarName : ValueStored")
        for key, value in var_dict.items():
            print(f"\t{key} : {value}")
        print("")

# Test Case for the class().function()
a = {'test': 1, 'test': 2, 'testl': [1, 2, 3, 4, 5]}
ErrorHandling().dump_vars(a)
