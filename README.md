# JASTR Coding Challenge Solutions

The python packages in this project contain solutions relevant to each of the 3 problems posed. 

Each package contains at least one module answering a subpart of some question, if that subpart called for some actually coding (all other answers are in this README).

Every module then has a companion set of unit tests to show example usage and verify that the solutions are correct (hopefully!).

Also, for most of the solutions I tried to include both a sort of "practical" way to solve the problem, as well as a more theoretically "ideal" (in space/time complexity) solution.  I've always thought that it's really important to be able to do both well, so hopefully I've pulled that off here.  Having two solutions was also convenient for unit testing where the results of a known library could be compared against my custom functions to make sure they're semantically correct (I do this frequently in a production setting too).

\* *Apologies for any style inconsistencies or weird idioms -- I'm much more of a java person but am trying to become pythonic on a production-worthy level ASAP.*

Solutions and Explanations:
* [Solution API](#solution-api)
* [Problem 1 - Frequency and consecutive item functions](#problem-1)
* [Problem 2 - Log merging](#problem-2)
* [Problem 3 - BST index search](#problem-3)

***
## Solution API

As a quicker, easier way to look at some of the results produced by the code answering these questions, I put some 
of the solutions behind a REST API.  I thought this would be easier than trying to make sure you have a compatible python environment with the source code in the project, in case you want to actually run anything.

I'll leave the explanations of each solution to the sections following, but as a quick reference, here's what's immediately available from the API:

* Querying for the item in a list with the largest number of consecutive appearances
    * http://ec2-50-112-200-1.us-west-2.compute.amazonaws.com:5000/most_consecutive/1,2,2,5,5,5,2,2
    * [http://ec2-50-112-200-1.us-west-2.compute.amazonaws.com:5000/most_consecutive/1,2,,,1,1,1 ,1 ,asdf,3,3](http://ec2-50-112-200-1.us-west-2.compute.amazonaws.com:5000/most_consecutive/1,2,,,1,1,1 ,1 ,asdf,3,3)
* Querying for the item in a list that occurs most frequently
    * http://ec2-50-112-200-1.us-west-2.compute.amazonaws.com:5000/most_frequent/1,2,2,5,5,5,2,2
    * http://ec2-50-112-200-1.us-west-2.compute.amazonaws.com:5000/most_frequent/1,2,1,2,2,3,1,1,1,1,1,asdf,3,2,3
* Merge-sorting two lists
    * http://ec2-50-112-200-1.us-west-2.compute.amazonaws.com:5000/merge_sort/?list1=1,3,5&list2=2,4,6
    * http://ec2-50-112-200-1.us-west-2.compute.amazonaws.com:5000/merge_sort/?list1=0,1,2,3,4&list2=1,3,6,8
    * http://ec2-50-112-200-1.us-west-2.compute.amazonaws.com:5000/merge_sort/?list1=1,kdl,3,5&list2=2,asdf,,,4,6
    
The API is deployed on a free-tier, micro AWS instance.  You gotta love AWS -- it's awesome being able to do this for free!

The source code for the API server is here, in case you're interested: [api/server.py](/jastr/api/server.py)

***
## Problem 1

##### Part A)  Consecutive elements


> Q: Write a function where the input is an array of integers and the output is the value that 
> appears the most times consecutively (in a row). Ex: [1, 2, 2, 5, 5, 5, 2, 2] => 5


Solutions in : [problem1/solutionA.py](/problem1/solutionA.py)

Unit tests in: [problem1/solutionA_test.py](/problem1/solutionA_test.py)  (Executable via a main method)


A "practical" solution to this problem, like this:

```
# arr is input element array
grouped = [(k, sum(1 for _ in g)) for k,g in groupby(arr)]
return nlargest(1, grouped, key=lambda x: x[1])[0]
```

would usually run with a computational complexity of **O(n log(n))** (due to sorting) and a storage complexity of **O(n)**.  That's not great but I'd always prefer a solution like this due to its simplicity unless there was a really good reason not to.  

Assuming there is a good reason to write a more optimal, custom solution like the one I gave, then you can shrink those complexities down to **O(n)** runtime, **O(1)** storage.

##### Part B)  Most Frequent Elements

> Q: Write a function where the input is an array of integers and the output is the value that
> appears most frequently. Ex: [1, 2, 2, 5, 5, 5, 2, 2] => 2


Solutions  ==> [problem1/solutionB.py](/problem1/solutionB.py)

Unit tests ==> [problem1/solutionB_test.py](/problem1/solutionB_test.py)  (Executable via a main method)


A "practical" solution to this problem, like this:

```
# arr is input element array
result = collections.Counter(arr).most_common(1)
return result[0] if result else None
```

would usually run with a computational complexity of **O(n)** and a storage complexity of **O(n)**.  This makes sense because the most naive solution just involves computing a histogram of element counts and then finding the value with the maximum number of occurrences in that histogram after adding everything to it (max functions run in linear time).

In extreme cases where the number of items is really big, the solution I proposed makes some tradeoffs between time and space complexity.  The solution includes a parameter, *c*, used to manipulate that tradeoff on a continuous spectrum.  I think this kind of control is incredibly important for real-world applications like this where the *real* problem isn't getting the space complexity down, it's getting things to work either completely in memory or with a combination of memory and **sequential** disk I/O.  In other words, I'll take an algorithm with **O(n^2)** space complexity over one with **O(n)** any day if **n** is to big too fit in memory anyways, and the former allows for sequential I/O in and out of memory while the latter doesn't (i.e. random I/O required).  The performance between these two I/O methods differs by approximately two orders of magnitude, so the exponents of the space complexities would have to be at least that different before sequential algorithms using more space would *actually* take longer. 

Anyways, the solution I proposed would only ever involve sequential I/O in and out of RAM and would also allow, at least to some extent, for a trade off to be made between space and time to try to fit as much in memory as possible before spilling anything to disk (or a network).

The computational complexity of the solution is **O( n^( 1 + *c* ) )**, where *c* is between 0 and .5.  The storage complexity, **O( n^( 1 - *c* ) + n^*c* )**, is also a function of *c* minimized at *c* = .5.  This means that the best this solution can do to save space is to reduce the storage complexity to **O(sqrt(n))**, at the expense of an increased runtime complexity of **O( n ^ (3/2) )**.  At the opposite end of the spectrum when *c* = 0, the runtime and storage complexities are both **O(n)**, and the implementation becomes essentially identical to the naive histogram approach I mentioned above.

I tried to think of possibilities for techniques requiring only log(n) space or constant space but came up blank.  Is there such a thing?  Now I'm really curious what the best theoretical solutions are (I've been religiously avoiding google on the off chance I come up with something decent on my own).


***
## Problem 2

> Q: You are given a large set of log files (k > 100) and each line of the file has a
> timestamp and an error message. Each file has (n > 10000) lines. The lines in 
> each file are sorted by timestamp in ascending order, naturally. 
> 
> The goal is to produce a single log file with the combined data from all the log 
> files, sorted in ascending order.

##### Part A)  Merging the logs with the given API

Solutions in : [problem2/solutionA.py](/problem2/solutionA.py)

Unit tests in: [problem2/solutionA_test.py](/problem2/solutionA_test.py)  (Executable via a main method)

The solution gives a way to merge the logs using the provided API as well as a custom merge sort implementation.  The unit tests only cover the merge sort routine though because it seemed like recognizing the opportunity to use it along with spotting the deficiencies in the given API were the real goal of the exercise (i.e. acutally testing some log file merges didn't seem worth the time it would take to do it).

Nevertheless, the solution pulls and sorts all the entries in memory using **O(n)** space before writing it to some final, sorted output stream.  I'd imagine that in a real-world scenario the timestamp ranges within each log file might mutually exclusive (or at least *mostly* different) so if I had more time, I would have probably tried some different heuristics to figure out if it was possible to consider merging and outputting subsets of log entries in the files instead of pulling the whole dataset into memory.  That might potentially help, depending on the data, but the asymptotic space complexity would still be the same (**O(n)**).  Whether or not any heuristics like that were used, the time complexity would still be **O(n)** as well since the log entries from each file were already sorted.


##### Part C)  Dealing with a larger-than-memory dataset using the given API

> Q: What if the full set of data could not all fit in memory (e.g. k > 1000, n >
> 1000000)? Given this constraint, is it possible to solve this problem with only the 
> API you’ve been given?

If all the log entries from the *largest* log file didn't fit in memory, then I'd say that it isn't possible to answer this question without some serious hacking.  One thing you could do though (I know it's possible in java), is change the way that a "List" works such that it doesn't really load things into memory but rather buffer it to/from disk.  That would be pretty involved though so practically speaking, it would probably just be smarter to pursue getting the API changed to use more scalable data structures.

However, if all the log entries from the largest log file *do* fit in memory, then you could simply buffer the entries from each file to disk and then read them back out using proper iterators (or some other structure that's less aggressive with memory usage).

> Q: Assuming you could change the interface/implementation of the API, 
> what would you modify to make the solution easier?

I don't think much would need to change other than that the log entries should be streamed/iterated instead of placed into a completely in-memory collection of some kind.

If that was the case, then it would be pretty straightforward to do a k-way merge across iterators for all the log files and write individual entries from the sorted stream to the output.  The time complexity would still be **O(n)** but the space complexity would only be **O(1)** -- a huge improvement, especially with log files which are usually larger than the memory available.

***
## Problem 3

> Q: Write a function where the input is a binary search tree of integers and the
> output is the Nth-greatest value in the tree. The BST is defined by a root node 
> and the property: every node on the right subtree has to be larger than the
> current node and every node on the left subtree has to be smaller (or equal) than 
> the current node.

##### Part A)  Find the Nth element in a BST

Solutions in : [problem3/solutionA.py](/problem3/solutionA.py)

Unit tests in: [problem3/solutionA_test.py](/problem3/solutionA_test.py)  (Executable via a main method)

I stared at this for a long time and then ultimately decided I didn't think it was possible in sub-linear time/space since it doesn't seem feasible to find a ranked element in a BST that you don't know the size of without potentially traversing it.  I have a sneaking suspicion that some googling might prove me wrong in like 2 seconds, but in the interest of fairness, I just went ahead with an in-order traversal instead since I couldn't think of anything better.

The solution I put together though works by moving recursively, depth-first, and left-first throughout the tree to enumerate the nodes in order from least to greatest.  Starting with the node having the smallest value, a counter is incremented within the traversal until **N** nodes are encountered, at which point the value for that node is returned.

The space and time complexity for this approach are both **O(|E| + |V|)**.
