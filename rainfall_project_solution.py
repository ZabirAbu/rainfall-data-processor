import csv

import pandas as pd
import datetime
import re
import os


class RainFallRecord:
    def __init__(self, temp):  # Create dictionary object
        self.dictionary = temp

    def validate(self):  # Validation method of dictionary
        today = datetime.date.today()
        current_year = today.year
        for year, rainfall_values in self.dictionary.items():
            if year > current_year:  # Checking if there are any years in the dictionary that have not passed
                raise ValueError("Only data for previous years can be entered into the system.")
            if len(rainfall_values) != 12:  # Checking if there are 12 rainfall datavalues (including 'None'
                raise ValueError("Invalid data set for a year.")
            if any(value < 0 for value in rainfall_values):  # Checking for negative rainfall values
                raise ValueError("Unexpected negative value found in dataset.")

    def average(self, year, start, end):  # Calculating average rainfall
        if not 1 <= start <= 12 or not 1 <= end <= 12:  # Validating month entry from user
            raise ValueError("Invalid month range. Range should be between 1 and 12.")
        if year not in self.dictionary:  # Validating year is in dictionary
            raise KeyError(f"The year {year} cannot be found in the dataset.")
        for key, values in self.dictionary.items():
            if key == year:
                total_rainfall = sum(values[start - 1: end])
                self.display_months(year)
                return print(f"Average rainfall between {start} and {end}:",  # Calculating average (2 d.p)
                             round(total_rainfall / (end - start + 1), 2))

    def rainfall(self, year, month):  # Returns rainfall value
        if year not in self.dictionary:  # Validating year is in dictionary
            raise KeyError(f"Data for year {year} not found in dataset.")
        rainfall_values = self.dictionary[year]
        if month < 1 or month > 12:  # Validating month entry from user
            raise ValueError("Month must be between 1 and 12.")
        return print("Rainfall for", year, "month", month, ":", rainfall_values[month - 1])

    def delete(self, year, month):  # Deletes rainfall value
        if year not in self.dictionary:  # Validating year is in dictionary
            raise KeyError(f"Data for year {year} not found in dataset.")
        if month < 1 or month > 12:  # Validating month entry from user
            raise ValueError("Month must be between 1 and 12.")
        self.dictionary[year][month - 1] = None  # Change rainfall value to 'None'
        self.display_months(year)  # Returns all data records for a particular year
        return print(f"The record for the year {year} month {month} has been deleted successfully. ")  # Confirmation
        # for the user

    def insert(self, year, month, value):  # Inserting rainfall value
        if year not in self.dictionary:  # Validating year is in dictionary
            raise KeyError(f"Data for year {year} not found in dataset.")
        if month < 1 or month > 12: # Validating month entry from user
            raise ValueError("Month must be between 1 and 12.")
        if value < 0:  # Checking for negative rainfall value entered by user
            raise ValueError("Rainfall cannot be a negative value.")
        self.dictionary[year][month - 1] = value  # Replaces value with users
        self.display_months(year)  # Returns all data records for a particular year
        return print(f"The record for the year {year} month {month} has been successfully replaced with {value}.")
        # Confirmation for the user

    def insert_quarter(self, year, quarter, list_of_values):  # Insert list of rainfall values
        if year not in self.dictionary:  # Validating year is in dictionary
            raise KeyError(f"Data for year {year} not found in dataset.")
        if quarter not in ['winter', 'spring', 'summer', 'autumn']:  # Validating quarter entered by user
            raise ValueError("Quarter must be one of 'winter', 'spring', 'summer', 'autumn'.")
        if len(list_of_values) != 3:  # Validating the number of rainfall values (must be 3)
            raise ValueError("A quarter must have exactly 3 months of data.")
        if any(value < 0 for value in list_of_values):  # Checking for negative rainfall value entered by user
            raise ValueError("Rainfall cannot be a negative value.")
        if quarter == 'winter':  # Entering into the quarters
            self.dictionary[year][0:3] = list_of_values
        elif quarter == 'spring':
            self.dictionary[year][3:6] = list_of_values
        elif quarter == 'summer':
            self.dictionary[year][6:9] = list_of_values
        elif quarter == 'autumn':
            self.dictionary[year][9:12] = list_of_values
        self.display_months(year)  # Returns all data records for a particular yea
        return print(f"The records for {quarter} have been replaced with {list_of_values} respectively.")
        # Confirmation for the user

    def display_months(self, year):
        values = self.dictionary[year]  # All rainfall values for that year
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']  # Better format
        print("Year:", year)
        for i, val in enumerate(values):
            print(f"{months[i]}: {val}")  # Printing month: rainfall value (e.g. 'Jan: 12.0')


