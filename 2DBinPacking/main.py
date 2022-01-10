import time

from src.DataProcess import DataProcess

if __name__ == "__main__":
    # Time Calculate
    START = time.time()

    # DataProcess
    data = DataProcess(config_path="src/config.txt")

    # End Program
    DURATION = time.time() - START
    print("Spent {} second(s)".format(DURATION))