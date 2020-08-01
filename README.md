# csv_exercise

Python scripts that accept many files as a command line parameter and return (as an output) one column
list of numbers that exist in at least 75% of those files.

**Dependencies installation**
---

1. Install python3 interpreter [`python3`](https://www.python.org/)
2. It is recommended to create a virtual environment [`venv`](https://docs.python.org/3/library/venv.html)
3. In linux environments use:
    $ pip install -r requirements.txt
4. In windows environments use:
    $ pip install -r requirements-windows.txt

**Usage**
---

```
Usage: python csv_interpreter_dict_map.py test_files/file1.in test_files/file2.in test_files/file3.in test_files/file4.in
```


**Tools usage**
---

For testing purposes, the project has additional python scripts that will help to create more random csv files.
If you want to create random csv files use the tools/create_random_csv_files.py script as the following:

    $ cd tools
    $ python create_random_csv_files.py 50 100

The above command will create **50** files with **100** lines each: 
+ A folder named **random_csv_files**
+ A folder inside **random_csv_files**/random_csv_files_**0_50_100**
    - The **0** value of the folder indicates that the folder is the first created by the user. In the next execution, this number will be incremented by 1.
    - The **50** value of the folder indicates that the script has created **50** random files named file**1**.in, file**2**.in ... file**50**.in
    - The **100** value of the folder indicates that the script has created files that have ***100*** lines each

Also, the project counts with a script that helps to use this random csv files as parameters in a very easy way. (This script is also en the tools folder)

    $ python create_parameters.py 20

The above command will create:
+ A text file named parameters.txt with a single line with **20** paths of the file*.in files created with the create_random_files.py script.
This will help the user to simply copy the line in the file and then paste the string in the terminal.

    $ cd ..
    $ python csv_interpreter_dict_map.py python csv_interpreter_dict_map.py /home/jonathan/git/csv_exercise/tools/random_csv_files/random_csv_files_0_50_100/file46.in /home/jonathan/git/csv_exercise/tools/random_csv_files/random_csv_files_0_50_100/file1.in /home/jonathan/git/csv_exercise/tools/random_csv_files/random_csv_files_0_50_100/file25.in /home/jonathan/git/csv_exercise/tools/random_csv_files/random_csv_files_0_50_100/file40.in /home/jonathan/git/csv_exercise/tools/random_csv_files/random_csv_files_0_50_100/file24.in /home/jonathan/git/csv_exercise/tools/random_csv_files/random_csv_files_0_50_100/file6.in /home/jonathan/git/csv_exercise/tools/random_csv_files/random_csv_files_0_50_100/file20.in /home/jonathan/git/csv_exercise/tools/random_csv_files/random_csv_files_0_50_100/file50.in /home/jonathan/git/csv_exercise/tools/random_csv_files/random_csv_files_0_50_100/file8.in /home/jonathan/git/csv_exercise/tools/random_csv_files/random_csv_files_0_50_100/file44.in /home/jonathan/git/csv_exercise/tools/random_csv_files/random_csv_files_0_50_100/file19.in /home/jonathan/git/csv_exercise/tools/random_csv_files/random_csv_files_0_50_100/file32.in /home/jonathan/git/csv_exercise/tools/random_csv_files/random_csv_files_0_50_100/file39.in /home/jonathan/git/csv_exercise/tools/random_csv_files/random_csv_files_0_50_100/file28.in /home/jonathan/git/csv_exercise/tools/random_csv_files/random_csv_files_0_50_100/file42.in /home/jonathan/git/csv_exercise/tools/random_csv_files/random_csv_files_0_50_100/file11.in /home/jonathan/git/csv_exercise/tools/random_csv_files/random_csv_files_0_50_100/file21.in /home/jonathan/git/csv_exercise/tools/random_csv_files/random_csv_files_0_50_100/file49.in /home/jonathan/git/csv_exercise/tools/random_csv_files/random_csv_files_0_50_100/file48.in /home/jonathan/git/csv_exercise/tools/random_csv_files/random_csv_files_0_50_100/file15.in


For every execution of create_parameters.py file, it will append the new parameters in the next line of the file, in order to test with the same parameters and compare results or re-test some scenarios.

**Scripts for input files that might be several gigabytes in size**
---
The **csv_interpreter_dict_map.py** script works very fast with small files. It uses a python dictionary object to "map" the first columns of every csv file. With greater/big files the store of this dictionary in memory could represent a major issue.
In that manner, the project also has two approaches to handle this kind of files (big files with several gigabytes in size).


The **csv_interpreter_sqlite.py** script uses a sqlite3 database to handle the "map" of the numbers of the first columns. It is slower than the **csv_interpreter_dict_map.py** because it uses physical memory (the hard drive) to store the numbers in its tables, but it does not use the RAM memory for store any "map" variable.

The **csv_interpreter_files.py** script uses the file system to store the "map" using several files. It is slower than the **csv_interpreter_sqlite.py** and uses more physical storage. In every execution, it uses a temporary folder to store the multiple files that keep the track of the columns of the csv files.

On one hand, the **csv_interpreter_dict_map.py** can be quicker but with large files, it can exhaust the memory. The other two approaches are slower but both consume a lot of physical memory.  It will depend "where" these scripts are going to be executed and the types of csv files involved.

The scripts can be used in the same way as the **csv_interpreter_dict_map.py** script.

    $ python csv_interpreter_sqlite.py test_files/file1.in test_files/file2.in test_files/file3.in test_files/file4.in
    $ python csv_interpreter_files.py test_files/file1.in test_files/file2.in test_files/file3.in test_files/file4.in

