# locustfile.py
from locust import HttpUser, task, between


class APILoadTest(HttpUser):
    wait_time = between(1, 5)

    @task
    def moderate_text(self):
        self.client.post(
            "/moderate", json={"text": "Sample text for moderation."}
        )  # noqa

    def get_moderation_result(self):
        self.client.post("/result/2d19daba-653a-4137-8429-613268116b67")
