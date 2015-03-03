# ExternalSort
A small module to do external sort. 

Assumptions:

1. All the files that are to be merged into a single file and sorted are small enough to be loaded into the RAM. 
2. All the files to be sorted have numbers separated by newline characters


How to use it:
1. Put it in a folder in which all the files to be sorted are placed.
2. Import this file as a module.The commands to be executed are
      import ExternalSort
        
      sorter=ExternalSort(<name of the output file>)
      sorter.sort()

