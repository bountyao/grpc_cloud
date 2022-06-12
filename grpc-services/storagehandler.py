import pandas as pd
import string
import secrets

users = pd.DataFrame(pd.read_csv('../storage/users.csv'))

class StorageHandler:

    def verify(self, name, nric):
        """Verify that user exists"""

        if name in users.name.values and nric in users.nric.values:
            return True
        else:
            return False

    def login(self, nric):
        """Update logged_in to True"""
        users.loc[users.nric == nric, 'logged_in'] = True

        # Store new dataframe to users.csv file
        users.to_csv('../storage/users.csv', index=False)

    def logout(self, nric):
        """Update logged_in to False"""
        users.loc[users.nric == nric, 'logged_in'] = False

        # Store new dataframe to users.csv file
        users.to_csv('../storage/users.csv', index=False)

    def generateID(self):
        """Generates random ID"""
        id = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(20))
        return id


if __name__ == '__main__':
    # For testing
    print(StorageHandler().verify('Bob', 'S1234567A'))
    # print(StorageHandler().generateID())

    pass
