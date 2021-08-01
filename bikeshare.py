import time
import pandas as pd
import numpy  as np

CITY_DATA   = { 'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv' }
days        = ['all', 'sunday', 'monday', 'tutuesday', 'wednesday', 'thursday', 'saturday', 'friday']
hrs         = ['12 AM', '01 AM', '02 AM', '03 AM','04 AM','05 AM','06 AM','07 AM','08 AM','09 AM','09 AM','10 AM','11 AM',
               '12 PM', '01 PM', '02 PM', '03 PM','04 PM','05 PM','06 PM','07 PM','08 PM','09 PM','09 PM','10 PM','11 PM']

def info():
    """
    Referances:
    
    1- https://stackoverflow.com/
    2- https://www.javatpoint.com/python-tutorial
    3- https://www.javatpoint.com/numpy-tutorial
    4- https://www.geeksforgeeks.org/
    5- https://www.programiz.com/
    """
    pass

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    day   = 'all'
    month = 'all'
    city  = 'chicago'
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). 
    # HINT: Use a while loop to handle invalid inputs
    print('Would you like to see data for Chicago, Newyork, or washington?')    
    while True:
        city = str(input().strip().lower())
        if (city == 'chicago' or city == 'newyork' or city == 'washington'):
            if city == 'newyork':
                city = 'new york city'
            break
    # TO DO: get user input for filter data (month, day, both or not at all)
    print('Would you like to to filter the data by month, day, both or not at all? HINT: Type \"none\" for no time filter.')
    while True:        
        flter_opt = str(input().lower())
        if flter_opt == 'month' or flter_opt == 'day' or flter_opt == 'both' or flter_opt == 'washington' or flter_opt == 'not at all' or flter_opt == 'none':
            break  

    # TO DO: get user input for month (all, january, february, ... , june)
    if flter_opt == 'month' or flter_opt == 'both':
        while True:
            print('Which month? HINT: All, January, Febrauray, March, April, May, or June.')
            month = str(input().strip().lower())
            if month == 'all' or month == 'january' or month == 'febrauray' or month == 'march' or month == 'april' or month == 'may' or month == 'june':
                break
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    if flter_opt == 'day' or flter_opt == 'both':
        while True:
            print('Which day? HINT: Please Type your response as integer (e.g. 0 = all, 1 = sunday)')
            day_int = int(input().lower())
            if day_int == 0 or day_int == 1 or day_int == 2 or day_int == 3 or day_int == 4 or day_int == 5 or day_int == 6 or day_int == 7:
                day = days[day_int]
                break
    if flter_opt == 'none' or flter_opt == 'not at all':        
        day   = 'all'
        month = 'all' 
        
    print('-'*40)
    return city, month, day

def is_colum(df, col):
    if col in df.columns:
        return True
    else:
        print("we are skipping the calculation in {} colum ...".format(col))
        return False    

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
    print("Just one moment ... \nLoading data...")

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    print("Data loaded...")
    print("Now appling filters ...")
    
    size = df.size

    if is_colum(df, 'Start Time'):
        # convert the Start Time column to datetime
        df['Start Time']    = pd.to_datetime(df['Start Time'])  

        # extract month and day of week from Start Time to create new columns
        df['month']         = df['Start Time'].dt.month
        df['day_of_week']   = df['Start Time'].dt.weekday_name    
        
        # filter by month if applicable
        if month != 'all':
            # use the index of the months list to get the corresponding int
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = months.index(month) + 1
    
            # filter by month to create the new dataframe nonth int
            df = df[df['month'] == month]

        # filter by day of week if applicable
        if day != 'all':
            # filter by day of week to create the new dataframe day str
            df = df[df['day_of_week'] == day.title()]
    else:
        print("restarting program ...")
        main()
    
    print("Now filters applied to city: {}, month: {}, day: {}".format(city, month, day))
    return df, size

