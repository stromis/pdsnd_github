import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (chicago, new york, washington), and validate the answer
    while True:
        city = input('Would you like to see data for Chicago, New York or Washington? \n').lower()
        if city not in ('chicago', 'new york', 'washington'):
            print('Sorry, not an appropriate choice.')
        else:
            break

    # Get user input for month (all, january, february, ... , june), and validate the answer
    while True:
        month = input('Which month do you like to filter the data? January, February, March, April, May, June or for All? \n').lower()
        if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print('Sorry, not an appropriate choice.')
        else:
            break

    # Get user input for day of week (all, monday, tuesday, ... sunday), and validate the answer
    while True:
        day = input('Which day do you like to filter the data? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or for All? \n').lower()
        if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            print('Sorry, not an appropriate choice.')
        else:
            break

    print('-'*40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week  and hour from Start Time to create new columns
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # Display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    # Display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('Most Popular Day:', popular_day_of_week)

    # Display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station:', start_station)

    # Display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('The most commonly used end station:', end_station)

    # Display most frequent combination of start station and end station trip by adding a new column
    df['comb_start_end'] = df['Start Station'] + ' --- ' + df['End Station']
    comb_start_end = df['comb_start_end'].mode()[0]
    print('The most frequent combination of start station and end station trip:', comb_start_end)
    # Remove the new column 
    del df['comb_start_end']
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    trip_duration = df['Trip Duration'].sum()
    print('Total travel time for rent bicykles:', trip_duration)
    
    # Display mean travel time
    trip_duration_ave = df['Trip Duration'].mean()
    print('Average travel time for rent bicyles:', trip_duration_ave)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of different user types:')
    print(user_types.to_string())
        
    # Display counts of gender if the column exist
    gender_in_column = "Gender" in df
    if gender_in_column == True:
        gender = df['Gender'].value_counts()
        print('\nCounts of different gender:')
        print(gender.to_string())
    else:
        print('\nColumn Gender does not exist for this choise')
        
    # Display earliest, most recent, and oldest year of birth if the column exist
    birth_in_column = "Birth Year" in df
    if birth_in_column == True:
        birth_year_max = df['Birth Year'].max().astype('Int64')
        birth_year_min = df['Birth Year'].min().astype('Int64')
        birth_year_common = df['Birth Year'].mode()[0].astype('Int64')
        print('\nYoungest that have rent a bike is born:', birth_year_max)
        print('Oldest that have rent a bike is born:', birth_year_min)
        print('Most common year of birth is:', birth_year_common)
    else:
        print('\nColumn Birth Year does not exist for this choise')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def records_per_records(df):
    """Displays 5 record of raw data at a time if the user wants to display the data"""
    x=0
    y=4
    while True:
        answer = input('Do you want to see 5 individual records? \n').lower()
        if answer not in ('yes', 'no'):
            print('Please answer yes or no')
        elif answer == 'yes':
           print(df.loc[x:y, :].to_string(index=False))
           x+=5
           y+=5
        elif answer == 'no':
            break
        else:
            break
            
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        records_per_records(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()