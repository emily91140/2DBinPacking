

from src.BinPack import *

class DataProcess():
    def __init__(self, config_path):
        self.config = self.LoadConfig(config_path)
        self.instanceDict = self.LoadInstance(self.config['instance_filename'])



    def LoadConfig(self, path):
        '讀取config檔案'
        myDict = {} 
        with open(path, "r") as f:
            for line in f:
                # 若此行開頭為 "#" 或 換行符號 則跳過此行不處理
                if line[0] in ["#", "\n"]:
                    continue
                
                line = line.replace("\n", "")
                item = line.split('=')
                if len(item)==2:
                    key = item[0].strip()
                    value = item[1].strip()
                    myDict[key] = eval(value)
        return myDict

    def LoadInstance(self, instance_filename):
        titleDict = {1:"PROBLEM CLASS", 2:"number of items(N)", 3:"RELATIVE AND ABSOLUTE NO. OF INSTANCE", 4:"HBIN,WBIN"}
        instanceDict = {}
        item_dict = {} # {item_no: [h_i, w_i]}, i = 1...N
        dir = 'instances/'
        with open(dir + instance_filename, "r") as f:
            line_no = 1 # 讀取列編號
            item_no = 0 # item 編號
            for line in f:
                item = line.split()
                tmp = [int(s) for s in item if s.isnumeric()]
                if line_no <= 4:
                    # 開頭4列
                    instanceDict[titleDict[line_no]] = tmp
                else:
                    # job 列表 存入item物件
                    item = Item(tmp[0], tmp[1])
                    item_dict[item_no] = item
                    item_no += 1
                
                # 更新line_no
                line_no += 1
            # 最後將item_dict 存入instanceDict
            instanceDict['ITEMS'] = item_dict

            return instanceDict