def display_data(df):
    start_loc = 0
    print('\nWould you like to view n rows of individual trip data? Hint: Enter yes or no')
    view_data = input('').lower()
    print('\nplease Enter numer of rows of data data to be displayed?')
    n = int(input())
    print('\n\n')

    while view_data == 'yes':
        for i in range(start_loc, start_loc + n, 1):
            print(df.iloc[i,:])
        start_loc   += n
        view_data = input('Do you wish to continue?:').lower()


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month       = df.mode()['month'][0]
    popular_month_count = df['month'].loc[lambda x : x == popular_month].value_counts()
    percentage          = "%.2f" %(float(popular_month_count/size * 100))
    print('-- The most popular month for traveling in {} is [{}] with count of {} i.e. {} %.'.format(city, int(popular_month), list(popular_month_count), percentage))

    # TO DO: display the most common day of week
    popular_day         = df.mode()['day_of_week'][0]
    popular_day_count   = df['day_of_week'].loc[lambda x : x == popular_day].value_counts() 
    percentage          = "%.2f" %(float(popular_day_count/size * 100))
    print('-- The most popular day of week to start traveling in {} is [{}] with count of {} i.e. {} %.'.format(city, popular_day, list(popular_day_count), percentage))

    # TO DO: display the most common start hour
    df['Hour']          = df['Start Time'].dt.hour
    popular_hour_1      = df.mode()['Hour'][0]
    popular_hour        = hrs[int(popular_hour_1)]
    popular_hour_count  = df['Hour'].loc[lambda x : x == popular_hour_1].value_counts()  
    percentage          = "%.2f" %(float(popular_hour_count/size*100))
    print('-- The most popular start hour to start traveling in {} is [{}] with count of {} i.e. {} %.'.format(city, popular_hour, list(popular_hour_count), percentage))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    if is_colum(df, 'Start Station'):
        # TO DO: display most commonly used start station
        popular_start_station       = df.mode()['Start Station'][0]
        popular_start_station_count = df['Start Station'].loc[lambda x : x == popular_start_station].value_counts() 
        percentage                  = "%.2f" %(float(popular_start_station_count/size*100))
        print('-- The most popular start station in {} state is {} with count of {} i.e. {} %.'.format(city, popular_start_station, list(popular_start_station_count), percentage))
    
    if is_colum(df, 'End Station'):
        # TO DO: display most commonly used end station
        popular_end_station         = df.mode()['End Station'][0]
        popular_end_station_count   = df['End Station'].loc[lambda x : x == popular_end_station].value_counts() 
        percentage                  = "%.2f" %(float(popular_end_station_count/size*100))
        print('-- The most popular end station in {} state is {} with count of {} i.e. {} %.'.format(city, popular_end_station, list(popular_end_station_count), percentage))
    
    if is_colum(df, 'Start Station') and is_colum(df, 'End Station'):
        # TO DO: display most frequent combination of start station and end station trip
        df['stat+stop'] = df['Start Station'] + df['End Station']
        popular_start_end_station       = df.mode()['stat+stop'][0]
        popular_start_end_station_count = df['stat+stop'].loc[lambda x : (x == popular_start_end_station)].value_counts() 
        percentage                      = "%.2f" %(float(popular_start_end_station_count/size*100))
        print('-- The most popular combination of start station and end station in {} state is {} with count of {} i.e. {} %.'.format(city, popular_start_end_station, list(popular_start_end_station_count), percentage))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    if is_colum(df, 'Trip Duration'):
        # TO DO: display total travel time
        popular_travel_time         = "%d" %(df['Trip Duration'].sum())
        print('-- The most popular travel time in {} state is {}.'.format(city, popular_travel_time))

        # TO DO: display mean travel time
        popular_travel_time_m       = "%d" %(df['Trip Duration'].mean())
        print('-- The mean travel time in {} state is {}.'.format(city, popular_travel_time_m))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    if is_colum(df, 'User Type'):
        # TO DO: Display counts of user types
        user_subscriber = df['User Type'].loc[lambda x : x == 'Subscriber'].value_counts() 
        user_customer   = df['User Type'].loc[lambda x : x == 'Customer'].value_counts()
        percentage      = "%.2f" %(user_subscriber.astype(float)/size*100)
        print('-- The counts of Subscriber in {} is {} i.e. {} %., Customer is {} i.e. {} %.'.format(city, list(user_subscriber), percentage, list(user_customer), 100 - float(percentage)))

    if is_colum(df, 'Gender'):
        # TO DO: Display counts of gender
        user_Male   = df['Gender'].loc[lambda x : x == 'Male'].value_counts() 
        user_Female = df['Gender'].loc[lambda x : x == 'Female'].value_counts()
        percentage          = "%.2f" %(user_Male.astype(float)/size*100)
        print('-- The counts of Male in {} is {} i.e. {} %., Female is {} i.e. {} %.'.format(city, list(user_Male), percentage, list(user_Female), 100 - float(percentage)))
    if is_colum(df, 'Gender'):
        # TO DO: Display earliest, most recent, and most common year of birth
        earliest_year_of_birth          = df['Birth Year'].min()
        earliest_year_of_birth_count    = df['Birth Year'].loc[lambda x : x == earliest_year_of_birth].value_counts() 
        percentage                      = "%.2f" %(earliest_year_of_birth_count.astype(float)/size*100)
        print('-- The earliest year of birth in {} state is {} with count of {}'.format(city, earliest_year_of_birth, list(earliest_year_of_birth_count), percentage))

        recent_year_of_birth        = df['Birth Year'].max()
        recent_year_of_birth_count  = df['Birth Year'].loc[lambda x : x == recent_year_of_birth].value_counts() 
        percentage                  = "%.2f" %(recent_year_of_birth_count.astype(float)/size*100)
        print('-- The most recent year of birth in {} state is {} with count of {}'.format(city, recent_year_of_birth, list(recent_year_of_birth_count), percentage))

        popular_year_of_birth       = df.mode()['Birth Year'][0]
        popular_year_of_birth_count = df['Birth Year'].loc[lambda x : x == popular_year_of_birth].value_counts() 
        percentage                  = "%.2f" %(popular_year_of_birth_count.astype(float)/size*100)
        print('-- The most popular year of birth in {} state is {} with count of {}'.format(city, popular_year_of_birth, list(popular_year_of_birth_count), percentage))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        global city, month, day, size
        city, month, day = get_filters()
        df, size = load_data(city, month, day)
        # display data per line
        display_data(df)
        
        print('Now calculating the first statistics ...')
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
