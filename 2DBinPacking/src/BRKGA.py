import numpy as np
import copy
import random

from src.BinPack import *

class BRKGA():
    def __init__(self, data, num_generations = 200, p = 100, num_elites = 100*0.25, num_mutants = 100*0.1, elite_inheritance_prob = 0.8):
        self.data = copy.deepcopy(data) # 排程輸入資料
        self.used_bin_LB = self.data.used_bin_LB
        self.residual_area_LB = self.data.residual_area_LB

        # Configuration
        self.num_generations = num_generations # num of generation
        self.gene_len = self.data.num_jobs
        self.p = int(p) # size of population
        self.num_elites = int(num_elites) # size of elite population
        self.num_mutants = int(num_mutants) # size of mutant population
        self.elite_inheritance_prob = elite_inheritance_prob # elite allel inheritance prob

        # Results
        self.solution = None
        self.B_EMSs = None
        self.jobResults = None
        self.used_bin = -1

        self.best_fitness = -1
        self.history = { "mean" : [], "min" : [] }

    def getBestSolution(self, best_gene):
        # 產生 Job sequence
        job_sequence = np.argsort(best_gene[:])
        # BFF演算法擺放 回傳solution
        solution, B_EMSs, jobResults, max_opened_batch_no = BFF_Heuristic(job_sequence, self.data)
        # 針對BFF結果( 回傳 list = [ 剩餘空間, 使用bin數 ] )
        fitness = evaluate_fitness(self.data.job_total_area, max_opened_batch_no, self.data.BIN_AREA)

        ## solution = [job_no, batch_no, orientation, x1, y1, x2, y2]
        ## B_EMSs = { batch_no : ems_object}
        ## jobResults = { job_no : job_object (filled information with coordinate) }
        return solution, B_EMSs, jobResults, fitness[1]

    def cal_fitness(self, population):
        fitness_list = []
        for ind in population:
            # 產生 Job sequence
            job_sequence = np.argsort(ind[:])
            # BFF演算法擺放 回傳solution
            solution, B_EMSs, jobResults, max_opened_batch_no = BFF_Heuristic(job_sequence, self.data)
            # 針對BFF結果( 回傳 list = [ 剩餘空間, 使用bin數 ] )
            fitness = evaluate_fitness(self.data.job_total_area, max_opened_batch_no, self.data.BIN_AREA)
            # fitness value  [0] : 剩餘空間, [1] : 使用bin數
            fitness_list.append(fitness[1])
        
        fitness_list = np.array(fitness_list).reshape((len(population), 1))
        return fitness_list

    def partition(self, population, fitness_list):
        "population 區分出 elites , non_elites 並儲存elite_fitness_list"
        sorted_indexs = np.argsort(fitness_list)
        sorted_indexs = [x.item() for x in sorted_indexs] # convert np.int64 to int
        return population[sorted_indexs[:self.num_elites]], population[sorted_indexs[self.num_elites:]], fitness_list[sorted_indexs[:self.num_elites]]

    def crossover(self, elite, non_elite):
        return [elite[i] if np.random.uniform(low=0.0, high=1.0) < self.elite_inheritance_prob else non_elite[i] for i in range(self.gene_len)]

    def mating(self, elites, non_elites):
        num_offspring = self.p - self.num_elites - self.num_mutants
        # selected_elite = random.choice(elites)
        # selected_non_elite = random.choice(non_elites)
        return [self.crossover(random.choice(elites), random.choice(non_elites)) for i in range(num_offspring)]

    def mutants(self):
        return np.random.uniform(low=0.0, high=1.0, size=(self.num_mutants, self.gene_len))

    def run(self, patient_generation = 10):
        "直接在 外面main call model.run() (BRKGA object)"
        
        print(" === Start to run BRKGA === ")
        # Initialize 
        ## population & fitness
        population = np.random.uniform(low=0.0, high=1.0, size=(self.p, self.gene_len))
        fitness_list = self.cal_fitness(population)

        ## Record best result
        best_fitness = np.min(fitness_list)
        best_gene = population[np.argmin(fitness_list)]
        self.history['min'].append(np.min(fitness_list))
        self.history['mean'].append(np.mean(fitness_list))

        # Start run generations
        best_generation = 0
        for g in range(self.num_generations):
            
            # Early stopping condition ( & return 'feasible')
            
            # Partition elite, non_elite group And select elite fitness list (複製全部菁英)
            elites, non_elites, elite_fitness_list = self.partition(population, fitness_list)

            # Biased mating & crossover (菁英與非菁英交配)
            offsprings = self.mating(elites, non_elites)

            # Generate mutants (突變)
            mutants = self.mutants()

            # New Population & fitness
            offsprings = np.concatenate((mutants,offsprings), axis=0)
            offspring_fitness_list = self.cal_fitness(offsprings)
            population = np.concatenate((elites, offsprings), axis = 0)
            fitness_list = np.concatenate((elite_fitness_list, offspring_fitness_list), axis = 0)

            # Update Best Fitness
            for fitness in fitness_list:
                if fitness < best_fitness:
                    best_generation = g
                    best_fitness = fitness
                    best_gene = population[np.argmin(fitness_list)]

            # 紀錄當下generation結果
            self.history['min'].append(np.min(fitness_list))
            self.history['mean'].append(np.mean(fitness_list))
            print("Generation : {} \t( Best Fitness: {} )".format(g, best_fitness))

        # 將BRKGA演算結果存回model物件內
        #self.used_bins = math.floor(best_fitness)
        self.best_fitness = best_fitness
        self.solution, self.B_EMSs, self.jobResults, self.used_bin = self.getBestSolution(best_gene)
        
        # return 'feasible'
        return "feasible"




