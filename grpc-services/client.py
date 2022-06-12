# client

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

        with grpc.insecure_channel('localhost:50051') as channel:
            self.stub = tracetogether_pb2_grpc.TraceTogetherStub(channel)

            if userInput == '1':
                self.userInterface()

            if userInput == '2':
                self.officerInterface()

    def run(self):
        responses = self.stub.Test(tracetogether_pb2.Request())
        for response in responses:
            print(response.message)

    def userInterface(self):
        # User mode
        self.login()

    def login(self):
        response = self.stub.Login(
            tracetogether_pb2.Request(name='Bob', nric='S1234567A', location='NYP', time=str(datetime.datetime.now())))
        print("Client received: " + response.message)

    def officerInterface(self):
        # TODO
        pass



if __name__ == '__main__':
    logging.basicConfig()
    Client()
