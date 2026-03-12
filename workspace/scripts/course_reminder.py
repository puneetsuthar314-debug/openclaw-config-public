#!/root/anaconda3/bin/python3
"""
课程提醒脚本 - 根据课表返回当天课程信息
"""
import json
from datetime import datetime, timedelta

# 用户课表数据（从小和山校区 PDF 提取）
COURSE_TABLE = {
    0: {  # 周一
        "morning": [
            {"name": "工程师英语 2★", "time": "8:00-9:35", "location": "A2-310", "teacher": "石教旺", "weeks": "1-16", "period": "1-2"}
        ],
        "afternoon": [
            {"name": "前端高级程序设计★", "time": "13:30-15:05", "location": "A1-110", "teacher": "彭燕妮", "weeks": "1-16", "period": "6-8"}
        ],
        "evening": [
            {"name": "宠物心理与营养健康★", "time": "18:30-20:05", "location": "A2-226", "teacher": "白凯文", "weeks": "1-11", "period": "10-11"}
        ]
    },
    1: {  # 周二
        "morning": [
            {"name": "数据库系统设计基础★", "time": "9:50-11:25", "location": "c1-A106", "teacher": "林焕祥", "weeks": "9-16", "period": "3-4"}
        ],
        "afternoon": [
            {"name": "形势与政策 4★", "time": "13:30-15:05", "location": "A2-301", "teacher": "郭鑫", "weeks": "13-16", "period": "6-7"}
        ],
        "evening": [
            {"name": "酒类鉴赏★", "time": "18:30-19:15", "location": "A2-222", "teacher": "侯洁，王伟，吴轶", "weeks": "1-16", "period": "10-11"}
        ]
    },
    2: {  # 周三
        "morning": [
            {"name": "计算数学★", "time": "9:50-11:25", "location": "A1-310", "teacher": "柳杨，郭翔", "weeks": "1-16", "period": "3-5"}
        ],
        "afternoon": [
            {"name": "数字图像处理★", "time": "13:30-15:05", "location": "A2-210", "teacher": "宋蔚", "weeks": "1-16", "period": "6-8"}
        ],
        "evening": []
    },
    3: {  # 周四
        "morning": [
            {"name": "习近平新时代中国特色社会主义思想概论★", "time": "9:50-11:25", "location": "A2-102", "teacher": "刘凤玲", "weeks": "1-16", "period": "3-5"}
        ],
        "afternoon": [
            {"name": "体育 4★", "time": "13:30-15:05", "location": "YD221 篮球场", "teacher": "常德胜", "weeks": "1-16", "period": "6-7"}
        ],
        "evening": [
            {"name": "快乐学习《易经》★", "time": "18:30-19:15", "location": "A2-302", "teacher": "罗惠龄", "weeks": "1-16", "period": "8-9"}
        ]
    },
    4: {  # 周五
        "morning": [
            {"name": "专业高级技术拓展 1★", "time": "9:50-11:25", "location": "A1-310", "teacher": "宗畅", "weeks": "1-16", "period": "3-5"}
        ],
        "afternoon": [],
        "evening": []
    },
    5: {  # 周六
        "morning": [],
        "afternoon": [],
        "evening": []
    },
    6: {  # 周日
        "morning": [],
        "afternoon": [],
        "evening": []
    }
}

# 学期开始日期（2026 年 3 月 2 日）
SEMESTER_START = datetime(2026, 3, 2)

def get_current_week():
    """计算当前是第几周"""
    today = datetime.now()
    if today < SEMESTER_START:
        return 0
    days_since_start = (today - SEMESTER_START).days
    week = (days_since_start // 7) + 1
    return min(week, 16)  # 最多 16 周

def get_course_progress(weeks_str, current_week):
    """计算课程进度百分比"""
    if "-" in weeks_str:
        start, end = map(int, weeks_str.split("-"))
        if current_week < start:
            return 0
        if current_week > end:
            return 100
        total = end - start + 1
        current = current_week - start + 1
        return int((current / total) * 100)
    return 0

def get_courses(period):
    """
    获取指定时间段的课程
    period: morning, afternoon, evening
    """
    today = datetime.now()
    weekday = today.weekday()  # 0=周一，6=周日
    current_week = get_current_week()
    
    courses = COURSE_TABLE.get(weekday, {}).get(period, [])
    
    result = []
    for course in courses:
        # 检查是否在上课周范围内
        weeks = course.get("weeks", "1-16")
        if "-" in weeks:
            start, end = map(int, weeks.split("-"))
            if current_week < start or current_week > end:
                continue
        
        progress = get_course_progress(course.get("weeks", "1-16"), current_week)
        
        result.append({
            "name": course["name"],
            "time": course["time"],
            "location": course["location"],
            "teacher": course["teacher"],
            "progress": progress,
            "week": current_week
        })
    
    return result

if __name__ == "__main__":
    import sys
    period = sys.argv[1] if len(sys.argv) > 1 else "morning"
    courses = get_courses(period)
    print(json.dumps(courses, ensure_ascii=False))
