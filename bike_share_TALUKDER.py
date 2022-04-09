#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import pandas as pd
import numpy as np
from difflib import get_close_matches


# In[2]:


CITY_DATA = {'chicago': 'chicago.csv',
            'new york city': 'new_york_city_csv',
            'washington': 'washington.csv'}


# In[3]:


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    month_dict = {1: 'january', 2: 'february', 3:'march', 4: 'april', 5: 'may', 6: 'june', 
                  7:'july', 8: 'august', 9:'spetember', 10: 'october', 11: 'november', 12:'december'}
    while True: 
        try:
            print("Please enter a city name here. Available cities are WASHINGTON, CHICAGO, NEW YORK CITY.")
            city = input("Enter the city name here: ")
            
            if city.lower() in CITY_DATA.keys():
                
                    month = input("Please enter the name or number of the month(e.g. March or 3).\nIf you do want to use any month filter please enter ALL.\nEnter your month here: ").lower()
                    
                    if month in month_dict.values() or month == 'all':
                        
                        day = input("Please enter your day here (e.g. Monday)\nIf you do want to use any day filter please enter ALL.\nEnter your day here: ")  
                        break
                        
                    elif int(month) <=12:
                        month = month_dict[int(month)]
                        day = input("Please enter your day here (e.g. Monday)\nIf you do want to use any day filter please enter ALL.\nEnter your day here: ").lower()
                        break

                    else:
                        print("Please enter a valid number from 1 to 12 or name of the month (e.g. June)")
                        
            else:
                close_word = get_close_matches(city,CITY_DATA.keys())
                print("Did you mean {}.\n Plese try to re-enter the city name with correct spelling "
                      .format(close_word[0].upper()))
                
                if close_word[0] in CITY_DATA.keys():
                    continue
            
                else:
                    print(" Please check your input data again")
        except:
            print("Sorry!! We do not have any data of this city. Please choose from this three option WASHINGTON, CHICAGO, NEW YORK CITY.")
            continue 
            
    month = month.lower()
    city = city.replace(" ","_")
    return city, month, day
    print("-"*80)


# In[4]:


def load_data(city,month,day):
    
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # reading data from csv
    start_time = time.time()
    df = pd.read_csv(city.lower()+".csv")
    # converting start to date time and making separete columns for month and day  and hour with names
    df ["Month"] = pd.DatetimeIndex(df["Start Time"]).month_name()
    df ['Day'] = pd.DatetimeIndex(df['Start Time']).day_name()
    df['hour'] = pd.DatetimeIndex(df['Start Time']).hour
    
    month_unique = pd.DatetimeIndex(df["Start Time"]).month_name().unique()
    day_unique = pd.DatetimeIndex(df['Start Time']).day_name().unique()
    
    
    if (month== "all") and (day== "all"): # condition for no month and day filter
        df = df
        
    elif (month=="all") and (day.title() in day_unique): # condition for no month and soecific day filter
        df = df[df['Day']== day.title()]
        
    elif (month.title() in month_unique) and (day == 'all'): # condition for specific day and all month filter
        df = df[df['Month']== month.title()]
        
    elif (day.title() in day_unique) and (month.title() in month_unique) : # condition for specifi day and  sepcific month filter
        df = df[(df['Month'] == month.title()) & (df['Day']== day.title())]
        
    else: # if the data is not found
        df = 0
        
        print("Sorry we do not have the data for this month. Try a month from January to June")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)
    
    return df


# In[5]:


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count= df['User Type'].value_counts()
    
    if user_type_count.size == 3: # printing proper user type when the user type is equal to 3
        print("There are {} {} (s), {} {} (s), and {} {} (s)."
              .format(user_type_count[0],user_type_count.index[0],
                      user_type_count[1], user_type_count.index[1],
                      user_type_count[2],user_type_count.index[2]))
        
    elif user_type_count.size == 2: # printing proper user type when the user type is equal to 3
        print("There are {} {} (s) and {} {} (s)."
              .format(user_type_count[0],user_type_count.index[0],
                      user_type_count[1], user_type_count.index[1]))
              
    else: # printing user type for one
        print("There are {} {} (s).".format(user_type_count[0],user_type_count.index[0]))
                                            
    # Display counts of gender
    
    if 'Gender' in df.columns:
        gender_count= df['Gender'].value_counts()
        
        if gender_count.size == 2:
            print("There are {} {} (s), {} {} (s),.".format(gender_count [0], gender_count.index [0],
                                                           gender_count [1], gender_count.index [1]))
            
        else:
            print("There are {} {} (s).".format(gender_count [0], gender_count.index [0]))
            
    else:
        print("Sorry there is no gender data for this city. Try another city.")
              
    # Display earliest, most recent, and most common year of birth
    
    if 'Birth Year' in df.columns:
        # oldest driver birth year
        earliest_birth = df['Birth Year'].min()
        #ypungest driver birth year
        recent_birth = df['Birth Year'].max()
        
        # common birth year
        most_common_birth = df['Birth Year'].value_counts().idxmax()
        
        print( 'Oldest rider born in {}.\nYongest rider born in {}.\nMost common riders are born in {}'
              .format(str(earliest_birth)[0:4],str(recent_birth)[0:4],str(most_common_birth)[0:4]))
    else:
        print("Sorry !!! There is no birth year data for this city. Try another city.")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


