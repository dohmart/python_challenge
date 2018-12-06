# This function outputs results. If no second argument passed, then it goes to stdout
# Otherwise, it expects a file name that it can successfully open. No error checking done for write access. 
def OutputResults(fin_ana, file_name=None):
    import sys
    if file_name is None:
        fd = sys.stdout
    else:
        fd = open(file_name, 'w')

# write to fd
    fd.write("Financial Analysis\n")
    fd.write("------------------\n")
    fd.write("   Total Months: " + str(fin_ana["Total_Months"]) + "\n")
    fd.write("   Total : " + str(fin_ana["Total_P/L"].format('en_US')) + "\n")
    fd.write("   Average_Change: " + str(fin_ana["Average_Change"].format('en_US')) + "\n")
    fd.write("   Greatest Increase in Profits: " + str(fin_ana["Max_Pos_P/L_Change"].format('en_US')) + "\n")
    fd.write("   Greatest Decrease in Profits: " + str(fin_ana["Max_Neg_P/L_Change"].format('en_US')) + "\n")
    
    if fd != sys.stdout:
        fd.close();

# This function populates the analysis results dictionary, including calculating the average
def PopulateResults(analysis, count, total, total_pl_change, max_change, min_change):
    analysis["Total_Months"] = count
    analysis["Total_P/L"] = total
    analysis["Average_Change"] = total_pl_change/count
    analysis["Max_Pos_P/L_Change"] = max_change[PL_COL]
    analysis["Max_Neg_P/L_Change"] = min_change[PL_COL]
    return analysis

# This function calculates and returns the running change in profit level.
# It handles up and down using string arg (LessThan, GreaterThan)
def UpdateChange(saved_change, current_change, comp_type):
    if (comp_type == "LessThan"):
        if (current_change[PL_COL] < saved_change[PL_COL]):
            saved_change = list(current_change)
    elif (comp_type == "GreaterThan"):
        if (current_change[PL_COL] > saved_change[PL_COL]):
            saved_change = list(current_change)
    return saved_change


# This is the main program that does the financial analysis
import os
import csv
from money.money import Money                                    # Use py_money from pypi
from money.currency import Currency
budget_data = os.path.join("resources", "budget_data.csv")       # Keep data in a local subdirectory
output_data = os.path.join("resources", "budget_summary.txt")

DATE_COL = 0                                                     # No real constants native to Python (crazy!) and
PL_COL = 1                                                       # Word is all upper-case implies an immutable variable
                                                                 # Interesting debate on stackoverflow on this, and a lot
                                                                 # of work-arounds that I won't use here

#
# Initialize the output record - it's a dictionary
# Probably doesn't really need to be initialized, could be dynamic, 
# but since we know what we want, might as well build it first
#
change_dict = {"Date" : "", "Value" : Money(0, Currency.USD)}
fin_ana = {"Total_Months" : 0,
           "Total_P/L" : Money(0, Currency.USD),
           "Average_Change" : Money(0, Currency.USD),
           "Max_Pos_P/L_Change" : ["", Money(0, Currency.USD)],
           "Max_Neg_P/L_Change" : ["", Money(0, Currency.USD)]
          }
# Initialize various accumulators
n=0 
sumpl = Money(0, Currency.USD)
sumpl_change = Money(0, Currency.USD)
prevpl = Money(0, Currency.USD)
pl_change = ["", Money(0, Currency.USD)]                                # pl_change, max_change, min_change 
max_change = ["", Money(0, Currency.USD)]                               # same list type as row from file
min_change = ["", Money(0, Currency.USD)]
with open(budget_data, newline="") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=",")
    next(csv_reader)
    for row in csv_reader:
        n+=1                                                            # Update row count
        sumpl+= Money(row[PL_COL], Currency.USD)
        if (n>1):                                                       # Do not update P/L change on first month
            pl_change[DATE_COL] = row[DATE_COL]
            pl_change[PL_COL] = Money(row[PL_COL], Currency.USD) - prevpl   # Calculate change from previous month
            max_change = UpdateChange(max_change, pl_change, "GreaterThan")
            min_change = UpdateChange(min_change, pl_change, "LessThan")    #
            sumpl_change+= pl_change[PL_COL]                                # Update P/L change sum
        prevpl = Money(row[PL_COL], Currency.USD)                           # Save previous
fin_ana = PopulateResults(fin_ana, n-1, sumpl, sumpl_change, max_change, min_change)  # Use n-1 for average calc to avoid 1st month
OutputResults(fin_ana)
OutputResults(fin_ana, output_data)