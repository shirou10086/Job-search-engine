import pymongo
import json
import os

def insert_json_to_mongodb(filename, collection):
    # 先把json换成字典
    with open(filename, 'r', encoding='utf-8') as f:
        data_dict = json.load(f)

    # 将data插入collection
    #collection.insert_one(data_dict)
    job_dict = {}
    for i in range(len(data_dict["data"])):
        job_dict = data_dict["data"][i]
        collection.insert_one(job_dict)

# 建立MongoDB连接

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["bigdata"]

# 定义集合名称列表
collections = ["cloud_developer", "data_scientist", "jobs_data", "product_manager", "researcher", "software_engineer", "technical_manager"]

# 遍历列表并插入到MongoDB
for collection_name in collections:
    collection = db[collection_name]
    filename = f"data/{collection_name}.json"
    insert_json_to_mongodb(filename, collection)
