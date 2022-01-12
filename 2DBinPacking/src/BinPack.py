
import copy

class Job():
    def __init__(self, no, width = 0, height = 0):
        self.no = no
        self.w = width
        self.h = height
        self.orientation = None
        self.x1 = None # bottom left corner x
        self.y1 = None # bottom left corner y
        self.x2 = None # upper right corner x
        self.y2 = None # upper right corner y
        self.batch_no = None # assigned to which batch_no

    def __repr__(self):
        repr_str = "[{}, {}]".format(self.w, self.h)
        return repr_str
    
    def is_accommodated(self, ems):
        """
        judge whether ems can contain job(object) with returning the place result'
        :param param1: ems(object) which want to put job in
        :type param1: BinPack.EMS object
        :return: result =  ['is_accommodated?', 'orientation', 'min_value' min(W-w, H-h), ems_id]
                            [True, 0, 5, 0] , [True, 1, 3, 1], [False, -1, -1, -1]
        :rtype: list
        """
        results = []
        # 分別檢視兩種方向(o)放不放得進ems
        for o in range(2):
            tmp_w, tmp_h = self.w, self.h
            if o == 1: #旋轉90度 寬高交換
                tmp_w, tmp_h = tmp_h, tmp_w
            
            if ems.W - tmp_w < 0 or ems.H - tmp_h < 0:
                results.append([False, -1, -1, -1])
            else:
                results.append([True, o, min(ems.W - tmp_w, ems.H - tmp_h), ems.id])
        
        # 篩選 選取最佳擺放方式與結果
        #print(results)
        true_results = [res for res in results if res[0] == True]
        #print("true_results: ", true_results)
        if len(true_results) == 0:
            return [False, -1, -1, -1]
        else:
            true_results = sorted(true_results, key = lambda s: s[2])
            #print("sorted true_results: ", true_results)
            return true_results[0]
    
    def putInChoosedEMSAndUpdateSolution(self, choosed_ems, final_placement, solution):
        """
        append new placement to solution
        :param param1: final_placement = ['is_accommodated?', 'orientation', 'min_value', ems_id]
        :type param1: list
        """
        # Record solution : [job_no, batch_no, orientation, x1, y1, x2, y2]
        orientation = final_placement[1]
        tmp_w, tmp_h = self.w, self.h
        if orientation == 1:
            tmp_w, tmp_h = tmp_h, tmp_w
        solution.append([self.no, choosed_ems.batch_no, orientation, choosed_ems.x1, choosed_ems.y1, choosed_ems.x1 + tmp_w, choosed_ems.y1 + tmp_h])

        # 更新 job self object
        self.orientation = orientation
        self.x1, self.y1 = choosed_ems.x1, choosed_ems.y1
        self.x2, self.y2 = choosed_ems.x1 + tmp_w, choosed_ems.y1 + tmp_h
        self.batch_no = choosed_ems.batch_no
        print("更新 job_id : {} 物件資訊 ---> 放置於 batch_no : {} 擺放座標為 ({}, {}), ({}, {})".format(self.no, self.batch_no, self.x1, self.y1, self.x2, self.y2))
        return solution, self

class EMS():
    
    # initialise class variable
    counter = 0

    def __init__(self, x1, y1, x2, y2, batch_no):
        self.x1 = x1 # bottom left corner x
        self.y1 = y1 # bottom left corner y
        self.x2 = x2 # upper right corner x
        self.y2 = y2 # upper right corner y
        self.W = x2 - x1 # Width
        self.H = y2 - y1 # Height
        self.area = self.W*self.H # Area
        self.batch_no = batch_no # related to batch_no
        self.id = EMS.counter

        # incrementing the class variable by 1
        # whenever new object is created
        EMS.counter += 1
    def __repr__(self):
        repr_str = "[({}, {}), ({}, {})]".format(self.x1, self.y1, self.x2, self.y2)
        return repr_str

def getEMSById(B_EMSs, search_ems_id):
    for b_no, EMSs in B_EMSs.items():
        for ems in EMSs:
            if ems.id == search_ems_id:
                return ems

def deleteEMSById(EMSs, delete_ems_id):
    'EMSs : EMSs list in certain batch'
    for ems in EMSs:
        if ems.id == delete_ems_id:
            result_EMSs = [e for e in EMSs if e.id != delete_ems_id]
            return result_EMSs


def largest_area_sort(job_dict):
    '將job依照面積由大到小排序'
    
    # 計算各 job 面積
    area_list = []
    for key, item in job_dict.items():
        area_list.append(item.w*item.h)

    #print("area_list: ", area_list)
    job_sequence = sorted(range(len(area_list)), key=lambda k: area_list[k], reverse=True) # 由大到小排列
    return job_sequence

def generateNewEMS(job, target_ems):
    """
    與重疊的ems進行切割
    return new_EMSs list
    """
    # target_ems 
    x1, y1 = target_ems.x1, target_ems.y1
    x2, y2 = target_ems.x2, target_ems.y2
    # job
    x3, y3 = job.x1, job.y1
    x4, y4 = job.x2, job.y2

    # generate new_EMSs
    batch_no = target_ems.batch_no
    new_EMSs = [
        EMS(x1, y1, x3, y2, batch_no),
        EMS(x4, y1, x2, y2, batch_no),
        EMS(x1, y1, x2, y3, batch_no),
        EMS(x1, y4, x2, y2, batch_no)
        ]
    return new_EMSs

