from locust import HttpUser, task, between
import requests

requests.packages.urllib3.disable_warnings()

class RedfishUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://localhost:8000"

    @task
    def get_system_info(self):
        self.client.get(
            "/redfish/v1/Systems/system",
            auth=("admin", "password"),
            name="Redfish /Systems/system"
        )

class PublicAPIUser(HttpUser):
    wait_time = between(0.5, 2)
    host = "https://jsonplaceholder.typicode.com"

    @task
    def get_posts(self):
        self.client.get("/posts", name="JSONPlaceholder /posts")
