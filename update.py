import requests
import json
import pymongo


def update_mongodb(update_json, collection):

    jobs_count = collection.count_documents({})
    print("original jobs num:",jobs_count)
    # 将更新的json转成字典
    with open(update_json, 'r', encoding='utf-8') as f:
        update_dict = json.load(f)

    #提取出要更新的 data list
    update_jobs = {}
    print("update data num:", len(update_dict["data"]))
    for i in range(len(update_dict["data"])):
        update_jobs = update_dict["data"][i]
        query ={"job_id" : update_jobs["job_id"]}
        jobs = collection.find(query)
        count = 0
        for items in jobs:
            count += 1
        if(count != 0):
            continue
        #有内容说明吃查到了这个ID的job
        else:
            collection.insert_one({str(jobs_count):update_jobs})
            jobs_count += 1
    print("finaly updated job num:", collection.count_documents({}))

url = "https://jsearch.p.rapidapi.com/search"

querystring = {"query":"data_scientist","page":"1","num_pages":"20"}

headers = {
	"content-type": "application/octet-stream",
	"X-RapidAPI-Key": "394d899556msh4f0740173b447c1p1e6a45jsnfd1521c2520f",
	"X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

# Serializing json
json_object = json.dumps(response.json(), indent=4)
 
# Writing to .json
with open("data_scientist_update.json", "w") as outfile:
    outfile.write(json_object)

# 建立MongoDB连接

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["bigdata"]

collections = db.data_scientist
jobs_count = collections.count_documents({})
update_mongodb(f"data_scientist_update.json",collections)



