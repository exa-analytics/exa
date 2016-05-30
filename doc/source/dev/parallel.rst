Parallelism and Scalability
##############################
In order to write high performance code, profiling must be done
continuously. Never make assumptions about the speed of a certain
algorithm. The following are some general guidelines that should
be followed when building code within the exa framework.

- minimize communication (MPI, CPU to GPU and back)
- multithreading and GPU processing are faster when the data size is >~5*10^5
- any function that can be threaded must release the GIL
- multithreading shares memory, multiprocessing does not
- sending and retrieving data to and from the GPU is costly; make the GPU do a lot of work and only return final result
- the above statement holds for multi-node processing as well