def is_overlap(job, ems):
    """
    判斷 job 與 ems 是否有重疊
    """
    dx = min(job.x2, ems.x2) - max(job.x1, ems.x1)
    dy = min(job.y2, ems.y2) - max(job.y1, ems.y1)
    if dx > 0 and dy > 0:
        return True
    return False

def is_inscribed(new_ems, another_ems):
    if new_ems.x1 >= another_ems.x1 and new_ems.y1 >= another_ems.y1 and new_ems.x2 <= another_ems.x2 and new_ems.y2 <= another_ems.y2:
        return True
    return False

def is_selfelimination(new_ems):
    if (new_ems.x1 == new_ems.x2) or (new_ems.y1 == new_ems.y2):
        return True
    return False

def sortEMSsByArea(EMSs):
    new_EMSs = sorted(EMSs, key=lambda x: x.area, reverse=True)
    return new_EMSs

def updateEMSs(job, batch_no, exisiting_ems):
    """
    return an updated B_EMSs

    solution_item = [job_no, batch_no, orientation, x1, y1, x2, y2]
    """
    
    EMSs = exisiting_ems[batch_no].copy()
    result_EMSs = EMSs.copy()

    for ems in EMSs.copy():
        
        # 檢查現存ems是否跟job疊到
        if is_overlap(job, ems):
            # 刪除此ems 更新exisiting_ems
            result_EMSs = deleteEMSById(result_EMSs, ems.id)
        
            # 新增4個新的ems
            new_EMSs = generateNewEMS(job, ems)

            # 檢查新的ems 是否合理 是則加入result_EMSs
            for new_ems in new_EMSs:
                isValid = True
                # 是否被其他ems詮釋
                for other_ems in result_EMSs:
                    if is_inscribed(new_ems, other_ems):
                        isValid = False
                # 是否為一條線
                if is_selfelimination(new_ems):
                    isValid = False

                # 加入result_EMSs
                if isValid:
                    result_EMSs.append(new_ems)
    
    # 依照ems大小排序過後 更新B_EMSs資料結構
    result_EMSs = sortEMSsByArea(result_EMSs)
    exisiting_ems[batch_no] = result_EMSs.copy()
    return exisiting_ems

def BFF_Heuristic(jobNo_sequence, data):
    """
    Best First Fit(BFF) Bin Packing Heuristic
    逐一搜尋所有可放進的ems，並選擇放入剩餘邊長最小者: 旋轉過後 min(W-w, H-h)
    """
    print("=== 開始BFF擺放 ===")
    # Initialize
    jobNo_sequence_list = jobNo_sequence.copy()
    B_EMSs = {}     # open batches records remain EMSs by list {batch_no : [ems1, ems2, ...]}
    solution = []   # solution : [job_no, batch_no, orientation, x1, y1, x2, y2]
    jobResults = {} # { job_no : job object}
    ## 初始化第一包的ems
    batch_no = 0
    WBIN, HBIN = data.instanceDict["HBIN,WBIN"][1], data.instanceDict["HBIN,WBIN"][0]
    B_EMSs[batch_no] = [EMS(0, 0, WBIN, HBIN, batch_no)]

    # 遍歷處理所有jobs
    for job_no in jobNo_sequence_list:

        # get job object (copy)
        job = copy.deepcopy(data.instanceDict['JOBS'][job_no])

        # find best ems can contain this job (only store for this job)
        BatchNo_results = {}

        for b_no, EMSs in B_EMSs.items():
            results = [] # 儲存當下batch的所有結果
            for ems in EMSs:
                res = job.is_accommodated(ems)
                results.append(res) # 記錄當下batch之每個ems的擺放結果
            
            BatchNo_results[b_no] = results.copy()
            results.clear()
        
        # check whether can put job in exisiting Bin(Batch)
        # if not, create a new bin
        final_placement = []
        true_result = []
        for b_no, results in BatchNo_results.items():
            for res in results:
                if res[0]:
                    true_result.append(res)
        #true_result = [res for res in results for b_no, results in BatchNo_results.items() if res[0] == True]
        if len(true_result) != 0:
            # 若有多個可放置的ems 選擇 min_value最小者
            true_result = sorted(true_result, key = lambda s: s[2])
            final_placement = true_result[0] # [True, 0, 15, ems_object_id]

        else:
            # create new bin and place in it
            batch_no +=1
            B_EMSs[batch_no] = [EMS(0, 0, WBIN, HBIN, batch_no)]
            res = job.is_accommodated(B_EMSs[batch_no][0])
            final_placement = res # [True, 0, 15, ems_object_id]


        # Get choosed ems
        choosed_ems_id = final_placement[3]
        choosed_ems = getEMSById(B_EMSs, choosed_ems_id)

        # Place job into choosed ems and Update solution
        solution, job = job.putInChoosedEMSAndUpdateSolution(choosed_ems, final_placement, solution)
        jobResults[job_no] = job

        # Update(Merge) EMSs in choosed batch(bin)
        B_EMSs = updateEMSs(job, choosed_ems.batch_no, B_EMSs)
    print("=== 擺放演算完成 ===")
    return solution, B_EMSs, jobResults, batch_no

def evaluate_fitnesses(job_total_area, max_opened_batch_no, bin_area):
    'return a list = [ residual_area, max_opened_batch_no]'
    num_used_bin = max_opened_batch_no + 1
    return [(num_used_bin*bin_area) - job_total_area, num_used_bin]