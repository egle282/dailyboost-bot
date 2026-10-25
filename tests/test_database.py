import unittest
import os
import time
import database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        database.DB_PATH = "test_users.db"
        if os.path.exists(database.DB_PATH):
            os.remove(database.DB_PATH)
        database.init_db()

    def tearDown(self):
        if os.path.exists(database.DB_PATH):
            os.remove(database.DB_PATH)

    def test_create_and_get_user(self):
        database.create_user(12345, "Alex", "ru")
        user = database.get_user(12345)
        self.assertIsNotNone(user)
        self.assertEqual(user["name"], "Alex")
        self.assertEqual(user["language"], "ru")
        self.assertEqual(user["premium_until"], 0)

    def test_update_user(self):
        database.create_user(12345, "Alex", "ru")
        now_ts = int(time.time()) + 3600
        database.update_user(12345, premium_until=now_ts, language="en")
        
        user = database.get_user(12345)
        self.assertEqual(user["premium_until"], now_ts)
        self.assertEqual(user["language"], "en")

    def test_get_all_users(self):
        database.create_user(1, "User1", "ru")
        database.create_user(2, "User2", "en")
        users = database.get_all_users()
        self.assertEqual(len(users), 2)

if __name__ == "__main__":
    unittest.main()
