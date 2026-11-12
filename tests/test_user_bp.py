import unittest
from app import app


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_greetings_page(self):
        response = self.client.get("/users/hi/John?age=30")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"JOHN", response.data)
        self.assertIn(b"30", response.data)

    def test_admin_page(self):
        response = self.client.get("/users/admin", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ADMINISTRATOR", response.data)
        self.assertIn(b"45", response.data)

    def test_profile_requires_login(self):
        response = self.client.get("/users/profile")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/users/login", response.location)

    def test_login_and_logout(self):
        response = self.client.post(
            "/users/login",
            data={"username": "user1", "password": "12345"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"user1", response.data)

        self.client.post("/users/logout")
        profile_response = self.client.get("/users/profile")
        self.assertEqual(profile_response.status_code, 302)

    def test_cookies_add_and_delete(self):
        self.client.post("/users/login", data={"username": "user1", "password": "12345"})
        add_response = self.client.post(
            "/users/add_cookie",
            data={"cookie_key": "test_key", "cookie_value": "test_val"},
            follow_redirects=True,
        )
        self.assertEqual(add_response.status_code, 200)
        self.assertIn(b"test_val", add_response.data)

        delete_response = self.client.post(
            "/users/delete_cookie",
            data={"delete_key": "test_key"},
            follow_redirects=True,
        )
        self.assertEqual(delete_response.status_code, 200)
        self.assertNotIn(b"test_val", delete_response.data)

    def test_color_scheme_switch(self):
        self.client.post("/users/login", data={"username": "user1", "password": "12345"})
        response = self.client.get("/users/set_color/dark", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"profile-dark", response.data)


if __name__ == "__main__":
    unittest.main()
