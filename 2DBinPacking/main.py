import time
import pprint

from src.DataProcess import DataProcess
from src.BinPack import *
from src.BRKGA import *
from src.plot import *

if __name__ == "__main__":
    # Time Calculate
    START = time.time()

    # DataProcess
    data = DataProcess(config_path="src/config.txt")
    print("Jobs Information: ")
    pprint.pprint(data.instanceDict['JOBS'])

    ## METHOD 1 : HEURISTIC METHOD
    ## Step1 Job Sequence (Largest Size)
    #job_sequence = largest_area_sort(data.instanceDict['JOBS'])

    ## Step2 Apply BFF with ordered Job Sequence
    #solution, B_EMSs, jobResults, max_opened_batch_no = BFF_Heuristic(job_sequence, data)
    #fitness = evaluate_fitness(data.job_total_area, max_opened_batch_no, data.BIN_AREA)
    #print("fitness : 剩餘空間為 {} , 共使用 {} 個bin".format(fitness[0], fitness[1]))
    
    ### Step3 draw rectangle
    #plot_one_bin(data, solution, b_no = 0, show_switch = True, save_switch = False)


    # METHOD 2 : BRKGA
    BRKGA_model = BRKGA(data, num_generations = 10, p = 100, num_elites = 100*0.25, num_mutants = 100*0.1, elite_inheritance_prob = 0.8)
    BRKGA_model.run()
    solution = BRKGA_model.solution # solution = [job_no, batch_no, orientation, x1, y1, x2, y2]

    ## draw rectangle
    plot_one_bin(data, solution, b_no = 0, show_switch = True, save_switch = False)

    # End Program
    print("Spent {} second(s)".format(time.time() - START))
    print()