#!/bin/bash

# Define constants
CYCLE=1000      # Number of cycles per trial
TRIAL=100       # Number of trials
T_INI=1         # Initial temperature for simulated annealing algorithm
T_MIN=1e-3      # Minimum temperature for simulated annealing algorithm

# Loop through all .txt files in the graph/ directory
for file in graph/*.txt
do
    # Display a message indicating which file is being processed
    echo "Processing file: $file"
    
    # Run the simulated annealing algorithm script (sa.py) using python located at /xxx/yyy/
    # Pass in the defined constants as command line arguments along with the current file path
    /xxx/yyy/python sa.py --cycle $CYCLE  --trial $TRIAL --T_ini $T_INI --T_min $T_MIN --file_path "$file"
done
