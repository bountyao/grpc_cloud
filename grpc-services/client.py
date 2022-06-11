#client

import logging
import grpc
import tracetogether_pb2
import tracetogether_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = tracetogether_pb2_grpc.TraceTogetherStub(channel)
        response = stub.CheckStatus(tracetogether_pb2.Request(name='you'))
        print("Client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()