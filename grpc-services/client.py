# client

import logging
import grpc
import tracetogether_pb2
import tracetogether_pb2_grpc
import datetime



class Client:
    stub = None
    name = None
    nric = None

    def __init__(self):

        print('1. Login as user\n'
              '2. Login as MOH officer\n'
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
        """User mode"""
        # TODO: implement login error
        self.login()
        self.dashboard()

    def login(self):
        """Login with name and NRIC"""
        # print("Enter name: ")
        # self.name = input()
        # print("Enter NRIC: ")
        # self.nric = input()

        self.name, self.nric = 'Bob','S1234567A'

        response = self.stub.Login(
            tracetogether_pb2.Request(name=self.name, nric=self.nric))
        print(response.message)

    def dashboard(self):
        """Dashboard to display Covid-19 exposure status and check-in/out"""

        while True:

            print('1. Check-in\n'
                  '2. Check-out\n'
                  '3. SafeEntry location history\n'
                  '4. Logout')
            userInput = input()

            if userInput == '1':
                self.checkIn()

            if userInput == '2':
                self.checkOut()

            if userInput == '3':
                self.getLocations()

            if userInput == '4':
                response = self.stub.Logout(
                    tracetogether_pb2.Request(name=self.name, nric=self.nric))
                print(response.message)
                break

    def checkIn(self):
        """Check In"""

        print("Enter name: ")
        name = input()
        print("Enter NRIC: ")
        self.nric = input()
        print("Enter location: ")
        location = input()

        response = self.stub.CheckIn(
            tracetogether_pb2.Request(name=name, nric=self.nric, location=location, time=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
        print(response.message)

    def checkOut(self):
        """Check Out"""

        response = self.stub.CheckOut(
            tracetogether_pb2.Request(nric=self.nric, time=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
        print(response.message)

    def getLocations(self):
        """Get all SafeEntry locations"""

        response = self.stub.GetLocations(
            tracetogether_pb2.Request(nric=self.nric))
        print(response.message)

    def officerInterface(self):
        # TODO
        pass


if __name__ == '__main__':
    logging.basicConfig()
    Client()
