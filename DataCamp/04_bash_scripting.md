## Introduction to shell
`;` links commands and runs sequentially, `&&` also links but waits for the previous commandz , `|` pipe uses output of 1st for 2nd command, `>` saves output into file
```shell
$ # when starting with / then it is an absolute path
$ man head # see manual
$ ls -R -F 
$ history # !head, !2
$ cp original.txt duplicate.txt # copy
$ cp seasonal/autumn.csv seasonal/winter.csv backup
$ mv autumn.csv winter.csv # move
$ rm thesis.txt backup/thesis-2017-08.txt # remove
$ mkdir test_dir # make directory
$ rmdir test_dir # remove directory
$ 
$ # HOW TO VIEW FILES CONTENTS
$ cat agarwal.txt
$ less seasonal/spring.csv
$ head -n 10 seasonal/summer.csv # view 10 lines | "tail"
$ grep -c -i -n value seasonal/winter.csv # select lines containing specific values, -v inverting
$ head -n 5 seasonal/winter.csv > bottom.csv # storing output
$ tail -n 3 bottom.csv
$ head -n 5 seasonal/summer.csv | tail -n 3 # combining commands
$ cut -f 2  -d , seasonal/summer.csv | grep -v Tooth | sort -r | uniq -c 
$ cut -d , -f 1 seasonal/* # cut -d , -f 1 seasonal/*.csv
$ # ? one char, [97] chars inside, {s*.txt, *.csv} for comma seperated
$ egrep # regex matching
$ sed 's/foo/linux/g' file.txt # sed does patter match and replacement
$ history | tail -n 3 > steps.txt
$
$ set | grep HOME
$ echo $USER # get the variable
$ echo "print('Hello')" > hello.py
$ for filename in seasonal/*.csv; do echo $filename; done
$ for file in seasonal/*.csv; do head -n 2 $file | tail -n 1; done # many commands inside loop
$
$ nano dates.sh # write some shell commands
$ bash dates.sh
$ # 1. if dates.sh has "sort $@ | uniq", with $@ we can send specific files like "bash dates.sh summer.csv"
$ # 2. or even bash script may have "cut -d , -f $2 $1", then while running it use "bash column.sh seasonal/autumn.csv 1"
$ 
```

## Data processing in shell
**Downloading data on the command line with CURL and WGET**
```shell
$ curl -O https://websitename.com/datafilename.txt
$ curl -o renameddatafilename.txt https://websitename.com/datafilename.txt
$ curl -O https://websitename.com/datafilename*.txt # to get ALL txt file at one with *
$ curl -O https://websitename.com/datafilename[001-100:10].txt # download every 10th file from 1 till 100
$ curl -L -O -C https://websitename.com/datafilename[001-100].txt # -L redirect, -C resume previous file transfer 
$ # wget is good for multiple files
$ wget -i url_list.txt # --limit-rate=200k --wait=2
```
**Data cleaning on the command line** `csvkit`
```shell
$ pip install csvkit
$ in2csv data.xlsx > data.csv # converting files to CSV
$ in2csv -n data.xlsx # print sheet names
$ in2csv data.xlsx --sheet "Sheet 1" > data.csv
$ csvlook data.csv
$
$ csvcut -h # column
$ csvgrep -h # row, -m=manually, -r=regex, -f=path
$ csvcut -n data.csv # print names of columns
$ csvcut -c 1,2 data.csv # prints 1st and 2nd column OR [-c "column_name","column2_name"] without space between
$ csvgrep -c "danceability" -m 0.812 Spotify_MusicAttributes.csv
$
$ csvstack data1.csv data2.csv > data_new.csv
$ csv -g "Rank 1", "Rank 2" data1.csv data2.csv > data_new.csv # we will have new column, which will tell from which file the row come out
```
**Database Operations on the Command Line**
```shell
$ sql2csv --db "sqlite:///spotify.db" \
          --query "SELECT * FROM popularity" \
          > spotify_popularity.csv
$ csvsql --db "sqlite:///SpotifyDatabase.db" --insert Spotify_MusicAttributes.csv # Upload Spotify_MusicAttributes.csv to database
$ sqlquery="SELECT * FROM Spotify_MusicAttributes"
$ sql2csv --db "sqlite:///SpotifyDatabase.db" --query "$sqlquery" # Apply SQL query to re-pull new table in database
```
**CRON**
```shell
$ man crontab
$ crontab -l
$ # * * * * * minute, hour, day of month, month, day of week
$ # * * * * * means every minute of every hour of every day of every month and of every day of week
$ echo "* * * * * python hello_world.py" | crontab
$ # 5 1 * * * run every day at 1:05 am
$ # 15 14 * * 0 run at 2:15pm every Sunday
$ # */15 * * * * every 15 minute
$ # 15,30,45 * * * * at the 15, 30 and 45 minute of every hour
```