class Archive:
    def __init__(self, cn, yr, tmax, tmin, a, rn, sn):  # Constructor for Archive
        self.city = cn
        self.year = yr
        self.max_temp = tmax
        self.min_temp = tmin
        self.af = a
        self.rain = rn
        self.sun = sn

    def insert(self, db):  # Method to insert data into a database

        if os.path.isfile('database.csv'):  # Checking to see if database csv already exits
            data_row = [self.city, self.year, *self.max_temp, *self.min_temp, *self.af, *self.rain, *self.sun]  # Create
            # a list of entire record
            df = pd.read_csv(db)  # Open database file (csv) into a dataframe
            for index, row in df.iterrows():  # Iterate over the dataframe
                if row['city'] == self.city and row['yyyy'] == self.year:  # Checking for duplicate values
                    raise ValueError("Duplicate records cannot be added!")  # Raise error for duplicate values
                else:
                    pass
            dbf = open(db, 'a')  # Open and append csv file
            writer = csv.writer(dbf)  # Creating writer for csv file
            writer.writerow(data_row)  # Inserting record into csv file
            dbf.close()  # Close csv file
            df1 = pd.read_csv(db)  # Convert csv to dataframe
            df1.to_csv(db, index=False)  # Replace csv file contents with dataframe (this is done for formatting purposes)
        else:
            df = pd.DataFrame(columns=['city', 'yyyy', 'mx1', 'mx2', 'mx3', 'mx4', 'mx5', 'mx6', 'mx7', 'mx8', 'mx9', 'mx10', 'mx11', 'mx12', 'mn1', 'mn2', 'mn3', 'mn4', 'mn5', 'mn6', 'mn7', 'mn8', 'mn9', 'mn10', 'mn11', 'mn12', 'af1', 'af2', 'af3', 'af4', 'af5', 'af6', 'af7', 'af8', 'af9', 'af10', 'af11', 'af12', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12'])
            df.to_csv('database.csv', index=False)  # Create database csv with headers

    @staticmethod
    def delete(city, year, db):  # Method to delete from database
        record_delete = False  # Boolean value to benefit user
        df = pd.read_csv(db)  # Convert csv file to dataframe
        for index, row in df.iterrows():  # Iterate over dataframe
            if row['city'] == city and row['yyyy'] == year:  # Checking for record to delete
                df = df.drop(df.index[index])  # Dropping entire record
                print(f"Record successfully deleted for {city} {year}!")  # Confirmation for the user
                record_delete = True
            else:
                pass
        df.to_csv(db, index=False) # Replace csv file contents with dataframe
        if record_delete == False:
            print(f"No such record exists in the database for {city} {year}!")  # Confirmation for the user
        else:
            pass

    @staticmethod
    def sma(city, year1, year2, k):  # Method to return the simple moving average
        df = pd.read_csv('database.csv')  # Convert csv file to dataframe
        df = df[(df['city'] == city) & (df['yyyy'].isin(range(year1, year2 + 1)))]  # Finding necessary years
        temp = df.iloc[:, 38:50].values.flatten()  # Extracting rainfall values for those years
        moving_average = []  # List for moving averages
        i = 0
        for i in range(0, len(temp) - k + 1, k):
            moving_average.append(sum(temp[i:i + k]) / k)  # Calculating moving average and appending
        return moving_average  # Returns list of moving averages


class Driver:
    def __init__(self, tf):  # Constructor for Driver class
        self.file_name = tf

    def run(self):  # Running method for task 1 and task 2
        df = pd.read_csv(self.file_name)  # Convert csv file to dataframe
        df = self.cleaner(df)  # Cleaner function removes anything other than integers/doubles (uses regex)
        df = df.filter([0, 5])  # Filter rows by year and rainfall values
        temp = df.groupby(0)[5].apply(list).to_dict()  # Dictionary which has key: year and values: list[rainfall]
        try:
            temp = RainFallRecord({int(key): [float(x) for x in value] for key, value in temp.items()})  # Convert
            # all values into desired format (year: int, rainfall: floats)
            temp.validate()  # Validate the data before proceeding
            return temp  # Returns dictionary to manipulate
        except ValueError:  # Raise error if there were any issues
            print("An error occurred while reading the data in from the provided file. ")

    def cleaner(self, df):  # Cleaner function to remove anything before/after the data values
        def apply_function(row):
            return pd.Series(  # All values to be converted
                [self.return_number(str(row[0])), self.return_number(str(row[1])), self.return_number(str(row[2])),
                 self.return_number(str(row[3])), self.return_number(str(row[4])), self.return_number(str(row[5])),
                 self.return_number(str(row[6]))])

        df = df.apply(apply_function, axis=1)  # Apply to entire dataframe
        return df

    def return_number(self, value):
        match = re.search(r'[-+]?\d*\.\d+|\d+', value)  # Regex expression to extract floats
        if match:
            return float(match.group())
        else:
            return None  # If it cannot convert any value it will be set as 'None'

    def archive_run(self, cname, db):  # Archive run method for task 3
        df = pd.read_csv(self.file_name).dropna()  # Convert to dataframe and dropping NaN values
        df = self.cleaner(df)  # Cleaner function removes anything other than integers/doubles (uses regex)
        df = df.filter([0, 2, 3, 4, 5, 6])  # Filter dataframe to desired values
        count_row = df.shape[0]  # Finding number of rows of dataframe
        for i in range(0, count_row, 12):  # Iterates through dataframe in groups of 12
            df_transposed = df.transpose()
            result = (int(df_transposed.iloc[0, i]),  # This will take the year as an integer. Then it will take all other values into a list of 12 and append it as a record
                      list(df_transposed.iloc[1, i:i + 12]),
                      list(df_transposed.iloc[2, i:i + 12]),
                      list(df_transposed.iloc[3, i:i + 12]),
                      list(df_transposed.iloc[4, i:i + 12]),
                      list(df_transposed.iloc[5, i:i + 12]))
            temp_o = Archive(cname, result[0], result[1], result[2], result[3], result[4], result[5])  # Creating object of each record
            temp_o.insert(db)  # Inserting object into database

city = 'Aberporth'  # City name (REQUIRED)
test_file = 'Aberporth.csv'  # CSV file (REQUIRED)

## NOTE: ALL CSV FILES MUST INCLUDE THE CORRECT HEADER FORMAT OTHERWISE AN ERROR WILL OCCUR (E.G. LIKE THE ABERPORTH CSV FILE) ##

# Task 1
test = Driver(test_file)
r = test.run()
r.average(1941, 1, 12)

# Task 2
r.rainfall(1941, 12)
r.delete(1941, 12)
r.insert(1941, 12, 30.5)
r.insert_quarter(1941, 'winter', [0, 0.1, 0.2])

# Task 3
database = 'database.csv'
e = test.archive_run(city, database)
Archive.delete('Aberporth', 1941, database)
print(Archive.sma('Aberporth', 1941, 1942, 2))
