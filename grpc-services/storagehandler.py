import pandas as pd
import string
import secrets
from os import path
from dateutil import parser
import datetime


class StorageHandler:

    def verify(self, name, nric):
        """Verify that user exists"""
        if path.exists("../storage/Users/{}.csv".format(nric)):
            user = pd.DataFrame(pd.read_csv('../storage/Users/{}.csv'.format(nric)))
            if user.name.values[0] != name:
                return False, "Wrong name entered for {}.".format(nric)
            else:
                return True, ""
        else:
            return False, "NRIC {} does not exist.".format(nric)

    def register(self, name, nric):
        """Register new user"""

        if path.exists("../storage/Users/{}.csv".format(nric)):
            duplicateFlag = True
        else:
            duplicateFlag = False

        if not duplicateFlag:

            # Generate new ID
            id = self.generateID()

            # Initialize new dataframes
            user = pd.DataFrame(
                {'name': [name], 'nric': [nric], 'logged_in': [False], 'checked_in': [False],
                 'documentid': [id]})
            safeentry_record = pd.DataFrame(columns=['location', 'check_in_time', 'check_out_time'])

            # Write to directory
            user.to_csv('../storage/Users/{}.csv'.format(nric), index=False)
            safeentry_record.to_csv('../storage/SafeEntryRecords/{}.csv'.format(id), index=False)

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

        return history

    def generateID(self):
        """Generates random ID"""
        id = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(20))
        return id

    def addCovidLocation(self, location, start_time):
        """Add affected location"""
        official = pd.DataFrame(pd.read_csv('../storage/affected.csv'))
        affectedDF = {"affected_location": location, "affected_datetime": start_time}
        official = official.append(affectedDF, ignore_index=True)
        official.to_csv('../storage/affected.csv', index=False)

    def checkAffected(self, nric):
        """Check Covid-19 exposure records"""
        affected_locations = pd.DataFrame(pd.read_csv('../storage/affected.csv'))
        user = pd.DataFrame(pd.read_csv('../storage/Users/{}.csv'.format(nric)))
        documentID = user.documentid.values[0]
        history = pd.DataFrame(pd.read_csv('../storage/SafeEntryRecords/{}.csv'.format(documentID)))

        # Add to exposed locations
        exposed_locations = []
        for history_location in history.values:
            day_difference = (parser.parse(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).date() - parser.parse(
                history_location[1]).date()).days

            # Only take past 14 days into account
            if 0 <= day_difference <= 14:
                for affected_location in affected_locations.values:
                    if history_location[0] == affected_location[0] and parser.parse(
                            history_location[1]).date() == parser.parse(affected_location[1]).date():
                        exposed_locations.append(history_location)

        if len(exposed_locations) != 0:
            # Remove duplicates
            exposed_locations = pd.DataFrame(exposed_locations, columns=['location', 'check_in_time', 'check_out_time'])
            exposed_locations = exposed_locations.sort_values(by='check_in_time')
            exposed_locations = exposed_locations.drop_duplicates(subset=['location'], keep='last')

            # Add 14 days to latest date exposed to Covid-19
            release_date = (parser.parse(exposed_locations.values[-1][1]) + datetime.timedelta(days=14)).date()

            return exposed_locations, release_date

        else:
            return (None, None)


if __name__ == '__main__':
    # For testing
    StorageHandler().verify('BOB','S1234567A')

    pass
