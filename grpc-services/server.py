# server

from concurrent import futures
import logging
import grpc
import tracetogether_pb2
import tracetogether_pb2_grpc
import time
from storagehandler import StorageHandler


class TraceTogether(tracetogether_pb2_grpc.TraceTogetherServicer):

    def Login(self, request, context):
        """Login with name and NRIC"""
        status = StorageHandler().verify(request.name, request.nric)
        reply = tracetogether_pb2.Reply()
        if status:
            StorageHandler().login(request.nric)
            reply.message = 'Successfully logged in as {}, {}.'.format(request.name, request.nric)
            reply.status = 200
        else:
            reply.message = 'User {}, {} does not exist.'.format(request.name, request.nric)
            reply.status = 401

        return reply

    def Logout(self, request, context):
        """Logout with name and NRIC"""
        reply = tracetogether_pb2.Reply()

        StorageHandler().logout(request.nric)
        reply.message = 'Successfully logged out.'

        return reply

    def CheckIn(self, request, context):
        """Check in"""
        StorageHandler().checkIn(request.nric, request.location, request.time)
        return tracetogether_pb2.Reply(
            message='{}, {} successfully checked in at {} on {}'.format(request.name, request.nric, request.location,
                                                                        request.time))

    def CheckOut(self, request, context):
        """Check out"""
        StorageHandler().checkOut(request.nric, request.time)
        return tracetogether_pb2.Reply(
            message='Successfully checked out')

    def GetLocations(self, request, context):
        """Get SafeEntry location history"""
        history = StorageHandler().getLocations(request.nric)
        reply = tracetogether_pb2.Reply()
        reply.message = history

        return reply

    def GetStatus(self, request, context):
        """Get Covid19 exposure status"""
        status = StorageHandler().getStatus(request.nric)
        reply = tracetogether_pb2.Reply()

        if status == False:
            reply.status = 200

        else:
            reply.status = 401

        return reply


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