# In[6]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['Month'].value_counts().idxmax()
    n_used_month = df['Month'].value_counts().max()
    print("Most common Month is {}. Total {} rides had been completed in this month.".format(most_common_month,str(n_used_month)))
    
    # display the most common day of week
    most_common_day = df['Day'].value_counts().idxmax()
    n_used_day = df['Day'].value_counts().max()
    print("Most common day is {}. Total {} rides had been completed in this day.".format(most_common_day,str(n_used_day)))

    # display the most common start hour
    most_common_hour = df['hour'].value_counts().idxmax()
    n_used_hour = df['hour'].value_counts().max()
    
    print("Most common hour is {}th. Total {} rides had been completed in this hour.".format(most_common_hour,str(n_used_hour)))
    print("\nThis took %s seconds." % (time.time() - start_time))
    
    print('-'*40)


# In[7]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].value_counts().idxmax()
    n_used_start = df['Start Station'].value_counts().max()
    print("Most commonly used start station is {}. Total {} rides had been started from this station."
          .format(most_common_start_station.upper(),str(n_used_start)))
    
    # display most commonly used end station
    most_common_end_station = df['End Station'].value_counts().idxmax()
    n_used_end = df['End Station'].value_counts().max()
    print("Most commonly used end station is {}. Total {} rides had been ended on this station."
          .format(most_common_end_station.upper(),str(n_used_end)))

    # display most frequent combination of start station and end station trip
    df["Start-End"]=df["Start Station"]+ " to " + df["End Station"]
    most_common_station = df['Start-End'].value_counts().idxmax()
    n_used = df['Start-End'].value_counts().max()
    print("Most commonly used route is {}. It has used {} times."
          .format(most_common_station.upper(),str(n_used)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[8]:


def trip_duration_stats(df,month):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    
    total = df["Trip Duration"].sum()
    def sec_day(n):
        day = n//(24*3600)
        n %=  (24*3600)
        hour = n // 3600
        n %= 3600
        minute = n // 60
        seconds = n
        return day, hour, minute, seconds
    
    print("Total travel time is {} days {} hour {} minutes and {} seconds".format(sec_day(total)[0],sec_day(total)[1],sec_day(total)[2],sec_day(total)[2]))
    
    # display mean travel time
    mean_travel = df["Trip Duration"].mean()
    print("Mean travel time is {} minutes {} seconds".format(sec_day(mean_travel)[2],sec_day(mean_travel)[3]))
    
    # sesonal statistics if all month filter all slected
    if month == 'all':
        df['month_end'] = pd.DatetimeIndex(df["End Time"]).month
        trip_duartion_winter = df['Trip Duration'][ (df['month_end'] >= df['month_end'].min()) &(df['month_end']<= 3)].sum()
        print("Total trip duration in winter is {} days {} hour {} minutes and {} seconds"
              .format(sec_day(trip_duartion_winter)[0],
                      sec_day(trip_duartion_winter)[1],sec_day(total)[2],
                      sec_day(trip_duartion_winter)[2]))
        
        trip_duartion_summer = df['Trip Duration'][ (df['month_end'] <= df['month_end'].max()) &(df['month_end'] >= 3)].sum()
        
        print("Total trip duration in summer is {} days {} hour {} minutes and {} seconds"
              .format(sec_day(trip_duartion_summer)[0],
                      sec_day(trip_duartion_summer)[1],sec_day(total)[2],
                      sec_day(trip_duartion_summer)[2]))
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[9]:


def raw_data (df):
    """Displays the data due filteration.
    5 rows will added in each press"""
    print('press enter to see raw data, press no to skip')
    
    x = 0
    while (input()!= 'no'):
        x = x+5
        print(df.head(x))


# In[10]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if type(df) is pd.core.frame.DataFrame:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df,month)
            user_stats(df)
            raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Thanks for your time. Have a nice day.")
            break


if __name__ == "__main__":
	main()

