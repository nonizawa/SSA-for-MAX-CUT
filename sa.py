import numpy as np
import time
import os
import math
import csv
import pandas as pd
import argparse

starttime = time.time()

# Parsing command line arguments
parser = argparse.ArgumentParser(description="Specify GPU device number")
parser.add_argument('--file_path', type=str, required=True, help="File path for data")
parser.add_argument('--cycle', type=int, default=1000, help="Number of ccyles (default: 1000)")
parser.add_argument('--T_ini', type=float, default=1, help="Initial temperature (default: 1)")
parser.add_argument('--T_min', type=float, default=1e-3, help="Minimum temperature (default: 1e-3)")
parser.add_argument('--trial', type=int, default=100, help="Number of trials (default: 100)")
args = parser.parse_args()

def cut_calculate(G_matrix, spin_vector):
    spin_vector_reshaped = np.reshape(spin_vector, (len(spin_vector),)) # spin_vectorを1次元配列に変換
    upper_triangle = np.triu_indices(len(spin_vector), k=1) # 上三角行列のインデックスを取得
    cut_val = np.sum(G_matrix[upper_triangle] * (1 - np.outer(spin_vector_reshaped, spin_vector_reshaped)[upper_triangle])) # 上三角行列の要素のみを計算してcut_valを算出
    return int(cut_val/2)

def image1to2(mi,tri,amin,H,W,N):
    state = mi[tri, amin].reshape((H, W))
    return state

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

file_path = args.file_path
dir_path, file_name = os.path.split(file_path)
with open(file_path, 'r') as f:
    # 1行目を取得する
    first_line = f.readline().strip() #Number of nodes
    second_line = f.readline().strip() #unipolar or bipolar
    third_line = f.readline().strip() #planer or random
    fourth_line = f.readline().strip() #best known
    lines = f.readlines()

vertex = np.int32(first_line) 
G_matrix = get_graph(vertex, lines)
J =  - G_matrix
best_known = np.int32(fourth_line)
h = np.zeros(vertex, dtype=int)

trial = args.trial
T_ini = args.T_ini
T_min = args.T_min
cycle = args.cycle
cool = np.exp(math.log((T_min/T_ini))/(cycle-1))
k = 1

print('T_ini = ', T_ini)
print('T_min = ', T_min)
print('Cycles = ', cycle)
print('Trials = ',trial)
print('Cool =',cool)

temp_list = []
time_list = []
cut_value_list = []
energy_list = []

for tri in range(trial):
    # Initial remperature
    st = time.time()
    temp = T_ini
    ini_spin_vector = np.random.randint(0, 2, size=vertex) * 2 - 1
    # Current eng calculation
    hm_tmp = np.dot(ini_spin_vector, h)
    Jm_tmp = np.dot(J, ini_spin_vector)
    e1 = -np.sum(Jm_tmp * ini_spin_vector) / 2 - hm_tmp
    spin_vector = ini_spin_vector.copy()
    for i in range(cycle):
       
        cur_spin_vector = spin_vector.copy()
        flip = np.random.randint(0, vertex)
        spin_vector[flip] = spin_vector[flip] * -1

        # Next eng calculation
        hm_tmp = np.dot(spin_vector, h)
        Jm_tmp = np.dot(J, spin_vector)
        e2 = - np.sum(Jm_tmp * spin_vector) / 2 - hm_tmp

        # Probability calculation
        diff_e = e2 - e1
        p = np.exp((-diff_e) / (k * temp))
        if np.isinf(p):
            p = 1.0

        rnd = np.random.rand(1)[0]

        if p < rnd:
            spin_vector = cur_spin_vector.copy()
            #print('non flip')
        else:
            e1 = e2
        
        temp = temp * cool
        if i == cycle-1:
            if p < rnd:
                last_energy = e1
            else:
                last_energy = e2

    et = time.time()
    print(str(tri + 1) + '-th trial end!')
    print('Time =', et - st)
    time_list.append(et - st)

    cut_value = cut_calculate(G_matrix, spin_vector)
    cut_value_list.append(cut_value)
    energy_list.append(last_energy)
    print('Last cycle =',cycle)
    print('Cut value =', cut_value)
    print('Last energy = ', last_energy)

print('min_cut_value =',np.min(cut_value_list))
print('mean_cut_value = ',np.mean(cut_value_list))
print('max_cut_value = ',np.max(cut_value_list))
print('mean_time = ', np.mean(time_list))

print("Total time:", time.time()-starttime)

if os.path.isfile("./result/result_sa.csv"): # "result.csv" ファイルが存在する場合
    with open("./result/result_sa.csv", 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([file_name,T_ini,T_min,cycle,trial,best_known,np.mean(cut_value_list), np.max(cut_value_list), np.min(cut_value_list), np.mean(time_list)])
else: # "result_sa.csv" 
    with open("./result/result_sa.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Gset','T_ini','T_min','cycle','trial','best-known value','mean_cut_value', 'max_cut_value', 'min_cut_value', 'mean_time'])
        writer.writerow([file_name,T_ini,T_min,cycle,trial,best_known,np.mean(cut_value_list), np.max(cut_value_list), np.min(cut_value_list), np.mean(time_list)])

with open('./result/cut_value_sa.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(cut_value_list)
