# Importing the Modules

import os

import csv


# Setting variables for the program

total_months = 0

total_profit_and_loss = 0

earlier_profit_and_loss = 0

monthly_change = 0

total_monthly_change = 0

average_monthly_change = 0

profits_greatest_increase = 0

profits_greatest_increase_month = ""

profits_greatest_decrease = 0

profits_greatest_decrease_month = ""



# Open the CSV data file

with open("budget_data.csv", newline="") as budget_data_csvfile:

    csv_reader = csv.reader(budget_data_csvfile, delimiter=",")



    # To read the header row first

    csv_header = next(csv_reader)



    # Using 'for' loop to read each row of data after the header

    for row in csv_reader:

        # counting the total number of months

        total_months = total_months + 1



        # adding up the total to get net total profit and loss

        total_profit_and_loss = total_profit_and_loss + int(row[1])



        # calculating the change in profit and loss between months

        if total_months > 1:

            monthly_change = int(row[1]) - earlier_profit_loss



        # adding up the total monthly change to calculate average later in the program

        total_monthly_change = total_monthly_change + monthly_change



        # setting profit and loss value for earlier month

        earlier_profit_loss = int(row[1])



        # calculating highest increase in profits

        if monthly_change > profits_greatest_increase:

            profits_greatest_increase = monthly_change

            profits_greatest_increase_month = row[0]



        # calculating highest decrease in losses

        if monthly_change < profits_greatest_decrease:

            profits_greatest_decrease = monthly_change

            profits_greatest_decrease_month = row[0]



# calculating average change between months(from total monthly change calculated above)

average_monthly_change = total_monthly_change / (total_months - 1)



# Printing analysis to the terminal

print("Financial Analysis")

print("----------------------------")

print("Total Months: " + str(total_months))

print("Total: $" + str(total_profit_and_loss))

print("Average Change: $" + str(format(average_monthly_change, '.2f')))

print("Greatest Increase in Profits: " + profits_greatest_increase_month

      + " ($" + str(profits_greatest_increase) + ")")

print("Greatest Decrease in Profits: " + profits_greatest_decrease_month

      + " ($" + str(profits_greatest_decrease) + ")")



# Writing to text file(analysis.txt)

f = open("analysis.txt", "w")

f.write("Financial Analysis\n")

f.write("----------------------------\n")

f.write("Total Months: " + str(total_months) + "\n")

f.write("Total: $" + str(total_profit_and_loss) + "\n")

f.write("Average Change: $" + str(format(average_monthly_change, '.2f')) + "\n")

f.write("Greatest Increase in Profits: " + profits_greatest_increase_month

      + " ($" + str(profits_greatest_increase) + ")\n")

f.write("Greatest Decrease in Profits: " + profits_greatest_decrease_month

      + " ($" + str(profits_greatest_decrease) + ")\n")

f.close()
