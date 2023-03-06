'''Importing all the necessary libraries.'''
import os
import sys
from pylint import lint

'''Setting minimum threshold value for every python script.'''
THRESHOLD = 8.5

'''Scanning all the .py files in all the directories in the root directory.'''
for root, dirs, files in os.walk("./"):
    for file in files:
        if file.endswith(".py") and not file.startswith(("chevrolet","utils", "constants" "pylint_score", "ford")):
            file_ = os.path.join(root, file)
            results = lint.Run([file_], do_exit=False)
            score = results.linter.stats['global_note']
            if score < THRESHOLD:
                OUTPUT = 'FAILED'
            elif score > THRESHOLD:
                OUTPUT = 'PASSED'
            print(f'Score for {file_} is {score} and it {OUTPUT}.')

sys.exit(0)