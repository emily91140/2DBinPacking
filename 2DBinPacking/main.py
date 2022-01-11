import time

from src.DataProcess import DataProcess
from src.BinPack import *

def BFF_Heuristic(item_sequence):
    """
    Best First Fit(BFF) Bin Packing Heuristic
    逐一搜尋所有可放進的ems，並選擇放入剩餘邊長最小者: 旋轉過後 min(W-w, H-h)
    """
    pass

if __name__ == "__main__":
    # Time Calculate
    START = time.time()

    # DataProcess
    data = DataProcess(config_path="src/config.txt")
    print("ITEMS_dict: ", data.instanceDict['ITEMS'])
    item_sequence = largest_area_sort(data.instanceDict['ITEMS'])
    print("item sequence(by area large to small): ", item_sequence)
    print()

    # HEURISTIC METHOD
    ## Step1 Job Sequence (Largest Size)

    ## Step2 Apply BFF with ordered Job Sequence


    # BRKGA

    # End Program
    print("Spent {} second(s)".format(time.time() - START))