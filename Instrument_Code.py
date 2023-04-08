import sys


def instrument_code(code_file_path, output_file):

    # Read in the .py file as a string
    with open(code_file_path, 'r') as f:
        code = f.read()

    # Dictionary to store execution metrics for the code
    code_metrics = {}

    # Function to track how often a piece of code gets executed
    def track_code(frame, event, arg):
        if event == 'line':
            # Get the source file and line number for the current statement
            file_name = frame.f_code.co_filename
            line_number = frame.f_lineno

            # Get the source code for the current line
            with open(file_name, 'r') as f:
                source_lines = f.readlines()
                source_code = source_lines[line_number - 1]

            # Increment the count for the current line
            code_metrics[(file_name, line_number, source_code)] = code_metrics.get((file_name, line_number, source_code), 0) + 1

        # Return the tracking information
        return track_code

    # Compile the code into a code object
    code_obj = compile(code, code_file_path, 'exec')

    # Set the track_code function and execute the code
    sys.settrace(track_code)
    exec(code_obj)
    sys.settrace(None)  # Clea track_code after code is finished executing

    # Save the metrics to a file
    with open(output_file, 'w+') as w:
        for (filename, lineno, source), count in sorted(code_metrics.items()):
            w.write(f"{filename}:{lineno}:{source} = {count}\n")
        w.close()


# Sample 2 - A very simple CLI based calculator
# The GUI of sample 1 is conflicting with the code
# Therefore, I am just using the CLI solution for this question
instrument_code("Simple-Calculator-2/calculator.py", "Metrics_Output-2.txt")
