import argparse
import random
import os
import numpy as np
import time

def parse_command_line_args():
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: Namespace containing command line arguments.
    """

    # Parsing command line arguments
    parser = argparse.ArgumentParser(description="Specify GPU device number")
    parser.add_argument('--file_path', type=str, required=True, help="File path for data")
    parser.add_argument('--param', type=int, default=1, help="Parameter type (default: 1)")
    parser.add_argument('--cycle', type=int, default=1000, help="Number of cycles (default: 1000)")
    parser.add_argument('--trial', type=int, default=100, help="Number of trials (default: 100)")
    parser.add_argument('--tau', type=int, default=1, help="tau (default: 1)")
    args = parser.parse_args()

    return args


# Define the fun_Itanh function, which calculates and returns the Itanh value based on inputs
def fun_Itanh(Itanh, I_vector, I0):
    discriminant = Itanh + I_vector
    Itanh = np.where(discriminant >= I0, I0, discriminant)
    Itanh = np.where(discriminant < -I0, -I0, Itanh)
    return Itanh

# Define the annealing function, which performs simulated annealing and returns the final spin vector and annealing time
def annealing(tau, I0_min, I0_max, beta, nrnd, Mshot, J_matrix, spin_vector, Itanh_ini, vertex):
    Itanh = Itanh_ini
    start_time = time.time()
    for i in range(Mshot): 
        I0 = I0_min
        while I0 <= I0_max:
            for i in range(tau):
                rnd = np.random.randint(0, 2, (vertex, 1)) # Generate random noise of 0 and 1
                rnd = np.where(rnd == 0, -1, 1) # Convert noise to -1 and 1
                I_vector = np.dot(J_matrix, spin_vector) + nrnd * rnd
                Itanh = fun_Itanh(Itanh, I_vector, I0)
                spin_vector = np.where(Itanh >= 0, 1, -1)
            I0 = I0 / beta
    end_time = time.time() 
    annealing_time = end_time - start_time
    return (spin_vector, annealing_time)

# Define the cut_calculate function, which calculates and returns the cut value based on inputs
def cut_calculate(G_matrix, spin_vector):
    spin_vector_reshaped = np.reshape(spin_vector, (len(spin_vector),))
    upper_triangle = np.triu_indices(len(spin_vector), k=1) # Get indices of upper triangle
    cut_val = np.sum(G_matrix[upper_triangle] * (1 - np.outer(spin_vector_reshaped, spin_vector_reshaped)[upper_triangle])) # Calculate cut_val
    return int(cut_val/2)

# Define the energy_calculate function, which calculates and returns the energy based on inputs
def energy_calculate(J_matrix, spin_vector):
    Jm_tmp = np.dot(J_matrix, spin_vector)
    return -np.sum(Jm_tmp * spin_vector) / 2

# Define the get_graph function, which constructs and returns the adjacency matrix G_matrix based on the graph
def get_graph(vertex, lines):
    G_matrix = np.zeros((vertex, vertex), int)
    
    # Counting the number of lines (edges)
    line_count = len(lines)
    print('Number of Edges :', line_count)
    
    # Iterating through the lines to construct the adjacency matrix
    for line_text in lines:
        weight_list = list(map(int, line_text.split(' ')))  # Convert space-separated string to list of integers
        i = weight_list[0] - 1
        j = weight_list[1] - 1
        G_matrix[i, j] = weight_list[2]  # Assign weight to the corresponding entry in the matrix
    
    # Adding the matrix to its transpose to make it symmetric
    G_matrix = G_matrix + G_matrix.T
    return G_matrix

def read_and_process_file(file_path):
    """
    Reads and processes the input file.

    Parameters:
        args (argparse.Namespace): A namespace containing the file_path.

    Returns:
        J_matrix (numpy.ndarray): The negative of the graph matrix.
        best_known (int): The best-known value parsed from the file.
    """

    name = [None] * 5
    # Read the input file
    dir_path, name[0] = os.path.split(file_path)

    with open(file_path, 'r') as f:
        # Read lines from the file
        name[1] = f.readline().strip()  # number of nodes
        name[2] = f.readline().strip()  # edge value: bipolar or unipolar
        name[3] = f.readline().strip()  # edge type
        name[4] = f.readline().strip()  # best-known value
        lines = f.readlines()

    # Parse the vertex count from the file and create graph matrix
    vertex = np.int32(name[1])
    G_matrix = get_graph(vertex, lines)
    J_matrix = -G_matrix
    best_known = np.int32(name[4])

    return vertex, G_matrix, J_matrix, best_known, name 

