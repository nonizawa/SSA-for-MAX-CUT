import numpy as np
import time
import random
import math
import csv
import sys
import os
import argparse

# Set verbose to True to print detailed log information
verbose = True

# Record the start time of the script
starttime = time.time()

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="Specify GPU device number")
parser.add_argument('--file_path', type=str, required=True, help="File path for data")
parser.add_argument('--param', type=int, default=1, help="Parameter type (default: 1)")
parser.add_argument('--cycle', type=int, default=1000, help="Number of cycles (default: 1000)")
parser.add_argument('--trial', type=int, default=100, help="Number of trials (default: 100)")
parser.add_argument('--tau', type=int, default=1, help="tau (default: 1)")
args = parser.parse_args()

# Define the Itanh function used for annealing
def fun_Itanh(Itanh, I_vector, I0):
    discriminant = Itanh + I_vector
    Itanh = np.where(discriminant >= I0, I0, discriminant)
    Itanh = np.where(discriminant < -I0, -I0, Itanh)
    return Itanh

# Define the annealing function
def annealing(tau, I0_min, I0_max, beta, nrnd_vector, Mshot, J_matrix, spin_vector, Itanh_ini):
    Itanh = Itanh_ini
    start_time = time.time()
    for i in range(Mshot):
        I0 = I0_min
        while I0 <= I0_max:
            for i in range(tau):
                rnd = np.random.randint(0, 2, (vertex, 1))  # Generate random noise of 0s and 1s
                rnd = np.where(rnd == 0, -1, 1)  # Convert random noise to -1s and 1s
                I_vector = np.dot(J_matrix, spin_vector) + nrnd_vector * rnd
                Itanh = fun_Itanh(Itanh, I_vector, I0)
                spin_vector = np.where(Itanh >= 0, 1, -1)
            I0 = I0 / beta
    end_time = time.time()
    annealing_time = end_time - start_time
    return (spin_vector, annealing_time)

# Define the function to calculate the cut value
def cut_calculate(G_matrix, spin_vector):
    spin_vector_reshaped = np.reshape(spin_vector, (len(spin_vector),))
    upper_triangle = np.triu_indices(len(spin_vector), k=1)
    cut_val = np.sum(G_matrix[upper_triangle] * (1 - np.outer(spin_vector_reshaped, spin_vector_reshaped)[upper_triangle]))
    return int(cut_val / 2)

# Define the function to calculate the energy
def energy_calculate(J_matrix, spin_vector):
    Jm_tmp = np.dot(J_matrix, spin_vector)
    return -np.sum(Jm_tmp * spin_vector) / 2

# Define the function to construct the graph's adjacency matrix
def get_graph(vertex, lines):
    G_matrix = np.zeros((vertex, vertex), int)
    line_count = len(lines)
    if verbose:
        print('Number of Edges :', line_count)
    for line_text in lines:
        weight_list = list(map(int, line_text.split(' ')))
        i = weight_list[0] - 1
        j = weight_list[1] - 1
        G_matrix[i, j] = weight_list[2]
    G_matrix = G_matrix + G_matrix.T
    return G_matrix

# Read the file and parse it to extract relevant information
file_path = args.file_path
dir_path, file_name = os.path.split(file_path)
with open(file_path, 'r') as f:
    first_line = f.readline().strip()
    second_line = f.readline().strip()
    third_line = f.readline().strip()
    fourth_line = f.readline().strip()
    lines = f.readlines()

# Set up initial parameters
vertex = np.int32(first_line)
G_matrix = get_graph(vertex, lines)
J_matrix = -G_matrix
best_known = np.int32(fourth_line)

# Calculate statistical values for SA-SC parameters
mean_each = []
std_each = []
for j in range(vertex):
    mean_each.append((vertex - 1) * np.mean(J_matrix[j]))
    std_each.append(np.sqrt((vertex - 1) * np.var(J_matrix[j])))