## Introduction to bash scripting
**From command-line to bash script**
```bash
$ cat two_cities.txt | egrep 'Sydney Carton|Charles Darnay' | wc -l
$ cat animals.txt | cut -d " " -f 2 | sort | uniq -c
```
```bash
#!/bin/bash
echo $1
echo $2
echo $@
echo "There are " $# "arguments"

# How to run? bash args.sh one two three four five

# Output:
# one
# two
# one two three four five
# There are 5 arguments
```
**Variables in bash**
```bash
hello='Rustam' # without space, prints what is inside

now_var_singlequote='$hello'
echo "Hello" $now_var_singlequote # Hello @hello

now_var_doublequote="$hello"
echo "Hello" $now_var_doublequote # Hello Rustam

rightnow_doublequote="The date is $(date)." # shell within shell
echo $rightnow_doublequot # The date is Mon 2 Dec 2019 14:13:35 AEDT
```
```bash
echo "2 + 2" | bc

temp_f=$1
temp_f2=$(echo "scale=2; $temp_f - 32" | bc)
temp_c=$(echo "scale=2; $temp_f2 * 5 / 9" | bc)

echo $temp_c

# How to run? bash script.sh 100
```
```bash
# Create three variables from the temp data files' contents
temp_a=$(cat temps/region_A)
temp_b=$(cat temps/region_B)
temp_c=$(cat temps/region_C)

# Print out the three variables
echo "The three temperatures were $temp_a, $temp_b, and $temp_c"
```
```bash
# Arrays
declare -a my_array
my_array=(1 2 3)
echo ${my_array[@]} # 1 2 3
echo ${#my_array[@]} # length
echo ${my_array[0]} # 1
echo ${my_array[@]:1:2} # 1 starting, 2 how many elements to return, so output will be 2 3
my_array+=(10) # appending

# Associative arrays -> python dict
declare -A city_details # declare
city_details=([city_name]="New York" [population]=14000000) # add elements
echo ${city_details[city_name]}
echo ${!city_details[@]} # keys
echo ${city_details[@]} # values
```
**Control statements in bash**
```bash
# Create variable from first ARGV element
sfile=$1

# Create an IF statement on sfile's contents
if grep -q 'SRVM_' $sfile && grep -q 'vpt' $sfile ; then
	# Move file if matched
	mv $sfile good_logs/
fi
```
```bash
for x in 1 2 3
do    
    echo $x
done

for ((x=2;x<=4;x+=2))
do     
    echo $x
done

for book in $(ls books/ | grep -i 'air')
do      
    echo $book
done
# AirportBook.txt
# FairMarketBook.txt


x=1
while [ $x -le 3 ];
do    
    echo $x    
    ((x+=1))
done
```
```bash
# CASE
# Use a FOR loop for each file in 'model_out/'
for file in model_out/*
do
    # Create a CASE statement for each file's contents
    case $(cat $file) in
      *"Random Forest"*|*GBM*|*XGBoost*) # Case
      mv $file tree_models/ ;;           # Command
      *KNN*|*Logistic*)                  # Case
      rm $file ;;                        # Command
      # Create a default
      *) 
      echo "Unknown model in $file" ;;
    esac
done
```
**Functions and automation**
```bash
# 1. Example
function hello_world () {
    echo "hello World"
}
hello_world # here we call the function

# 2. Example
function return_percentage () {
  percent=$(echo "scale=2; 100 * $1 / $2" | bc)
  # Return the calculated percentage
  echo $percent
}

# Call the function with 456 and 632 and echo the result
return_test=$(return_percentage 456 632)
echo "456 out of 632 as a percent is $return_test%"

# 3. Example
function sum_array () {
  local sum=0
  # Loop through, adding to base variable
  for number in "$@"
  do
    sum=$(echo "$sum + $number" | bc)
  done
  # Echo back the result
  echo $sum
  }
# Call function with array
test_array=(14 12 23.5 16 19.34)
total=$(sum_array "${test_array[@]}")
echo "The total sum of the test array is $total"
```
