import numpy as np
import time
import random
import math
import csv
import sys
import os
import argparse

# Set verbose to True for detailed output
verbose = True
# Record the start time of the program
starttime = time.time()

# Parsing command line arguments
parser = argparse.ArgumentParser(description="Specify GPU device number")
parser.add_argument('--file_path', type=str, required=True, help="File path for data")
parser.add_argument('--param', type=int, default=1, help="Parameter type (default: 1)")
parser.add_argument('--cycle', type=int, default=1000, help="Number of cycles (default: 1000)")
parser.add_argument('--trial', type=int, default=100, help="Number of trials (default: 100)")
parser.add_argument('--tau', type=int, default=1, help="tau (default: 1)")
args = parser.parse_args()

# Define the fun_Itanh function, which calculates and returns the Itanh value based on inputs
def fun_Itanh(Itanh, I_vector, I0):
    discriminant = Itanh + I_vector
    Itanh = np.where(discriminant >= I0, I0, discriminant)
    Itanh = np.where(discriminant < -I0, -I0, Itanh)
    return Itanh

# Define the annealing function, which performs simulated annealing and returns the final spin vector and annealing time
def annealing(tau, I0_min, I0_max, beta, nrnd, Mshot, J_matrix, spin_vector, Itanh_ini):
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

# Read the input file
file_path = args.file_path
dir_path, file_name = os.path.split(file_path)
with open(file_path, 'r') as f:
    # Read lines from the file
    first_line = f.readline().strip() # graph name
    second_line = f.readline().strip() # edge value: bipolar or unipolar
    third_line = f.readline().strip() # edge type
    fourth_line = f.readline().strip() # best-known value
    lines = f.readlines()

# Parse the vertex count from the file and create graph matrix
vertex = np.int32(first_line)
G_matrix = get_graph(vertex, lines)
J_matrix = -G_matrix
best_known = np.int32(fourth_line)

# Set parameters for simulated annealing
mean_each = []
std_each = []
for j in range(vertex):
    mean_each.append((vertex-1)*np.mean(J_matrix[j]))
    std_each.append(np.sqrt((vertex-1)*np.var(J_matrix[j])))
sigma = np.mean(std_each)
mean = np.mean(mean_each)

# Output mean and sigma if verbose is True
if verbose:
    print('mean = ', mean)
    print('sigma = ', sigma)

# Setting more parameters for the simulated annealing
min_cycle = np.int32(args.cycle)
trial = np.int32(args.trial)
Mshot = np.int32(1)
nrnd = np.float32(0.67448975 * sigma)

# Setting the parameters based on the argument param
param = args.param
if param == 1:
    I0_min = np.float32(sigma * 0.01 + abs(mean))
    I0_max = np.float32(sigma * 2 + np.abs(mean))

# More parameters
tau = np.int32(args.tau)
beta = np.float32((I0_min / I0_max) ** (tau / (min_cycle - 1)))
max_cycle = math.ceil((math.log10(I0_min / I0_max) / math.log10(beta))) * tau

# Output parameters if verbose is True
if verbose:
    print('trials:', trial)
    print("Min Cycles :", min_cycle)
    print('beta:', beta)
    print('I0_min:', I0_min)
    print('I0_max:', I0_max)
    print('tau:', tau)
    print('nrnd', nrnd)

# Initializing Itanh and performing the annealing
Itanh_ini = (np.random.randint(0, 3, (vertex, 1)) - 1) * I0_min
cut_sum = 0
time_sum = 0
cut_list = []
for k in range(trial):
    ini_spin_vector = np.random.randint(0, 2, (vertex, 1))
    ini_spin_vector = np.where(ini_spin_vector == 0, -1, 1)
    (last_spin_vector, annealing_time) = annealing(tau, I0_min, I0_max, beta, nrnd, Mshot, J_matrix, ini_spin_vector, Itanh_ini)
    cut_val = cut_calculate(G_matrix, last_spin_vector)
    min_energy = energy_calculate(J_matrix, last_spin_vector)
    cut_sum += cut_val
    cut_list.append(cut_val)
    time_sum += annealing_time
    
    # Output results for this trial
    print('File_name:', file_name, "Trial", k + 1)
    if verbose:
        print("Trial", k + 1)
        print('Cut value :', cut_val)
        print('Min energy :', min_energy)
        print("Annealing time :", annealing_time)

# Calculate and output the average results over all trials
cut_average = cut_sum / trial
cut_max = max(cut_list)
cut_min = min(cut_list)
time_average = time_sum / trial
print('Cut value average :', cut_average)
print('Cut value max :', cut_max)
print('Cut value min :', cut_min)
print('Time average :', time_average)

# Output total time taken
print("Total time:", time.time() - starttime)

# Define data to be written to csv
data = [
    file_name, first_line, second_line, third_line, fourth_line, cut_average, cut_max, cut_min, I0_min, I0_max, 100*cut_average/best_known, 100*cut_max/best_known, time_average]

# Define file names for output csv files
csv_file_name1 = './result/result_cpu_cycle{}_trial{}_tau{}_param{}.csv'.format(args.cycle, args.trial, args.tau, args.param)
csv_file_name2 = './result/cut_cpu_cycle{}_trial{}_tau{}_param{}.csv'.format(args.cycle, args.trial, args.tau, args.param)

# Write data to csv files
if os.path.isfile(csv_file_name1):
    with open(csv_file_name1, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)
else:
    with open(csv_file_name1, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Gset', 'number of edges', 'edge value', 'edge type', 'best-known value', 'mean_cut_value', 'man_cut_value', 'min_cut_value', 'I0_min', 'I0_max', 'ratio of mean/best', 'ratio of max/best', 'mean_time'])
        writer.writerow(data)

# Write cut list to csv
with open(csv_file_name2, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(cut_list)
