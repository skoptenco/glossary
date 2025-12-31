# client.py
import grpc
import glossary_pb2
import glossary_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as ch:
        stub = glossary_pb2_grpc.GlossaryStub(ch)

        # Create
        create_resp = stub.CreateTerm(glossary_pb2.CreateTermRequest(keyword="Python", description="A programming language"))
        print("Create:", create_resp.created, create_resp.error)

        # Get
        get_resp = stub.GetTerm(glossary_pb2.GetTermRequest(keyword="python"))
        print("Get:", get_resp.found, get_resp.term.keyword, get_resp.term.description)

        # List
        list_resp = stub.ListTerms(glossary_pb2.ListTermsRequest())
        print("List:", [(t.keyword, t.description) for t in list_resp.terms])

        # Update
        upd = stub.UpdateTerm(glossary_pb2.UpdateTermRequest(keyword="python", description="High-level programming language"))
        print("Update:", upd.updated, upd.error)

        # Delete
        delr = stub.DeleteTerm(glossary_pb2.DeleteTermRequest(keyword="python"))
        print("Delete:", delr.deleted, delr.error)

if __name__ == "__main__":
    run()
