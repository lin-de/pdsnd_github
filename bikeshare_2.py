import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    while True:
        city = input('\nWould you like to see data for Chicago, New York City, or Washington?\n').lower()
        if city in ('chicago', 'new york city', 'washington'):
            break
        print('\nThat is not a valid city. Please try again.')

    # get user input for month (all, january, february, ... , june) and day of week (all, monday, tuesday, ... sunday)
    while True:
        filter_type = input('\nWould you like to filter the data by month, day, both, or not at all?  Type "none" for no time filter.\n')
        if filter_type == 'month':
            day = 'all'
            month = input('\nWhich month? January, February, March, April, May, or June?\n').lower()
            if month in ('january', 'february', 'march', 'april', 'may', 'june'):
                break
        elif filter_type == 'day':
            month = 'all'
            day = input('\nWhich day? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday?\n').title()
            if day in ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'):
                break
        elif filter_type == 'both':
            month = input('\nWhich month? January, February, March, April, May, or June?\n')
            day = input('\nWhich day? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday?\n').title()
            if day in ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday') and month in ('january', 'february', 'march', 'april', 'may', 'june'):
                break
        elif filter_type == 'none':
            month = 'all'
            day = 'all'
            break
        print('\nYou have entered an invalid filter period.  Please enter a valid filter period.')

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


    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by input month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by input day
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    # returns filtered dataframe
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # calculate statistics for the month
    popular_month_min = df['month'].min()
    popular_month_max = df['month'].max()
    popular_month_mode = df['month'].mode()[0]

    # check if max = min = mode, then month filter applied and don't print popular month message
    if not (popular_month_min == popular_month_max):
        print('Most popular month: ', popular_month_mode)

    # calculate statistics for the day
    popular_day_min = df['day_of_week'].min()
    popular_day_max = df['day_of_week'].max()
    popular_day_mode = df['day_of_week'].mode()[0]

    # check if max = min = mode, then month filter applied and don't print popular day message
    if not (popular_day_min == popular_day_max):
        print('Most popular day: ', popular_day_mode)

    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    popular_start_hour = df['start_hour'].mode()[0]
    print('Most popular start hour: ', popular_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_count = df['Start Station'].value_counts()
    popular_start_station = start_station_count.index[0]
    print('Most commonly used starting station: {}  Count: {}'.format(popular_start_station, start_station_count.values[0]))

    # display most commonly used end station
    end_station_count = df['End Station'].value_counts()
    popular_end_station = end_station_count.index[0]
    print('Most commonly used end station: ', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['start_end_station_combination'] = df['Start Station'] + ' / ' + df['End Station']
    start_end_station_combination_count = df['start_end_station_combination'].value_counts()
    popular_start_end_station_combination = start_end_station_combination_count.index[0]
    print('Most popular start/end station combination: ', popular_start_end_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time (in seconds): ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average travel time (in seconds): ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('Number of users:\n', user_type_count)

    # Display counts of gender if have that information
    try:
        gender_count = df['Gender'].value_counts()
        print('\nGender count:\n', gender_count)
    except:
        pass

    # Display earliest, most recent, and most common year of birth if have that information
    try:
        earliest_birth_year = df['Birth Year'].min()
        print('\nBirth year statistics')
        print('Earliest birth year: ', int(earliest_birth_year))
    except:
        pass

    try:
        latest_birth_year = df['Birth Year'].max()
        print('Latest birth year: ', int(latest_birth_year))
    except:
        pass

    try:
        common_birth_year = df['Birth Year'].mode()[0]
        print('Most common birth year: ', int(common_birth_year))
    except:
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        print('You have selected: {}, {}, {}'.format(city.title(), month.title(), day.title()))
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Display 5 random rows of raw data at user's request
        while True:
            raw_data_request = input('\nWould you like to see 5 lines of raw data? (yes/no)\n')
            if raw_data_request == 'yes':
                raw_data = pd.read_csv(CITY_DATA[city])
                print(raw_data.sample(n=5))
            elif raw_data_request == 'no':
                break
            else:
                print('\nThat is not a valid input.  Please try again.')

        restart = input('\nWould you like to restart the US bikeshare data analysis app? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
