#client

import logging
import grpc
import tracetogether_pb2
import tracetogether_pb2_grpc
import datetime

class Client:
    stub = None

    def __init__(self):
        print('1. Login as user\n'
              '2. Login as officer\n'
              '3. Quit')
        userInput = input()

        if userInput == '3':
            exit(1)

    def run(self):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = tracetogether_pb2_grpc.TraceTogetherStub(channel)
            response = stub.CheckIn(tracetogether_pb2.Request(name='Bob', nric='S1234567A', location='NYP', time=str(datetime.datetime.now())))
            print("Client received: " + response.message)

            responses = stub.Test(tracetogether_pb2.Request())
            for response in responses:
                print(response.message)


if __name__ == '__main__':
    logging.basicConfig()
    Client().run()