# Reshape sigma vector
sigma_vector = np.array(std_each, dtype=np.float32)
sigma_vector = sigma_vector.reshape((-1, 1))

# Output information if verbose is True
if verbose:
    print('mean mean = ', np.mean(mean_each))
    print('max mean = ', np.max(mean_each))
    print('min mean = ', np.min(mean_each))
    print('mean std = ', np.mean(std_each))
    print('max std = ', np.max(std_each))
    print('min std = ', np.min(std_each))

# Setting more parameters for the annealing process
min_cycle = np.int32(args.cycle)
trial = np.int32(args.trial)
Mshot = np.int32(1)
nrnd_vector = np.float32(0.67448975 * sigma_vector)
nrnd_max = np.max(nrnd_vector)
param = args.param

if param == 1:
    I0_min = np.float32(np.max(sigma_vector) * 0.01 + np.min(np.abs(mean_each)))
    I0_max = np.float32(np.max(sigma_vector) * 2 + np.min(np.abs(mean_each)))

tau = np.int32(args.tau)
beta = np.float32((I0_min / I0_max) ** (tau / (min_cycle - 1)))
max_cycle = math.ceil((math.log10(I0_min / I0_max) / math.log10(beta))) * tau

# Main execution of the annealing process
if verbose:
    print('trials:', trial)
    print("Min Cycles :", min_cycle)
    print('beta:', beta)
    print('I0_min:', I0_min)
    print('I0_max:', I0_max)
    print('tau:', tau)

Itanh_ini = np.zeros((vertex, 1), int)
cut_sum = 0
time_sum = 0
cut_list = []

# Loop through the number of trials
for k in range(trial):
    ini_spin_vector = np.random.randint(0, 2, (vertex, 1))
    ini_spin_vector = np.where(ini_spin_vector == 0, -1, 1)
    (last_spin_vector, annealing_time) = annealing(tau, I0_min, I0_max, beta, nrnd_vector, Mshot, J_matrix, ini_spin_vector, Itanh_ini)
    cut_val = cut_calculate(G_matrix, last_spin_vector)
    min_energy = energy_calculate(J_matrix, last_spin_vector)
    cut_sum += cut_val
    cut_list.append(cut_val)
    time_sum += annealing_time
    print('File_name:', file_name, "Trial", k + 1)
    if verbose:
        print("Trial", k + 1)
        print('Cut value :', cut_val)
        print('Min energy :', min_energy)
        print("Annealing time :", annealing_time)

# Calculate final results
cut_average = cut_sum / trial
cut_max = max(cut_list)
cut_min = min(cut_list)
time_average = time_sum / trial
print('Cut value average :', cut_average)
print('Cut value max :', cut_max)
print('Cut value min :', cut_min)
print('Time average :', time_average)

# Output total execution time
print("Total time:", time.time() - starttime)

# Organize data for output
data = [
    file_name, first_line, second_line, third_line, fourth_line, cut_average, cut_max, cut_min, I0_min, I0_max, 100 * cut_average / best_known, 100 * cut_max / best_known, time_average]

# Create file names for the output
csv_file_name1 = './result/result_cpu_vector_cycle{}_trial{}_tau{}_param{}.csv'.format(args.cycle, args.trial, args.tau, args.param)
csv_file_name2 = './result/cut_cpu_vector_cycle{}_trial{}_tau{}_param{}.csv'.format(args.cycle, args.trial, args.tau, args.param)

# Write data to csv files
if os.path.isfile(csv_file_name1):
    with open(csv_file_name1, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)
else:
    with open(csv_file_name1, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Gset', 'number of edges','edge value', 'edge type', 'best-known value', 'mean_cut_value', 'man_cut_value', 'min_cut_value', 'I0_min', 'I0_max', 'ratio of mean/best', 'ratio of max/best', 'mean_time'])
        writer.writerow(data)

# Write the cut list to a csv file
with open(csv_file_name2, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(cut_list)
