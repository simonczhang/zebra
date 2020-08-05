# Instructions

homework.py - Run to create the output csv from the sample csv input files
test_homework.py - Unit testing file

There is one main function that creates the output csv
It takes in a list of csv file paths, the output csv file path, and the output csv schema. 
It checks each csv in the list and determines if it can even be imported at all.
If so, then it goes through each row and each field value and performs some checks based on the output schema criteria 
and then writes the row to the output file, flagging any rows that had issues along the way

It assumes that we are retrieving the csv files locally for this exercise and also outputs to the current directory

List of csv file paths can be changed to test other files, but those files need to exist in the correct directory also.

Running the homework.py file will output the csv with the sample auto and home csv files concatenated together based on the outlined criteria. It will also print the top 15 rows of the csv just so you can easily see the result

Running test_homework.py file will show the result of some unit testing also
I tried testing some csv fringe cases like if the csv is completely blank or if the csv is missing any necessary output fields it will keep track of those errors so you can go back to the partner to ask about it

I tried accounting for as many string variations in order to clean up each field value, but obviously it's impossible for me to know every possible scenario ahead of time.

I wasn't sure the best way to validate 2 of my functions that just processes the csv file (reading/writing). Maybe I could have made it more modular. I ended up just testing that the functions' output being equal to the correct number of rows added for each file, and for the other function, the correct number of files added from the list of files.




