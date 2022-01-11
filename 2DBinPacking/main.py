import time

from src.DataProcess import DataProcess
from src.BinPack import *

if __name__ == "__main__":
    # Time Calculate
    START = time.time()

    # DataProcess
    data = DataProcess(config_path="src/config.txt")
    print("JOBS_dict: ", data.instanceDict['JOBS'])

    # METHOD 1 : HEURISTIC METHOD
    ## Step1 Job Sequence (Largest Size)
    job_sequence = largest_area_sort(data.instanceDict['JOBS'])
    print("job sequence(sorted by area large to small): ", job_sequence)

    ## Step2 Apply BFF with ordered Job Sequence
    solution, B_EMSs, data = BFF_Heuristic(job_sequence, data)
    # solution = [job_no, batch_no, x1, y1, x2, y2]
    print()

    # METHOD 2 : BRKGA

    # End Program
    print("Spent {} second(s)".format(time.time() - START))