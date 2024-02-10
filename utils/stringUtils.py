from typing import List


def stringArrayToStr(list:List[str]):
    res=""
    for i,s in enumerate(list):
        res+=s
        if((i+1)<len(list)):res+=","
    return res