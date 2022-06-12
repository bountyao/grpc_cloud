import pandas as pd
import string
import secrets

class StorageHandler:

    def verify(self, name, nric):
        """Verify that user exists"""
        users = pd.DataFrame(pd.read_csv('../storage/users.csv'))
        if name in users.name.values and nric in users.nric.values:
            return True
        else:
            return False

    def generateID(self):
        """Generates random ID"""
        id = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(20))
        return id


if __name__ == '__main__':
    #For testing
    #print(StorageHandler().verify('Bob','S1234567A'))
    #print(StorageHandler().generateID())

    pass