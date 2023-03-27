import pymongo

# client = pymongo.MongoClient("mongodb://localhost:27017")
client = pymongo.MongoClient("mongodb+srv://root:root@cluster0.rhwqd.mongodb.net/?retryWrites=true&w=majority",connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True, connect=False, maxPoolsize=1)

db = client.LoginDatabase
# db=client["LoginDatabase"]
userDetails = db.userCollection
# userDetails=db["userCollection"]
# userDetails.insert_one({"name":"gokul"})
