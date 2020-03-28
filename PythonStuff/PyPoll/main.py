# Importing the Modules

import os

import csv



# Seting variables to run in the program

total_votes = 0

candidates = ""

candidates_list = []

cast_vote_list = []

vote_percent_list = []

poll_winner = ""



# Open the CSV data file

with open("election_data.csv", newline="") as election_data_csvfile:

    csv_reader = csv.reader(election_data_csvfile, delimiter=",")



    # Reading the header row first

    csv_header = next(csv_reader)



    # Using 'for' loop to read each row of data after the header

    for row in csv_reader:

        # counting the total number of votes

        total_votes = total_votes + 1



        if row[2] not in candidates_list:

            candidates_list.append(row[2])

            cast_vote_list.append(1)

        else:

            cast_vote_list[candidates_list.index(row[2])] = cast_vote_list[candidates_list.index(row[2])] + 1



# Calculating the percent of votes cast

vote_percent_list = [(100/total_votes) * x for x in cast_vote_list]



# Finding the poll winner at large

poll_winner = candidates_list[cast_vote_list.index(max(cast_vote_list))]



# Printing analysis to the terminal

print("Election Results")

print("-------------------------")

print("Total Votes: " + str(total_votes))

print("-------------------------")



for x in candidates_list:

    print(x + ": " + str(format(vote_percent_list[candidates_list.index(x)], '.3f'))

        + "% (" + str(cast_vote_list[candidates_list.index(x)]) + ")")



print("-------------------------")

print("Winner: " + poll_winner)

print("-------------------------")



# Writing to the text file(analysis.txt)

f = open("analysis.txt", "w")



f.write("Election Results\n")

f.write("-------------------------\n")

f.write("Total Votes: " + str(total_votes) + "\n")

f.write("-------------------------\n")



for x in candidates_list:

    f.write(x + ": " + str(format(vote_percent_list[candidates_list.index(x)], '.3f'))

        + "% (" + str(cast_vote_list[candidates_list.index(x)]) + ")\n")



f.write("-------------------------\n")

f.write("Winner: " + poll_winner + "\n")

f.write("-------------------------\n")



f.close()
