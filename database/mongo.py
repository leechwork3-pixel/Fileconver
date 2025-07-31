# /database/mongo.py
from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

class Database:
    def __init__(self, uri, db_name):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[db_name]
        self.users = self.db.users
        self.settings = self.db.settings

    # --- User Management ---
    async def add_user(self, user_id):
        if not await self.users.find_one({"_id": user_id}):
            await self.users.insert_one({"_id": user_id, "banned": False})
            return True
        return False

    async def get_all_user_ids(self):
        return [user["_id"] async for user in self.users.find({}, {"_id": 1})]

    async def ban_user(self, user_id):
        await self.users.update_one({"_id": user_id}, {"$set": {"banned": True}}, upsert=True)

    async def unban_user(self, user_id):
        await self.users.update_one({"_id": user_id}, {"$set": {"banned": False}}, upsert=True)

    async def is_user_banned(self, user_id):
        user = await self.users.find_one({"_id": user_id})
        return user.get("banned", False) if user else False

    # --- Settings Management ---
    async def get_setting(self, key):
        setting = await self.settings.find_one({"_id": key})
        return setting['value'] if setting else None

    async def set_setting(self, key, value):
        await self.settings.update_one({"_id": key}, {"$set": {"value": value}}, upsert=True)

db = Database(Config.DATABASE_URI, Config.DATABASE_NAME)
