import pandas as pd
import string
import secrets
import os.path
from os import path


class StorageHandler:

    def verify(self,name, nric):
        """Verify that user exists"""
        if path.exists("../storage/Users/{}.csv".format(nric)):
            return True
        else:
            return False

    def login(self, nric):
        """Update logged_in to True"""
        user = pd.DataFrame(pd.read_csv('../storage/Users/{}.csv'.format(nric)))
        user.loc[user.nric == nric, 'logged_in'] = True

        # Store new dataframe to users.csv file
        user.to_csv('../storage/Users/{}.csv'.format(nric), index=False)

    def logout(self, nric):
        """Update logged_in to False"""
        user = pd.DataFrame(pd.read_csv('../storage/Users/{}.csv'.format(nric)))
        user.loc[user.nric == nric, 'logged_in'] = False

        # Store new dataframe to users.csv file
        user.to_csv('../storage/Users/{}.csv'.format(nric), index=False)

    def generateID(self):
        """Generates random ID"""
        id = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(20))
        return id


if __name__ == '__main__':
    # For testing
    print(StorageHandler().verify('Bob','S1234567A'))
    # print(StorageHandler().generateID())

    pass
