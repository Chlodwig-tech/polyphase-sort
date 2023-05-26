An implementation of a polyphasic sorting algorithm for
sort sequential files. The algorithm has been implemented in version 2+1.
There are 1 phase of distribution and then phases of merging until complete
to sort the file.

The number of phases needed to sort a file (approximately) of r series at
'Fibonnaci distribution' is known at the beginning and is given by the formula:
1.45 log2(r).

The total number of disk operations (reads and writes) including distributions initial is approximately:
2N(1.04log2(r)+1)/b

The above formulas are more accurate the larger r is.
(Record draw - 44)
The records in the project consist of 6 numbers: a0, a1, a2, a3, a4, x
The average record size is 13B.
They are sorted according to the value of the g(x) function:
g(x) = a0 + a1^x + a2x^2 + a3x^3 + a4x^4


Files:

  generate_records.py - generates random records, is run from the command line with
  parameters – the file to which the randomized records are saved, and
  the second argument is the number of records to generate
  
  polyphase_sort.py - implements polyphase sort algorithm
 
  print_file.py - a program for printing a file with records and their corresponding values (debugging and checking tool
  sorting correctness)
  
  read.py - used to read records from file
  
  main.py - main program using programs generate_records,
  polyphase_sort and read. Used to sort the file. It is called from the line
  commands with the following parameters:
    
      -s source file path
      -d destination sorted file path
      -r read records from keyboard
      -debug print all records ant their values during each phase
      -ps defines the size of the page read from the file (the default value is 2kB)
      -sort t - ascending sort
      -sort f - descending sort
