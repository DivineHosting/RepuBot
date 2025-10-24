from pymongo import MongoClient
from datetime import datetime

def connect_to_mongo():
    from config import MONGO_URI
    client = MongoClient(MONGO_URI)
    return client

# Database functions
def add_vouch(db, guild_id, vouched_by, vouched_for, reason):
    vouch = {
        "guild_id": guild_id,
        "vouched_by": vouched_by,
        "vouched_for": vouched_for,
        "reason": reason,
        "status": "pending",
        "timestamp": datetime.utcnow()
    }
    result = db.vouches.insert_one(vouch)
    return result.inserted_id

def update_vouch_status(db, vouch_id, status):
    from bson import ObjectId
    db.vouches.update_one({"_id": ObjectId(vouch_id)}, {"$set": {"status": status}})

def get_vouch_by_id(db, vouch_id):
    from bson import ObjectId
    return db.vouches.find_one({"_id": ObjectId(vouch_id)})

def get_user_vouches(db, user_id, guild_id, status="approved"):
    return list(db.vouches.find({"vouched_for": str(user_id), "guild_id": guild_id, "status": status}))

def get_top_users(db, guild_id, limit=10):
    pipeline = [
        {"$match": {"guild_id": guild_id, "status": "approved"}},
        {"$group": {"_id": "$vouched_for", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]
    return list(db.vouches.aggregate(pipeline))

def set_log_channel(db, guild_id, channel_id):
    db.settings.update_one({"guild_id": guild_id}, {"$set": {"log_channel": channel_id}}, upsert=True)

def get_log_channel(db, guild_id):
    settings = db.settings.find_one({"guild_id": guild_id})
    return settings["log_channel"] if settings and "log_channel" in settings else None
