# server.py
from concurrent import futures
import grpc
import glossary_pb2
import glossary_pb2_grpc
from storage import Storage
from models import TermCreate, TermUpdate
from grpc_reflection.v1alpha import reflection
from datetime import datetime

class GlossaryServicer(glossary_pb2_grpc.GlossaryServicer):
    def __init__(self, storage: Storage):
        self.storage = storage

    def ListTerms(self, request, context):
        terms_db = self.storage.list_terms()
        resp = glossary_pb2.ListTermsResponse()
        for t in terms_db:
            resp.terms.add(
                keyword=t.keyword,
                description=t.description,
                created_at=t.created_at.isoformat() if t.created_at else "",
                updated_at=t.updated_at.isoformat() if t.updated_at else ""
            )
        return resp

    def GetTerm(self, request, context):
        keyword = (request.keyword or "").strip().lower()
        if not keyword:
            return glossary_pb2.GetTermResponse(found=False, error="keyword is required")
        t = self.storage.get_term(keyword)
        if not t:
            return glossary_pb2.GetTermResponse(found=False, error="not found")
        term_msg = glossary_pb2.Term(
            keyword=t.keyword,
            description=t.description,
            created_at=t.created_at.isoformat() if t.created_at else "",
            updated_at=t.updated_at.isoformat() if t.updated_at else ""
        )
        return glossary_pb2.GetTermResponse(found=True, term=term_msg)

    def CreateTerm(self, request, context):
        # validate with Pydantic
        try:
            data = TermCreate(keyword=request.keyword, description=request.description)
        except Exception as e:
            return glossary_pb2.CreateTermResponse(created=False, error=str(e))
        # check exists
        if self.storage.get_term(data.keyword):
            return glossary_pb2.CreateTermResponse(created=False, error="term already exists")
        created = self.storage.create_term(data.keyword, data.description)
        term_msg = glossary_pb2.Term(
            keyword=created.keyword,
            description=created.description,
            created_at=created.created_at.isoformat() if created.created_at else "",
            updated_at=created.updated_at.isoformat() if created.updated_at else ""
        )
        return glossary_pb2.CreateTermResponse(created=True, term=term_msg)

    def UpdateTerm(self, request, context):
        try:
            data = TermUpdate(keyword=request.keyword, description=request.description)
        except Exception as e:
            return glossary_pb2.UpdateTermResponse(updated=False, error=str(e))
        if not self.storage.get_term(data.keyword):
            return glossary_pb2.UpdateTermResponse(updated=False, error="term not found")
        updated = self.storage.update_term(data.keyword, data.description)
        if not updated:
            return glossary_pb2.UpdateTermResponse(updated=False, error="failed to update")
        term_msg = glossary_pb2.Term(
            keyword=updated.keyword,
            description=updated.description,
            created_at=updated.created_at.isoformat() if updated.created_at else "",
            updated_at=updated.updated_at.isoformat() if updated.updated_at else ""
        )
        return glossary_pb2.UpdateTermResponse(updated=True, term=term_msg)

    def DeleteTerm(self, request, context):
        keyword = (request.keyword or "").strip().lower()
        if not keyword:
            return glossary_pb2.DeleteTermResponse(deleted=False, error="keyword is required")
        deleted = self.storage.delete_term(keyword)
        if not deleted:
            return glossary_pb2.DeleteTermResponse(deleted=False, error="term not found")
        return glossary_pb2.DeleteTermResponse(deleted=True)

def serve(host='[::]', port=50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    storage = Storage()
    glossary_pb2_grpc.add_GlossaryServicer_to_server(GlossaryServicer(storage), server)

    SERVICE_NAMES = (
        glossary_pb2.DESCRIPTOR.services_by_name['Glossary'].full_name,
        reflection.SERVICE_NAME,
    )

    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port(f'{host}:{port}')
    server.start()
    print(f"gRPC server started on {host}:{port}")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == "__main__":
    serve()
