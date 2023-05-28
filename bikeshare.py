
import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


# New print function to add slow effect to the print function
def print_s(text, delay=0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def get_filters():

    print_s('Hello! Welcome to this interactive experience to explore US bikeshare data, provided by Motivate!')

    print_s('Motivate is a bike share system provider for many major cities in the United States')

    print_s('Available cities: Chicago, New York City and Washington DC')

    # using input function to get the desired city from the user

    while True:
        city = input('To begin, please type the name of one of the available cities (chicago, new york city, washington): ').lower()

        if city in ['chicago', 'new york city', 'washington']:
            confirm = input(f'"{city}" was selected. Shall we proced? (yes/no): ').lower()
            
            if confirm == 'yes':
                break
            elif confirm == 'no':
                continue
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

        else:
            print(f'My apologies, but at the moment the data for "{city}" is not available in our database. Please try again.')
            continue

    # getting user input for the desired month filter

    month = input('Please, type the desired month to have the data displayed (entire year, january, february, ..., june): ').lower()
    while month not in ['entire year', 'january', 'february', 'march', 'april', 'may', 'june']:
        print(f'Unfortunatelly, "{month}" is not a valid input. Please try again.')
        month = input('Please type the desired month to have the data displayed (entire year, january, february, ..., june): ').lower()

    # getting user input for day to be displayed

    day = input('Last step. Please type the desired time (day/week) to filter the data (weekly, monday, tuesday, ..., sunday): ').lower()
    while day not in ['weekly', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        print(f'It seems that "{day}" is not a valid input. Please try again.')
        day = input('Enter the name of the day of the week (weekly, monday, tuesday, ..., sunday): ').lower()

    # Displaying filters

    print('\nYou selected the following filters:')
    print(f'City: {city.capitalize()}')
    print(f'Month: {month.capitalize()}')
    print(f'Day filter: {day.capitalize()}')

    # checking if filters are correct

    confirm_filters = input('Are these filters correct? (yes/no): ').lower()

    if confirm_filters == 'no':
        print_s('\nOh boy, here we go again...\n')  # if not returns to the begining of the functions
        return get_filters()
    if confirm_filters == 'yes':
        print_s('\nAwesome possum!')    # if yes, we get a funny msg
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")

    print('-'*40)
    return city, month, day



def current_filters(city,month,day):
    print(f'Applied filters: {city.capitalize()}, {month.capitalize()}, {day.capitalize()}.\n')


def load_data(city, month, day):
    # Load the data file for the specified city into a df
    file_name = CITY_DATA[city]
    df = pd.read_csv(file_name)

    # Convert start time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Creating new columns by extracting month and the day of the week from the column start time
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()

    # Filtering based on user input for month and day of the week
    if month != 'entire year':
        month = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['Month'] == month]

    if day != 'weekly':
        df = df[df['Day of Week'] == day.title()]

    return df

def display_raw_data(df, num_rows=5):
    """Displays raw data 5 rows at a time."""
    start_index = 0
    continue_display = True

    while continue_display:
        show_raw_data = input("\nWould you like to see the raw data? Enter 'yes' or 'no': ").lower()

        if show_raw_data == 'yes':
            print(f'\nNow displaying {num_rows} lines of raw data:\n')
            print(df.iloc[start_index:start_index + num_rows])
            start_index += num_rows

            if start_index >= len(df):
                print('No more data left to display.')
                break

        elif show_raw_data == 'no':
            break

        else:
            print('Invalid input. Please try again.')


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print_s('\nAcessing database...\n')
    print_s('\nCalculating time data...\n')
    print('\nDone. Now displaying most frequent times of travel.\n')

    current_filters(city,month,day)

    start_time = time.time()

    # Print most freq month
    if month != 'entire year':
        print(f'Now displaying data for the month of {month}.')
    else:
        top_month_index = df['Month'].mode()[0]
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        top_month = months[top_month_index - 1]
        print(f'{top_month} is the most frequented month of the year.')

    # Print most freq day
    if day != 'weekly':
        print(f'Now displaying data for {day}.')
    else:
        top_day = df['Day of Week'].mode()[0]
        print(f'{top_day} is the most frequented day of the week.')

    # Extracts hour from start time and display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    top_hour = df['Hour'].mode()[0]

    # Converting to AM/PM
    top_hour = pd.to_datetime(str(top_hour), format='%H').strftime('%I %p')
    print(f'{top_hour} is the most common starting hour.')

    print("\nQuery was completed in %s seconds." % (time.time() - start_time))
    print('-'*40)

    # Prompt the user to see raw data
    display_raw_data(df, num_rows=5)


def station_stats(df, city, month, day):
    """Displays statistics on the most popular stations and trip."""
    
    print_s('\nAcessing database...\n')
    print_s('Processing Query...\n')
    print('Done. Now displaying stations data.\n')
    
    current_filters(city,month,day)

    start_time = time.time()

    # Print most used start stations
    top_start_station = df['Start Station'].mode()[0]
    print(f'Most trips beggin from the station: {top_start_station}')

    # Print most used end station
    top_end_station = df['End Station'].mode()[0]
    print(f'Most trips end at the station: {top_end_station}')

    # Print the most freq combination of start and end stations of the trips
    top_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f'The most common route is (Start station, End Station): {top_trip}')

    print("\nQuery was completed in %s seconds." % (time.time() - start_time))
    print('-'*40)

        # Prompt the user to see raw data
    display_raw_data(df, num_rows=5)

