# client

from ast import pattern
import logging
import grpc
import tracetogether_pb2
import tracetogether_pb2_grpc
import datetime
import re

class Client:
    stub = None
    name = None
    nric = None
    checkedin_names = None
    checkedin_nric = None
    checkedinFlag = False

    def __init__(self):

        while True:
            print('1. Register new user\n'
                  '2. Login as user\n'
                  '3. Login as MOH officer\n'
                  '4. Quit')

            userInput = input()

            if userInput == '4':
                exit(1)

            with grpc.insecure_channel('localhost:50051') as channel:
                self.stub = tracetogether_pb2_grpc.TraceTogetherStub(channel)

                if userInput == '1':
                    self.register()

                if userInput == '2':
                    self.userInterface()

                if userInput == '3':
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

    def register(self):
        """Login with name and NRIC"""
        while True:
            print("Enter name: ")
            self.name = input()
            print("Enter NRIC: ")
            self.nric = input()

            response = self.stub.Register(
                tracetogether_pb2.Request(name=self.name.upper(), nric=self.nric))
            print(response.message)

            if response.status == 200:
                break
            elif response.status == 401:
                continue

    def login(self):
        """Login with name and NRIC"""
        while True:
            print("Enter name: ")
            self.name = input()
            print("Enter NRIC: ")
            self.nric = input()

            response = self.stub.Login(
                tracetogether_pb2.Request(name=self.name.upper(), nric=self.nric))
            print(response.message)

            if response.status == 200:
                break
            elif response.status == 401:
                continue

    def dashboard(self):
        """Dashboard to display Covid-19 exposure status and check-in/out"""

        while True:

            print('1. Check-in\n'
                  '2. Check-out\n'
                  '3. SafeEntry location history\n'
                  '4. Check notification\n'
                  '5. Logout')
            userInput = input()

            if userInput == '1':
                self.checkIn()

            if userInput == '2':
                self.checkOut()

            if userInput == '3':
                self.getLocations()

            if userInput == '4':
                self.getNotification()

            if userInput == '5':
                response = self.stub.Logout(
                    tracetogether_pb2.Request(name=self.name, nric=self.nric))
                print(response.message)
                break

    def checkIn(self):
        """Check In"""

        if self.checkedinFlag == True:
            print('Already checked in . . .')

        else:

            while True:
                print("Enter name (For multiple users, separate with commas): ")
                self.checkedin_names = input()

                print("Enter NRIC: (For multiple users, separate with commas)")
                self.checkedin_nric = input()

                if len(self.checkedin_names.split(',')) != len(self.checkedin_nric.split(',')):
                    print('Please ensure that the total number of NRICs entered corresponds to the number of names')
                    continue
                else:
                    print("Enter location: ")
                    location = input()

                    response = self.stub.CheckIn(
                         tracetogether_pb2.Request(name=self.checkedin_names, nric=self.checkedin_nric, location=location,
                                                   time=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
                    print(response.message)

                    if response.status == 200:
                        self.checkedinFlag = True
                        break

                    elif response.status == 401:
                        continue


    def checkOut(self):
        """Check Out"""

        if self.checkedinFlag == False:
            print('Already checked out . . .')

        else:
            self.checkedinFlag = False
            response = self.stub.CheckOut(
                tracetogether_pb2.Request(nric=self.checkedin_nric, time=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
            print(response.message)


    def getLocations(self):
        """Get all SafeEntry locations"""

        response = self.stub.GetLocations(
            tracetogether_pb2.Request(nric=self.nric))
        print(response.message)

    def getNotification(self):
        """Check notifications"""
        response = self.stub.GetStatus(
            tracetogether_pb2.Request(nric=self.nric))
        print(response.message)

    def officerInterface(self):
        """Log in as MOH Official"""
        print("Enter Location Affected by COVID: ")
        affected_location = input()
        print("Enter DateTime of Visit: YYYY-MM-DD HH:MM:SS ")
        affected_datetime = input()

        response = self.stub.AddCovidLocation(
            tracetogether_pb2.Request(location=affected_location, time=affected_datetime))
        print(response.message)


if __name__ == '__main__':
    logging.basicConfig()
    Client()
