from locust import HttpUser, task, between
from utils import *


class FastApiUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.terms = [];

    @task(1)
    def list_terms(self):
        response = self.client.get("/terms")
        if response and response.status_code == 200:
            terms = response.json()
            self.terms = [item["keyword"] for item in terms]
        else:
            self.terms = []

    @task(2)
    def create_term(self):
        keyword = random_word()
        term = {
            "keyword": keyword,
            "description": "Load testing term",
        }
        response = self.client.post("/terms", json=term)
        if response and response.json():
            self.terms.append(keyword)

    @task(3)
    def get_term(self):
        if not self.terms:
            return
        keyword = random.choice(self.terms)
        self.client.get(f"/terms/{keyword}")

    @task(4)
    def delete_term(self):
        if not self.terms:
            return
        keyword = random.choice(self.terms)
        self.client.delete(f"/terms/{keyword}")
        self.terms.remove(keyword)

