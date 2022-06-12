# server

from concurrent import futures
import logging
import grpc
import tracetogether_pb2
import tracetogether_pb2_grpc
import time


class TraceTogether(tracetogether_pb2_grpc.TraceTogetherServicer):

    # Check in
    def CheckIn(self, request, context):
        return tracetogether_pb2.Reply(
            message='{}, {} successfully checked in at {} on {}'.format(request.name, request.nric, request.location,
                                                                        request.time))

    # Test concurrency
    def Test(self, request, context):
        for i in range(10):
            yield tracetogether_pb2.Reply(message='Message {}'.format(i))
            time.sleep(1)



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
