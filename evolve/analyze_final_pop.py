import json
import ast
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from lfr_graph import create_matrix


def histograms(population):
    diffusion = [x[0] for x in population]
    seeding = [x[1] for x in population]
    clear = [x[2] for x in population]

    figure, axis = plt.subplots(3, 1, figsize=(9, 18))
    axis[0].hist(diffusion)
    axis[1].hist(seeding)
    axis[2].hist(clear)
    axis[0].set_xlabel('diffusion')
    axis[1].set_xlabel('seeding')
    axis[2].set_xlabel('clear')

    plt.savefig('histograms.png')


def pareto_front(fitnesses):
    biomass = [x['Biomass'] for x in fitnesses]
    growth_rate = [x['Growth_Rate'] for x in fitnesses]
    heredity = [x['Heredity'] for x in fitnesses]

    #fig = plt.figure()
    #ax = plt.axes(projection="3d")
    #ax.scatter(biomass, growth_rate, heredity)

    figure, axis = plt.subplots(3, 1, figsize=(9, 18))
    axis[0].scatter(biomass, growth_rate)
    axis[1].scatter(growth_rate, heredity)
    axis[2].scatter(heredity, biomass)
    axis[0].set_xlabel('biomass')
    axis[0].set_ylabel('growth rate')
    axis[1].set_xlabel('growth rate')
    axis[1].set_ylabel('heredity')
    axis[2].set_xlabel('heredity')
    axis[2].set_ylabel('biomass')

    plt.savefig('pareto.png')


def visualize_network(input_name, output_name):
    matrix = np.loadtxt(input_name, delimiter=',')

    #https://stackoverflow.com/questions/23994020/colorplot-that-distinguishes-between-positive-and-negative-values
    cmap = plt.get_cmap('PuOr')
    cmaplist = [cmap(i) for i in range(cmap.N)]
    cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
    bounds = [-1, -0.75, -0.5, -0.25, -.0001, .0001, 0.25, 0.5, 0.75, 1]
    norm = BoundaryNorm(bounds, cmap.N)

    plt.imshow(matrix, cmap=cmap, interpolation='none', norm=norm)
    plt.colorbar()
    plt.savefig(output_name)


def create_matrix_unformatted(genome):
    diffusion = genome[0]
    seeding = genome[1]
    clear = genome[2]
    average_k = genome[12]
    max_degree = genome[13]
    mut = genome[3]
    muw = genome[4]
    beta = genome[5]
    com_size_min = genome[10]
    com_size_max = genome[11]
    tau = genome[6]
    tau2 = genome[7]
    overlapping_nodes = genome[14]
    overlap_membership = genome[15]
    pct_pos_in = genome[8]
    pct_pos_out = genome[9]
    matrix = create_matrix(num_nodes=9, average_k=average_k, max_degree=max_degree, mut=mut, muw=muw, beta=beta, com_size_min=com_size_min, com_size_max=com_size_max, tau=tau, tau2=tau2, overlapping_nodes=overlapping_nodes, overlap_membership=overlap_membership, pct_pos_in=pct_pos_in, pct_pos_out=pct_pos_out)
    return matrix


def check_matrices(population):
    zeros = 0
    unique = []
    for genome in population:
        matrix = create_matrix_unformatted(genome)
        if sum([sum(x) for x in matrix]) == 0:
            zeros += 1
        if genome[3:] not in unique:
            unique.append(genome[3:])
    print(f'error matrices: {zeros}')
    print(f'unique matrices: {len(unique)}')


def get_final_pop():
    final_pop = open('final_population').read()
    pop_list = []
    fitness_list = []
    for line in final_pop.split('\n'):
        if len(line) > 0:
            if line[0] == '{':
                fitnesses, genome = line.split('} ')
                fitnesses = json.loads(fitnesses.replace('\'', '\"') + '}')
                genome = ast.literal_eval(genome[1:])
                pop_list.append(genome)
                fitness_list.append(fitnesses)
    return pop_list, fitness_list


if __name__ == '__main__':
    population, fitnesses = get_final_pop()
    check_matrices(population)

    interactions = create_matrix_unformatted(population[0])
    with open("interaction_matrix.dat", "w") as f:
        wr = csv.writer(f)
        wr.writerows(interactions)
    visualize_network('interaction_matrix.dat', 'interaction_matrix.png')