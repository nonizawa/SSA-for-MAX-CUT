#!/bin/bash

# Define constants
PARAM_TYPE=1
CYCLE=1000 # Number of cycles per trial
TRIAL=100  # Number of trials
TAU=1

# Loop through all .txt files in the graph/ directory
for file in graph/*.txt
do
    # Display a message indicating which file is being processed
    echo "Processing file: $file"
    
    # Run the simulated annealing algorithm script (sa.py) using python located at /xxx/yyy/
    # Pass in the defined constants as command line arguments along with the current file path
    /xxx/yyy/python ssau.py --cycle $CYCLE  --trial $TRIAL --tau $TAU --param $PARAM_TYPE --file_path "$file"
done


