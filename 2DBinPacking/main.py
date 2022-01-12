import time
from PIL import Image, ImageDraw

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
    # solution = [job_no, batch_no, orientation, x1, y1, x2, y2]
    # B_EMSs = { batch_no : ems_object}
    # jobResults = { job_no : job_object (filled information with coordinate) }
    
    solution, B_EMSs, jobResults, max_opened_batch_no = BFF_Heuristic(job_sequence, data)
    fitness = evaluate_fitnesses(data.job_total_area, max_opened_batch_no, data.BIN_AREA)
    print("fitness : 剩餘空間為 {} , 共使用 {} 個bin".format(fitness[0], fitness[1]))


    ## draw rectangle
    #im = Image.new('RGB', (data.WBIN, data.HBIN), (128, 128, 128))
    #draw = ImageDraw.Draw(im)
    #for job_sol in solution:
    #    if job_sol[1] == 0:
    #        print("draw job {}".format(job_sol[0]))
    #        draw.rectangle((job_sol[3], data.HBIN - job_sol[4], job_sol[5], data.HBIN - job_sol[6]), fill=(0, 192, 192), outline=(255, 255, 255))
    #im.show()
    #im.save('pillow_imagedraw.jpg', quality=95)
    print()

    # METHOD 2 : BRKGA

    # End Program
    print("Spent {} second(s)".format(time.time() - START))