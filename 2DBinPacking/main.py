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
    # solution : [job_no, batch_no, orientation, x1, y1, x2, y2]
    solution, B_EMSs, data = BFF_Heuristic(job_sequence, data)
    print()

    # draw rectangle
    im = Image.new('RGB', (200, 400), (128, 128, 128))
    draw = ImageDraw.Draw(im)
    for job_sol in solution:
        if job_sol[1] == 0:
            print("draw job {}".format(job_sol[0]))
            draw.rectangle((job_sol[3], 400-job_sol[4], job_sol[5], 400-job_sol[6]), fill=(0, 192, 192), outline=(255, 255, 255))
    im.show()
    im.save('pillow_imagedraw.jpg', quality=95)
    
    # METHOD 2 : BRKGA

    # End Program
    print("Spent {} second(s)".format(time.time() - START))