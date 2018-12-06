# This function outputs results. If no second argument passed, then it goes to stdout
# Otherwise, it expects a file name that it can successfully open. No error checking done for write access.
def OutputResults(vote_sum, totalvotes, winner, file_name=None):
    import sys
    if file_name is None:
        fd = sys.stdout
    else:
        fd = open(file_name, 'w')

# write to fd
    fd.write("Election Results\n")
    fd.write("----------------\n")
    fd.write("Total Votes: " + str(totalvotes) + "\n")
    fd.write("----------------\n")
    for key in vote_sum:
        fd.write("   " + key + ": " + str(round(100*vote_sum[key]/totalvotes, 3)) + "% (" + str(vote_sum[key]) + ")\n")
    fd.write("----------------\n")
    fd.write("Winner: " + winner + "\n")
    fd.write("----------------\n")
    if fd != sys.stdout:
        fd.close();

# This function loops through the results summary dictionary to find the 
# candidate with the most votes and declares the winner
def GetWinner(results_dict):
    highvotes=0
    winner=""
    for key in results_dict:
        if results_dict[key] > highvotes:
            highvotes = results_dict[key]
            winner = key
    return winner

# This function loops through the results summary dictionary to get total votes cast
def GetTotal(results_dict):
    totalvotes = 0
    for key in results_dict:
        totalvotes+= results_dict[key]
    return totalvotes

# Main vote counting program
import os
import csv

election_data = os.path.join("resources", "election_data.csv")       # Keep data in a local subdirectory
election_results = os.path.join("resources", "election_results.txt")
CAND_COL = 2

vote_sum = {}
tmpd = {}

with open(election_data, newline="") as csvfile:
    ed = csv.reader(csvfile, delimiter=",")                                 # Get pointer to csv file
    next(ed)                                                                # Skip header
    for row in ed:                                                          # Loop to count the votes
        cd = row[CAND_COL]                                                  # Get candidate voted for
        votectr = int(0 if vote_sum.get(cd) is None else vote_sum.get(cd))  # Get current vote count for this candidate
        votectr+=1                                                          # Increment count for this vote
        tmpd = {cd : votectr}                                               # Store result in temp dict
        vote_sum.update(tmpd)                                               # Update the vote_sum dict

total = GetTotal(vote_sum)
winner = GetWinner(vote_sum)
OutputResults(vote_sum, total, winner)
OutputResults(vote_sum, total, winner, election_results)
