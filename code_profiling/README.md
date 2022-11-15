# Code Profiling: the TL;DR 

## What is it?

At its highest level, code profiling is the exercise of interrogating code to ensure that it is optimised. You may measure space (memory) or the time complexity of a program. 

To estimate times for especially long processes, it can be helpful to prototype a program on a smaller sample and estimate the running time for the full set. 

Remember:
1. Run times are not always linear esp. with data with higher dimensions 

2.  Order of data can have an impact.

3. Find the right trade off between invoking overheads (i.e. loading lookups, preparing data for parallel processing) and your code run time. 

## So what?

It's good to optimise code so...

* ...it doesn't take forever to run a program
* ...you can write higher quality code 
* ...you have a more informed sense of when you should take advantage of i.e. GPUs 

## Libraries 

Some tools to profile code run times include: using Python's inbuilt `time` or `timeit`. 

You can also pip install `line_profiler` to identify which parts of your code are taking the longest. 