
def largest_area_sort(item_dict):
    '將item依照面積由大到小排序'
    
    # 計算各 item 面積
    area_list = []
    for key, item in item_dict.items():
        area_list.append(item.w*item.h)

    print("area_list: ", area_list)
    item_sequence = sorted(range(len(area_list)), key=lambda k: area_list[k], reverse=True) # 由大到小排列
    return item_sequence

class Item():
    def __init__(self, width = 0, height = 0):
        self.w = width
        self.h = height
        self.orientation = 0
        self.x1 = None # bottom left corner x
        self.y1 = None # bottom left corner y
    def __repr__(self):
        repr_str = ""
        repr_str += "["
        repr_str += str(self.w)
        repr_str += ","
        repr_str += str(self.h)
        repr_str += "]"
        return repr_str
    def is_accommodated(self, ems):
        'judge whether ems can contain item with returning the place result'
        pass

class EMS():
    def __init__(self):
        self.x1 = None # bottom left corner x
        self.y1 = None # bottom left corner y
        self.x2 = None # upper right corner x
        self.y2 = None # upper right corner y
    
    def generateNewEMS(insert_item, orientation, selected_EMS, exisiting_EMSs):
        pass