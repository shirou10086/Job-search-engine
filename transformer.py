from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# 连接到 MongoDB 数据库
client = MongoClient('mongodb://localhost:27017/')
joblist={}

# 选择数据库

db = client['bigdata']

# 获取数据库中所有集合的名称
collections = db.list_collection_names()

total = 0
for collection_name in db.list_collection_names():
    collection = db[collection_name]
    cursor = collection.find()
    # Iterate through all documents in the collection
    for document in cursor:
        total += 1
print(total)

# 加载句向量模型
model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')
count = 0
for collection_name in db.list_collection_names():
    collection = db[collection_name]
    cursor = collection.find()

    # Iterate through all documents in the collection
    for document in cursor:
        count += 1
        if(count%100 == 0):
            print(count,"/",total)
        # Extract job description field
        job_description = document.get('job_description', None)
        if job_description is not None:
            job_vector = model.encode(job_description)
            joblist[job_description]= job_vector.tolist()
print("inseting...")
count = 0
#插入数据库
collection_vectors = db['job_vectors']
for key, value in joblist.items():
    count+=1
    if(count%500 == 0):
        print(key, value )
    collection_vectors.insert_one({'job_description': key, 'job_vector': value})

with open('data/jobs_data.json', 'r') as f:
    jobs_data = json.load(f)

job_descriptions = [job['description'] for job in jobs_data]
vectorizer = TfidfVectorizer(max_features=500)
job_description_features = vectorizer.fit_transform(job_descriptions).toarray()

from sklearn.feature_extraction.text import TfidfVectorizer

# 用户数据example:
'''users_data = [
    {"id": 1, "skills": "python, data analysis", "search_history": "machine learning, deep learning"},
    {"id": 2, "skills": "java, web development", "search_history": "spring boot, microservices"}
]'''

skills_data = [user["skills"] for user in users_data]
search_history_data = [user["search_history"] for user in users_data]

skills_vectorizer = TfidfVectorizer(max_features=50)
skills_features = skills_vectorizer.fit_transform(skills_data).toarray()

search_vectorizer = TfidfVectorizer(max_features=50)
search_features = search_vectorizer.fit_transform(search_history_data).toarray()

user_features = np.hstack([skills_features, search_features])

salaries = [job['salary'] for job in jobs_data]
locations = [job['location'] for job in jobs_data]

user_features = np.random.rand(100, 5)
job_features = np.random.rand(50, 7)

# 交互矩阵
interactions = np.random.randint(0, 2, (100, 50))  # 1表示申请

X = []
y = []

for i in range(100):
    for j in range(50):
        combined_features = np.concatenate([user_features[i], job_features[j]])
        X.append(combined_features)
        y.append(interactions[i][j])

X = np.array(X)
y = np.array(y)
