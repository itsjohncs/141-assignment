# CS 141 Final Project

## User Manual

Our program is straightforward to use. Navigate to the root of the project directory and execute the build script with `./build.sh`. You can now run `./run.py -h` to get a list of the available options (included below).

```
Usage: run.py [options] [DATABASE_FILE] [QUERY_FILE]

Finds organisms that are similar to the given organism in QUERY_FILE contained
in DATABSE_FILE.

Options:
  -n NUM_RESULTS, --num-results=NUM_RESULTS
                        The number of results to print out. Default is 10.
  -a, --print-alignment
                        If this flag is present, alignment information will be
                        print out in the results.
  --no-colors           If this flag is present, colors will not be used when
                        printing the alignment.
  -j NUM_JOBS, --num-jobs=NUM_JOBS
                        The number of organisms to process concurrently.
                        Default: 3
  --chunk-size=CHUNK_SIZE
                        The chunk size to use when processing large organisms.
                        Default: 200000
  -v, --verbose         May be specified twice. If specified once, INFO
                        messages and above are output. If specified twice,
                        DEBUG messages and above are output. By default, only
                        WARN messages and above are output.
  -q, --quiet           Only CRITICAL log messages will be output.
  -h, --help            show this help message and exit
```

Most of the interface is self-explanatory, however, the `--num-jobs` and `--chunk-size` options deserve special mention. These control the parallelization and memory-usage, respectively. Increasing the number of jobs will increase the amount of memory and processing power that is used and decreasing the chunk-size will decrease the amount of memory each job uses. Be careful when playing with these options as it is very easy for the program to grab all the memory on your system.

The output of the program without the `--print-alignment` flag is self-explanatory. When the alignment is printed however, you will be able to see the ideal alignment of the two strings with coloring between them to highlight gaps (yellow), matching characters (green), and mismatched characters (red). If `--no-colors` is given as well, gaps are shown as spaces, matching characters are shown as pipes, and mismatched characters are shown as X's.

## Algorithms

The algorithm used to determine the ideal alignment and score is Smith Waterman's algorithm and is implemented without any creative deviations. A matrix is created that is used like a lookup table to map out all possible alignments efficiently in `O(mn)` time.

Creating the alignments from the matrix after the ideal score is found is done via a straightforward algorithm that moves through the matrix according to rules laid out in the algorithm's description on Wikipedia. Each cell stores whether it represents as match, a deletion, or an insertion and once you find the cell with the largest score you can move backwards by making certain moves based on what action the cell represents.

Sorting at the end is done simply by using Python's native sorting algorithm. In addition, a priority queue is used to ensure that we don't store too many results as we go through the database. We did not implement any of the low-level sorting code because whatever we made in Python would be many, many times slower than the CPython's standard libraries implementations which are written in C.

## Design of the System

The project's design is straightforward and most of the logic should be easy to follow. The Python portion of the project is split up into various modules that are responsible for parsing the database, outputting results, and communicating with the C++ portion of the project. The `main.py` file drives the application and defines the flow in addition to managing the various worker processes.

The worker processes are spawned by various Python "threads" who collect the output from the processes and expose them to the rest of the application through a thread-safe queue.

The C++ portion of the project is a straightforward implementation of Smith Waterman's algorithm. When compiled, an executable file is created that accepts two strings from standard input, executes the algorithm on them, and then outputs the results to standard output.

This hybrid approach was chosen because Python gave us a lot of flexibility and power when creating the user interface, but proved to be too slow for the CPU bound algorithm. My experience with distributed systems made creating a multi-processor solution straightforward as well so I added that to give us a little more speed.

`bell.cs.ucr.edu` is capable of running my program on the small organisms file in ~10 seconds.
