from locust import HttpUser, task, between


class MyUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        # login to get token
        login_payload = {"username": "soeun", "password": "1234"}
        response = self.client.post("/auth/login", json=login_payload)

        self.token = response.json()["access_token"]

    @task
    def common_question_request(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        self.client.get("/common_question", headers=headers)

    @task
    def personal_question_request(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        self.client.get("/personal_question", headers=headers)
