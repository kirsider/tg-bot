import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient['mydatabase']

users = mydb['users']


def insert_record(user_id, username, config, dictionary, stats, statlist):
    record = {'user_id': user_id,
              'username': username,
              "config": config,
              'dictionary': dictionary,
              'statistic': stats,
              'statlist': statlist
              }
    users.insert_one(record)


def find_record(user_id):
    return users.find_one({"user_id": user_id})


def delete_record(user_id):
    users.delete_one({"user_id": user_id})
