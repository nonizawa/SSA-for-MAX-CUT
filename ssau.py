import numpy as np
import time
import random
import math
import csv
import sys
import os
import utils as ut
import statistics

# Set verbose to True to print detailed log information
verbose = True

# Record the start time of the script
starttime = time.time()

args = ut.parse_command_line_args()
vertex, G_matrix, J_matrix, best_known, name = ut.read_and_process_file(args.file_path)

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
elif param == 2:
    I0_min = np.float32(np.mean(sigma_vector) * 0.01 + np.mean(np.abs(mean_each)))
    I0_max = np.float32(np.mean(sigma_vector) * 2 + np.mean(np.abs(mean_each)))

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
    (last_spin_vector, annealing_time) = ut.annealing(tau, I0_min, I0_max, beta, nrnd_vector, Mshot, J_matrix, ini_spin_vector, Itanh_ini, vertex)
    cut_val = ut.cut_calculate(G_matrix, last_spin_vector)
    min_energy = ut.energy_calculate(J_matrix, last_spin_vector)
    cut_sum += cut_val
    cut_list.append(cut_val)
    time_sum += annealing_time
    print('File_name:', name[0], "Trial", k + 1)
    if verbose:
        print('Cut value :', cut_val)
        print('Min energy :', min_energy)
        print("Annealing time :", annealing_time)

# Calculate final results
cut_average = cut_sum / trial
cut_max = max(cut_list)
cut_min = min(cut_list)
time_average = time_sum / trial
std_cut = statistics.stdev(cut_list)
print('Cut value average :', cut_average)
print('Cut value max :', cut_max)
print('Cut value min :', cut_min)
print('Time average :', time_average)
print('Std of cut value :', std_cut)

# Output total execution time
print("Total time:", time.time() - starttime)

# Define data to be written to csv
data = [
    name[0], name[1], name[2], name[3], name[4], cut_average, cut_max, cut_min, std_cut, 0.67448975*np.mean(sigma_vector), I0_min, I0_max, 100*cut_average/best_known, 100*cut_max/best_known, time_average]

# Create file names for the output
csv_file_name1 = './result/result_ssau_vector_cycle{}_trial{}_tau{}_param{}.csv'.format(args.cycle, args.trial, args.tau, args.param)
csv_file_name2 = './result/cut_ssau_vector_cycle{}_trial{}_tau{}_param{}.csv'.format(args.cycle, args.trial, args.tau, args.param)

# Write data to csv files
if os.path.isfile(csv_file_name1):
    with open(csv_file_name1, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)
else:
    with open(csv_file_name1, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Gset', 'number of edges', 'edge value', 'edge type', 'best-known value', 'mean_cut_value', 'man_cut_value', 'min_cut_value', 'std_cut_value', 'n_rnd', 'I0_min', 'I0_max', 'ratio of mean/best', 'ratio of max/best', 'mean_time'])
        writer.writerow(data)

# Write the cut list to a csv file
with open(csv_file_name2, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(cut_list)
