#server

from concurrent import futures
import logging
import grpc
import tracetogether_pb2
import tracetogether_pb2_grpc

class TraceTogether(tracetogether_pb2_grpc.TraceTogetherServicer):
    def CheckStatus(self, request, context):
        return tracetogether_pb2.Reply(message='Success, %s' % request.name)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tracetogether_pb2_grpc.add_TraceTogetherServicer_to_server(TraceTogether(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server is running")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()