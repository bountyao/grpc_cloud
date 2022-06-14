import pandas as pd
import string
import secrets
from tabulate import tabulate
from os import path


class StorageHandler:

    def verify(self, name, nric):
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

    def checkIn(self, nric, location, time):
        """Check in with location and time"""

        # Set checked_in to True
        user = pd.DataFrame(pd.read_csv('../storage/Users/{}.csv'.format(nric)))
        user.loc[user.nric == nric, 'checked_in'] = True

        # Access linked document
        documentID = user.documentid.values[0]
        record = pd.DataFrame(pd.read_csv('../storage/SafeEntryRecords/{}.csv'.format(documentID)))

        # Store location and time
        checkInDF = {"location": location, "check_in_time": time}
        record = record.append(checkInDF, ignore_index=True)

        user.to_csv('../storage/Users/{}.csv'.format(nric), index=False)
        record.to_csv('../storage/SafeEntryRecords/{}.csv'.format(documentID), index=False)

    def checkOut(self, nric, time):
        # Set checked_in to True
        user = pd.DataFrame(pd.read_csv('../storage/Users/{}.csv'.format(nric)))
        user.loc[user.nric == nric, 'checked_in'] = False

        # Access linked document
        documentID = user.documentid.values[0]
        record = pd.DataFrame(pd.read_csv('../storage/SafeEntryRecords/{}.csv'.format(documentID)))

        print(time)
        # Edit latest row 'checked_out_time' column
        record.loc[record.index[-1], 'check_out_time'] = time

        user.to_csv('../storage/Users/{}.csv'.format(nric), index=False)
        record.to_csv('../storage/SafeEntryRecords/{}.csv'.format(documentID), index=False)

    def getLocations(self, nric):
        """Get SafeEntry location history"""
        user = pd.DataFrame(pd.read_csv('../storage/Users/{}.csv'.format(nric)))
        documentID = user.documentid.values[0]
        history = pd.DataFrame(pd.read_csv('../storage/SafeEntryRecords/{}.csv'.format(documentID)))

        # Tabulate dataframe
        history = tabulate(history, headers=history.columns)

        return history

    def getStatus(self, nric):
        """Retrieve Covid19 exposure status"""
        user = pd.DataFrame(pd.read_csv('../storage/Users/{}.csv'.format(nric)))
        status = user.covid_exposure.values[0]

        print(status)

        if not status:
            return False

        else:
            return True

    def generateID(self):
        """Generates random ID"""
        id = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(20))
        return id

    def official(self,affected_location,affected_datetime):
        official = pd.DataFrame(pd.read_csv('../storage/SafeEntryRecords/affected.csv'))
        affectedDF = {"affected_location": affected_location, "affected_datetime": affected_datetime}
        official = official.append(affectedDF, ignore_index=True)
        official.to_csv('../storage/SafeEntryRecords/affected.csv', index=False)


if __name__ == '__main__':
    # For testing
    # print(StorageHandler().verify('Bob', 'S1234567A'))
    # print(StorageHandler().generateID())
    StorageHandler().getStatus('S1234567A')

    pass
