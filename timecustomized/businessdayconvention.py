from enum import Enum


class BusinessDayConvention(Enum):
    Following = 1  # 节日之后的第一个工作日
    ModifiedFollowing = 2  # 节日之后的第一个工作日，若工作日属于另一个月，则返回节假日之前的第一个工作日
    Preceding = 3  # 节日之前非第一个工作日
    ModifiedPreceding = 4  # 节日之前的第一个工作日，若工作日属于另一个月，则返回节假日之后的第一个工作日
    Unadjusted = 5  # 不调整
    Nearest = 6  # 返回节日最近的工作日，如果前后两个日期距离相同，就按Following的规则处理
