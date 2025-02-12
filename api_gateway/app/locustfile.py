from locust import HttpUser, task, between


class APILoadTest(HttpUser):
    wait_time = between(1, 5)

    @task
    def moderate_text(self):
        self.client.post(
            "/api/moderate", json={"text": "Sample text for moderation."}
        )  # noqa

    @task
    def get_moderation_result(self):
        self.client.get(
            "/api/moderation/result/8270137805bd42b18dd35349c826ca2a"
        )  # noqa
