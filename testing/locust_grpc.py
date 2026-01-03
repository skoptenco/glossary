from locust import User, task, between, events
import grpc
from time import time
import glossary_pb2, glossary_pb2_grpc
from scenarios import *
from utils import *

class GrpcGlossaryUser(User):
    wait_time = between(1, 3)

    def on_start(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = glossary_pb2_grpc.GlossaryStub(self.channel)
        self.known_terms = []

    def track(self, name, func):
        start = time.time()
        try:
            result = func()
            events.request.fire(
                request_type="gRPC",
                name=name,
                response_time=(time.time() - start) * 1000,
                response_length=0,
                exception=None
            )
            return result
        except Exception as e:
            events.request.fire(
                request_type="gRPC",
                name=name,
                response_time=(time.time() - start) * 1000,
                exception=e
            )

    @task(1)
    def list_terms(self):
        response = self.track(
            "ListTerms",
            lambda: self.stub.ListTerms(glossary_pb2.ListTermsRequest())
        )
        if response and response.terms:
            self.known_terms = [t.keyword for t in response.terms]

    @task(2)
    def create_term(self):
        keyword = random_word()
        response = self.track(
            "CreateTerm",
            lambda: self.stub.CreateTerm(
                glossary_pb2.CreateTermRequest(
                    keyword=keyword,
                    description="Load testing term"
                )
            )
        )
        if response.created:
            self.known_terms.append(keyword)

    @task(3)
    def get_term(self):
        if not self.known_terms:
            return
        keyword = random.choice(self.known_terms)
        self.track(
            "GetTerm",
            lambda: self.stub.GetTerm(glossary_pb2.GetTermRequest(keyword=keyword))
        )

    @task(4)
    def delete_term(self):
        if not self.known_terms:
            return
        keyword = random.choice(self.known_terms)
        self.track(
            "DeleteTerm",
            lambda: self.stub.DeleteTerm(glossary_pb2.DeleteTermRequest(keyword=keyword))
        )
