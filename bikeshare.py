import time
import pandas as pd
import numpy as np
import calendar as cal
import sys
from termcolor import colored,cprint

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Pluck city names out of CITY_DATA
city_data_str = ', '.join([str(elem) for elem in CITY_DATA.keys()])  
# Generate list of months with an "ALL" option
month_selection = cal.month_name[1:7]
month_selection.append('All')
# Generate list of days with an "ALL" option
day_selection = cal.day_name[0:]
day_selection.append('All')
# Lambda functions for colorizing text
print_green = lambda x: cprint(x, 'green')
print_red = lambda x: cprint(x, 'red')
print_yellow = lambda x: cprint(x, 'yellow')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print_yellow('Hello! Let\'s explore some US bikeshare data!\n')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        try:
            city = input('Please select your city: ' + city_data_str.title() + '\n\n-->').lower()
            if city in CITY_DATA.keys():
                print_green('\n{} Selected.\n'.format(city))
                break
        except KeyboardInterrupt:
            sys.exit(print_red('CTRL-C received...exiting.'))
        else:
            print_red('\nInvalid input detected.\n')

    # get user input for month (all, january, february, ... , june)
    
    while True:
        try:
            month = input('\nPlease select the month you would like to examine: ' + str(month_selection) + '\n\n-->').title()
            if month in month_selection:
                print_green('\n{} Selected.\n'.format(month)) 
                break
        except KeyboardInterrupt:
            sys.exit(print_red('CTRL-C received...exiting.'))
        else:
            print_red('\nInvalid input detected.\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        try:
            day = input('\nPlease select the day you would like to examine: ' + str(day_selection) + '\n\n-->').title()
            if day in day_selection:
                print_green('\n{} Selected.\n'.format(day)) 
                break
        except KeyboardInterrupt:
            sys.exit(print_red('CTRL-C received...exiting.'))
        else:
            print_red('\nInvalid input detected.\n')

    print_yellow('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print_yellow('Loading selected data and filters...')

    df = pd.read_csv(CITY_DATA[city])
    # format dataframe
    df = df.rename(columns={'Unnamed: 0': 'ID'})
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month_name()
    df['Weekday'] = df['Start Time'].dt.weekday_name
    if month != 'All':
        df = df[df['Month'] == month]
    if day != 'All':
        df = df[df['Weekday'] == day]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print_yellow('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    print_green('-'*40)

    # display the most common month
    print('Top Start Month:', df['Month'].mode()[0])

    # display the most common day of week
    print('Top Start Day:', df['Weekday'].mode()[0])

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    print('Top Start Hour:', df['Hour'].mode()[0])
    print_green('-'*40)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print_yellow('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    print_green('-'*40)

    # display most commonly used start station
    print('Top Starting Locale:', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Top Ending Locale:', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' / ' + df['End Station']
    print('Top Trip:', df['Trip'].mode()[0])
    print_green('-'*40)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print_yellow('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    print_green('-'*40)

    # display total travel time
    print('Total Travel Seconds:', df['Trip Duration'].sum())

    # display mean travel time
    print('Mean Travel Seconds:', df['Trip Duration'].mean())
    print_green('-'*40)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print_yellow('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    print_green('-'*40)

    # display counts of user types
    print(df['User Type'].value_counts())
    print_green('-'*40)

    # display counts of gender
    if 'Gender' in df:
        print(df['Gender'].value_counts())
    else:
        print('No gender data for Washington.')
    print_green('-'*40)

    # display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('Oldest Birth Year:', df['Birth Year'].min())
        print('Newest Birth Year:', df['Birth Year'].max())
        print('Most Common Birth Year:', df['Birth Year'].mode()[0])
    else:
        print('No birth year data for Washington.')
    print_green('-'*40)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print_yellow('-'*40)

def buffer_data(df):
    """Buffer data five rows at a time based on user input"""
    while True:
        try:
            display_rows = input('\nWould you like to display five rows of raw data? Please enter yes or no.\n\n-->').lower()
            if display_rows == 'yes':
                row_count = 0
                while True:
                    try:
                        for row in range(row_count, len(df.index)):
                            print_green('-'*40)
                            print('\n', df.iloc[row_count:row_count+5].to_string(justify='left', na_rep=''), '\n')
                            row_count += 5
                            print_green('-'*40)
                            continue_buffer = input('\nDisplay an additional five rows? Please enter yes or no.\n\n-->').lower()
                            while continue_buffer not in ['yes' , 'no']:
                                continue_buffer = input('\nInvalid input detected. Please enter yes or no.\n\n-->').lower()
                            if continue_buffer != 'yes':
                                break
                    except KeyboardInterrupt:
                        sys.exit(print_red('CTRL-C received...exiting.'))
                    break
        except KeyboardInterrupt:
            sys.exit(print_red('CTRL-C received...exiting.'))
        else:
            print_red('No raw data chosen.')
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        buffer_data(df)

        try:
            restart = input('\nWould you like to restart? Enter yes or no.\n\n-->')
            if restart.lower() == 'no':
                sys.exit(print_red('Program complete...exiting'))

if __name__ == "__main__":
	main()