def trip_duration_stats(df, city, month, day):
    """Displays statistics on the total and average trip duration."""

    print_s('\nAcessing database...\n')
    print_s('Processing Query...\n')
    print('Done. Now displaying trip duration data.\n')

    current_filters(city,month,day)
    
    start_time = time.time()

   # Calculating total trip duration
    total_duration_seconds = df['Trip Duration'].sum()
    total_hours = total_duration_seconds // 3600
    print(f"The total accumulated trip duration is {total_hours} hours.")

    # Accessing the avg durantion and the time components then printing the avg trip duration
    avg_duration = df['Trip Duration'].mean()
    avg_duration = pd.to_timedelta(avg_duration, unit='s')
    avg_hours = avg_duration.components.hours
    avg_minutes = avg_duration.components.minutes
    avg_seconds = avg_duration.components.seconds

    print(f"The average trip duration is {avg_hours} h {avg_minutes} min {avg_seconds} s.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

        # Prompt the user to see raw data
    display_raw_data(df, num_rows=5)


def user_stats(df, city, month, day):
    """Displays statistics on bikeshare users."""

    print_s('\nAcessing database...\n')
    print_s('Processing user status...\n')
    print('Done. Now displaying user data.\n')
    
    current_filters(city,month,day)


    start_time = time.time()

    # Get the unique user types, count them then print the results

    user_types = df['User Type'].value_counts()
    print("Amount of users per user type:")
    print(user_types.to_string(header=False))

   # Printing gender count
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print("\nUsers by gender:")
        print(gender.to_string(header=False))

        # Calculate gender per user type
        genders_by_user_type = df.groupby('User Type')['Gender'].value_counts()
        print("\nGenders by user type:")
        print(genders_by_user_type.to_string(header=False))

        # Calculate average age per gender
        if 'Birth Year' in df:
            current_year = datetime.datetime.now().year
            average_age = df.groupby('Gender')['Birth Year'].apply(lambda x: np.mean(current_year - x)).round(1)
            print("\nAverage age per gender:")
            print(average_age.to_string(header=False))

        else:
            print("\nUnfortunately, there is no available data regarding birth years. Please try again with new filters.")

    else:
        print("\nUnfortunately, there is no available data regarding gender. Please try again with new filters.")

    if 'Birth Year' in df:
        oldest_user = int(df['Birth Year'].min())
        youngest_user = int(df['Birth Year'].max())
        top_birthyear = int(df['Birth Year'].mode()[0])
        print("\nBirth Year Statistics:")
        print(f'The oldest user was born in {oldest_user}.')
        print(f'The youngest user was born in {youngest_user}.')
        print(f'Most users were born in {top_birthyear}.')
    else:
        print("\nUnfortunately, there is no available data regarding birth years. Please try again with new filters.")


    print('\nQuery was completed in %s seconds.' % (time.time() - start_time))
    print('-' * 40)

        # Prompt the user to see raw data
    display_raw_data(df, num_rows=5)

def menu():

    print("\nWhat statistics would you like to see?")
    print("1. Time Statistics")
    print("2. Station Statistics")
    print("3. Trip Duration Statistics")
    print("4. User Statistics")
    print("5. Exit")
    choice = input("\nType the desired option number: ")
    return choice


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        df = df.dropna()

        def next_action():
            next_action = input("What would you like to see next? 1 - Menu, 2 - Exit: ")

            if next_action == "1":
                return next_action
            elif next_action == "2":
                print("Exiting the program...")
                exit()
            else:
                print("Invalid choice. Please try again.")
            

        while True:
            choice = menu()

            if choice == "1":
                choice = time_stats(df, city, month, day)  
                next_action()
            elif choice == "2":
                choice = station_stats(df, city, month, day)  
                next_action()
            elif choice == "3":
                choice = trip_duration_stats(df, city, month, day) 
                next_action()
            elif choice == "4":
                choice = user_stats(df, city, month, day)  
                next_action()
            elif choice == "5":
                print("Exiting the program...")
                exit()
            else:
                print("Invalid choice. Please try again.")
                next_action()

city, month, day = main()

          

if __name__ == "__main__":
	main()


