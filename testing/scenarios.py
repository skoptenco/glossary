import random
import time

def browsing_scenario(user):
    user.client.get("/terms")
    time.sleep(random.uniform(0.5, 1.5))
    term_id = random.randint(1, 100)
    user.client.get(f"/terms/test")

def editing_scenario(user):
    payload = {
        "keyword": f"term_{random.randint(1, 100000)}",
        "description": "definition"
    }
    user.client.post("/terms", json=payload)

def grpc_browsing(user):
    user.stub.ListTerms()
    time.sleep(random.uniform(0.3, 1.2))
    user.stub.GetTerm('test')

def grpc_editing(user, term):
    user.stub.CreateTerm(term)