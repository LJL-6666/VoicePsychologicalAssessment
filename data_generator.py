# -*- coding: utf-8 -*-
"""
心理评估报告数据生成器
创建与测试文件完全一致的模拟数据
"""

import os
import json

def create_mock_data():
    """创建模拟数据文件 - 使用与测试文件完全相同的数据格式"""
    
    # 存储模拟数据的目录
    DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api_data')
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # 10001的数据 - 与测试文件完全一致
    data_10001 = {
        "code": 0,
        "data": {
            "groupName": "问卷测评",
            "organizationName": "员工心理健康项目",
            "createTime": "2025-05-15",
            "dataList": [
                {
                    "cognitiveAbility": "",
                    "cognitiveAbilityName": "",
                    "createTime": "",
                    "description": "",
                    "emptyLevel": 0,
                    "facterDisplay": "1",
                    "facterId": 123,
                    "facterName": "健康状况问卷（PHQ-9）>总分",
                    "factorCoefficientLevelNorm": "0-4",
                    "factorCoefficientScore": 4,
                    "feedback": "测评结果表明，没有明显的抑郁倾向.得分范围0-27分，得分越高抑郁倾向越明显。",
                    "groupId": 0,
                    "level": "健康",
                    "levelCode": "2",
                    "levelNorm": "0.0-4.0",
                    "max": 4,
                    "maxScore": "",
                    "min": 0,
                    "name": "",
                    "parentId": "",
                    "questionnaireId": 33,
                    "questionnaireName": "健康状况问卷（PHQ-9）",
                    "recommend": "",
                    "score": 4,
                    "scoreStr": "4.0",
                    "sort": 20,
                    "standardScore": "",
                    "standardScoreStr": ""
                },
                {
                    "cognitiveAbility": "",
                    "cognitiveAbilityName": "",
                    "createTime": "",
                    "description": "",
                    "emptyLevel": 0,
                    "facterDisplay": "1",
                    "facterId": 389,
                    "facterName": "广泛性焦虑量表（GAD-7）>总分",
                    "factorCoefficientLevelNorm": "0-4",
                    "factorCoefficientScore": 0,
                    "feedback": "测评结果表明，没有明显的焦虑倾向。得分范围0-21分，得分越高焦虑越严重。",
                    "groupId": 0,
                    "level": "健康",
                    "levelCode": "2",
                    "levelNorm": "0.0-4.0",
                    "max": 4,
                    "maxScore": "",
                    "min": 0,
                    "name": "",
                    "parentId": "",
                    "questionnaireId": 129,
                    "questionnaireName": "广泛性焦虑量表（GAD-7）",
                    "recommend": "",
                    "score": 0,
                    "scoreStr": "0.0",
                    "sort": 21,
                    "standardScore": "",
                    "standardScoreStr": ""
                },
                {
                    "cognitiveAbility": "",
                    "cognitiveAbilityName": "",
                    "createTime": "",
                    "description": "",
                    "emptyLevel": 0,
                    "facterDisplay": "1",
                    "facterId": 1371,
                    "facterName": "压力知觉量表（CPSS）>总分",
                    "factorCoefficientLevelNorm": "0-57",
                    "factorCoefficientScore": 21,
                    "feedback": "得分范围在0-56分之间，得分越高，表示觉知的压力感越强。",
                    "groupId": 0,
                    "level": "无等级",
                    "levelCode": "51",
                    "levelNorm": "0.0-57.0",
                    "max": "",
                    "maxScore": "",
                    "min": "",
                    "name": "",
                    "parentId": "",
                    "questionnaireId": 354,
                    "questionnaireName": "压力知觉量表（CPSS）",
                    "recommend": "",
                    "score": 21,
                    "scoreStr": "21.0",
                    "sort": 16,
                    "standardScore": "",
                    "standardScoreStr": ""
                },
                {
                    "cognitiveAbility": "",
                    "cognitiveAbilityName": "",
                    "createTime": "",
                    "description": "",
                    "emptyLevel": 0,
                    "facterDisplay": "1",
                    "facterId": 3983,
                    "facterName": "一般健康问卷（GHQ-12）>总分",
                    "factorCoefficientLevelNorm": "0-3",
                    "factorCoefficientScore": 4,
                    "feedback": "可能存在心理健康状况问题，请进一步评估。",
                    "groupId": 0,
                    "level": "异常",
                    "levelCode": "3",
                    "levelNorm": "0.0-3.0",
                    "max": 3,
                    "maxScore": "",
                    "min": 0,
                    "name": "",
                    "parentId": "",
                    "questionnaireId": 960,
                    "questionnaireName": "一般健康问卷（GHQ-12）",
                    "recommend": "",
                    "score": 4,
                    "scoreStr": "4.0",
                    "sort": 19,
                    "standardScore": "",
                    "standardScoreStr": ""
                }
            ],
            "logo": "",
            "aiReport": 1,
            "personInfo": {
                "性别": "男",
                "年龄": "34岁",
                "出生日期": "1990-01-01",
                "工种": "普通职工",
                "行业": "科研",
                "测试开始时间": "2024-01-01 10:00:00",
                "测试结束时间": "2024-01-01 10:25:00",
                "持续时长": "00:25:07"
            },
            "fileList": [
                {
                    "title": "预热题-天气",
                    "file_address": "http://example.invalid/data/files/audio/100001/20240101100000_13800000000_语音题目 天气_10001.wav"
                },
                {
                    "title": "工种题-多次完成相同操作",
                    "file_address": "http://example.invalid/data/files/audio/100001/20240101100800_13800000000_多次完成相同操作_10001.wav"
                },
                {
                    "title": "职场感知-工作充实的完整工作日",
                    "file_address": "http://example.invalid/data/files/audio/100001/20240101100600_13800000000_工作充实的完整工作日_10001.wav"
                },
                {
                    "title": "个性画像-最近一次自豪",
                    "file_address": "http://example.invalid/data/files/audio/100001/20240101100200_13800000000_最近一次自豪_10001.wav"
                },
                {
                    "title": "支持系统-家人生病",
                    "file_address": "http://example.invalid/data/files/audio/100001/20240101100400_13800000000_家人生病_10001.wav"
                }
            ],
            "recordId": 10001
        },
        "message": "ok"
    }
    
    # 10002的数据 - 与测试文件完全一致
    data_10002 = {
        "code": 0,
        "data": {
            "groupName": "问卷测评",
            "organizationName": "员工心理健康项目",
            "createTime": "2025-05-15",
            "dataList": [
                {
                    "cognitiveAbility": "",
                    "cognitiveAbilityName": "",
                    "createTime": "",
                    "description": "",
                    "emptyLevel": 0,
                    "facterDisplay": "1",
                    "facterId": 123,
                    "facterName": "健康状况问卷（PHQ-9）>总分",
                    "factorCoefficientLevelNorm": "0-4",
                    "factorCoefficientScore": 4,
                    "feedback": "测评结果表明，没有明显的抑郁倾向.得分范围0-27分，得分越高抑郁倾向越明显。",
                    "groupId": 0,
                    "level": "健康",
                    "levelCode": "2",
                    "levelNorm": "0.0-4.0",
                    "max": 4,
                    "maxScore": "",
                    "min": 0,
                    "name": "",
                    "parentId": "",
                    "questionnaireId": 33,
                    "questionnaireName": "健康状况问卷（PHQ-9）",
                    "recommend": "",
                    "score": 4,
                    "scoreStr": "4.0",
                    "sort": 20,
                    "standardScore": "",
                    "standardScoreStr": ""
                },
                {
                    "cognitiveAbility": "",
                    "cognitiveAbilityName": "",
                    "createTime": "",
                    "description": "",
                    "emptyLevel": 0,
                    "facterDisplay": "1",
                    "facterId": 389,
                    "facterName": "广泛性焦虑量表（GAD-7）>总分",
                    "factorCoefficientLevelNorm": "0-4",
                    "factorCoefficientScore": 0,
                    "feedback": "测评结果表明，没有明显的焦虑倾向。得分范围0-21分，得分越高焦虑越严重。",
                    "groupId": 0,
                    "level": "健康",
                    "levelCode": "2",
                    "levelNorm": "0.0-4.0",
                    "max": 4,
                    "maxScore": "",
                    "min": 0,
                    "name": "",
                    "parentId": "",
                    "questionnaireId": 129,
                    "questionnaireName": "广泛性焦虑量表（GAD-7）",
                    "recommend": "",
                    "score": 0,
                    "scoreStr": "0.0",
                    "sort": 21,
                    "standardScore": "",
                    "standardScoreStr": ""
                },
                {
                    "cognitiveAbility": "",
                    "cognitiveAbilityName": "",
                    "createTime": "",
                    "description": "",
                    "emptyLevel": 0,
                    "facterDisplay": "1",
                    "facterId": 1371,
                    "facterName": "压力知觉量表（CPSS）>总分",
                    "factorCoefficientLevelNorm": "0-57",
                    "factorCoefficientScore": 21,
                    "feedback": "得分范围在0-56分之间，得分越高，表示觉知的压力感越强。",
                    "groupId": 0,
                    "level": "无等级",
                    "levelCode": "51",
                    "levelNorm": "0.0-57.0",
                    "max": "",
                    "maxScore": "",
                    "min": "",
                    "name": "",
                    "parentId": "",
                    "questionnaireId": 354,
                    "questionnaireName": "压力知觉量表（CPSS）",
                    "recommend": "",
                    "score": 21,
                    "scoreStr": "21.0",
                    "sort": 16,
                    "standardScore": "",
                    "standardScoreStr": ""
                },
                {
                    "cognitiveAbility": "",
                    "cognitiveAbilityName": "",
                    "createTime": "",
                    "description": "",
                    "emptyLevel": 0,
                    "facterDisplay": "1",
                    "facterId": 3983,
                    "facterName": "一般健康问卷（GHQ-12）>总分",
                    "factorCoefficientLevelNorm": "0-3",
                    "factorCoefficientScore": 4,
                    "feedback": "可能存在心理健康状况问题，请进一步评估。",
                    "groupId": 0,
                    "level": "异常",
                    "levelCode": "3",
                    "levelNorm": "0.0-3.0",
                    "max": 3,
                    "maxScore": "",
                    "min": 0,
                    "name": "",
                    "parentId": "",
                    "questionnaireId": 960,
                    "questionnaireName": "一般健康问卷（GHQ-12）",
                    "recommend": "",
                    "score": 4,
                    "scoreStr": "4.0",
                    "sort": 19,
                    "standardScore": "",
                    "standardScoreStr": ""
                }
            ],
            "logo": "",
            "aiReport": 1,
            "personInfo": {
                "性别": "男",
                "年龄": "34岁",
                "出生日期": "1990-01-01",
                "工种": "普通职工",
                "行业": "科研",
                "测试开始时间": "2024-01-01 10:00:00",
                "测试结束时间": "2024-01-01 10:25:00",
                "持续时长": "00:25:07"
            },
            "fileList": [
                {
                    "title": "预热题-天气",
                    "file_address": "http://example.invalid/data/files/audio/100002/20240102100000_13800000001_语音题目 天气_10002.wav"
                },
                {
                    "title": "工种题-多次完成相同操作",
                    "file_address": "http://example.invalid/data/files/audio/100002/20240102100200_13800000001_多次完成相同操作_10002.wav"
                },
                {
                    "title": "职场感知-工作充实的完整工作日",
                    "file_address": "http://example.invalid/data/files/audio/100002/20240102100400_13800000001_工作充实的完整工作日_10002.wav"
                },
                {
                    "title": "个性画像-最近一次自豪",
                    "file_address": "http://example.invalid/data/files/audio/100002/20240102100600_13800000001_最近一次自豪_10002.wav"
                },
                {
                    "title": "支持系统-家人生病",
                    "file_address": "http://example.invalid/data/files/audio/100002/20240102100800_13800000001_家人生病_10002.wav"
                }
            ],
            "recordId": 10002
        },
        "message": "ok"
    }
    
    # 保存模拟数据文件
    with open(os.path.join(DATA_DIR, '10001.txt'), 'w', encoding='utf-8') as f:
        json.dump(data_10001, f, ensure_ascii=False, indent=2)
    
    with open(os.path.join(DATA_DIR, '10002.txt'), 'w', encoding='utf-8') as f:
        json.dump(data_10002, f, ensure_ascii=False, indent=2)
    
    print("模拟数据文件已创建（与测试文件格式完全一致）")
    return DATA_DIR

if __name__ == "__main__":
    create_mock_data()