# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 18:01:17 2021

@author: hello
"""

# Import our packages
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# read from csv file
# read data
df= pd.read_csv('https://raw.githubusercontent.com/Hala-Alsouly/Theatre/main/Theaters.csv')
df.head()


###### return number of students, revenue
def discount(ticketCost,people):
    total = ticketCost * people
    #calculate the Discount for senior and students: 10%
    discountedTicket = total * 0.1
    # calculate the total after apply the Discount
    total = total - discountedTicket
    return total


# calculate the Discount for sunday: 35%
def sundayDiscount (ticketCost,people):
    total = ticketCost * people
    # calculate the Discount for senior and students: 35%
    discountedTicket = total * 0.35
    # calculate the total after apply the Discount
    total = total - discountedTicket
    return total

################################## Snacks Function #####################################

# the function takes snacks data frame to store the sales on it, Branch name, theater number
# and takes number of visitors.It is return the total revenue of the day for a theater.
def snacksF(BranchName, TheaterN, visitorsN):
    #snacks prices
    prices= [6, 8, 10, 8, 7, 9]
    #create a vector of sold snacks
    snack = random.sample(range(10,visitorsN), 6)
    #calculate the sales of snacks for a screen
    snacksSales= np.array(snack) @ np.array(prices)
    #bind it with the branch and theater
    snack= [BranchName, TheaterN,snack]
    return snacksSales,snack

'''
 This function takes theater dataframe, then generates random
 number of visitors for each branch, each theatre, each day, each show time. In addition, call snack
 function to generate random snacks, then save it in snacks dataframe.
 It is return a datafram of the generated visitors and generated snacks.
'''
def runTheatre(theatredf):
    #create visitors dataframe to store the number of visitors
    column_names=['Branch', 'Theater', 'Day', 'Show', 'nAdults', 'nChildren', 'nStudents', 'nSenior']
    visitordf= pd.DataFrame(columns = column_names)

    #create revenue dataframe to store the total revenue for each theatre in each day
    col_names=['Branch', 'Theater', 'Day', 'Show', 'AdultsR', 'ChildrenR', 'StudentsR', 'SeniorR', 'snacksSales']
    revenusdf= pd.DataFrame(columns = col_names)

    #Create snacks dataframe to store the sales
    snacksDF = pd.DataFrame(columns = [])

    #Iterate through days
    for day in range(1,8):
        #row= np.zeros(6)
        
        #iterate through theatres
        for j in range(len(df)):
            
            #iterae by shows numbers
            for show in range(1,df['Shows'][j]+1):
                # store the number of visitors each iteration
                row= np.array([df['Branch'][j],df['Theater'][j], day, show ,0,0,0,0], dtype=object)
                # store the revenue for each iteration
                Rrow= np.array([df['Branch'][j],df['Theater'][j], day, show ,0,0,0,0,0], dtype=object)

                # The least visitor accepted is 30
                startSeat=30
                # if it is weekend increase the visiting chance
                if day in range(5,8):
                    startSeat= df['seats'][j] // 2
                adults= np.random.randint(low=startSeat, high=df['seats'][j])
                availableSeats= df['seats'][j] - adults

                #generate students sample from the previous adults
                students= np.random.randint(low=0, high= adults//2)
                row[6]= students
                # 10% discount for students
                Rrow[6]= discount(df['AdultCost'][j],students)

                adults-= students

                #generate senior sample from the previous adult
                senior= np.random.randint(low=0, high= adults//4)
                row[7]= senior
                # 10% discount for senior on Friday
                if day == 6:
                    Rrow[7]= discount(df['SeniorCost'][j],senior)
                else:
                    Rrow[7]= senior * df['SeniorCost'][j]

                adults-= senior
                row[4]= adults
                Rrow[4]= adults * df['AdultCost'][j]

                # conditional statements for movies that children are allowed to watch
                if( df['AgeRate'][j] == "PG" or df['AgeRate'][j] == "PG-13"):
                    children= np.random.randint(low=0, high= availableSeats)
                    row[5]= children
                    Rrow[5]= children * df['ChildCost'][j]
                    availableSeats-= children

                #Apply Sunday discount
                if day==1:
                    Rrow[4]= sundayDiscount(df['AdultCost'],adults)
                    Rrow[5]= sundayDiscount(df['ChildCost'][j],children)
                    Rrow[6]= sundayDiscount(df['AdultCost'][j],students)
                    Rrow[7]= sundayDiscount(df['SeniorCost'][j],senior)
                    
                # call  snacks function to generate snacks
                sales, snack = snacksF(df['Branch'][j], df['Theater'][j], df['seats'][j]-availableSeats)
                
                #add it to the dataframe
                snacksDF =snacksDF.append({'Branch':snack[0],
                                        'Theater':snack[1],
                                        'Small Popcorn':snack[2][0],
                                        'Medium Popcorn':snack[2][1],
                                        'Large Popcorn':snack[2][2],
                                        'Icecream':snack[2][3],
                                        'Soft Drink':snack[2][4],
                                        'Frozen':snack[2][5]}, ignore_index=True)
                Rrow[8]= sales  

                # append the geneated visitors to the dataframe
                visitordf.loc[len(visitordf.index)] = row

                # append the revenues to the dataframe
                revenusdf.loc[len(revenusdf.index)] = Rrow

                
    return visitordf, snacksDF, revenusdf

'''
 This function takes visitors dataframe, then generates random
 number of visitors for each branch, each theatre, each day, each show time.
 It is return a datafram of the generated info.
'''

def  calculateRevenues(visitordf, filter=False):
    # if no filter selected then calculate the total revenue
    if filter==False:
        df= visitordf[['AdultsR', 'ChildrenR', 'StudentsR', 'SeniorR', 'snacksSales']]
        df= df.sum()
        total= df.to_numpy().sum()

    return total, df

v,s, r = runTheatre(df)
calculateRevenues(r)

v,s, r = runTheatre(df)
calculateRevenues(r)