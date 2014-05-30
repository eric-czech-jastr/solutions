'''
Created on May 29, 2014

Solutions for the following problem:

"A) You are given a large set of log files (k > 100) and each line of the file has a
timestamp and an error message. Each file has (n > 10000) lines. The lines in 
each file are sorted by timestamp in ascending order, naturally. 

The API for interacting with this data is the following (pseudo-code):
 
struct LogLine { 
 long timestamp; 
 String message; 
}
 
int getTotalNumberOfLogFiles(); 
int getTotalNumberOfLinesInFile(int k); 
List<LogLine> readAllLogLinesFromFile(k); 

The goal is to produce a single log file with the combined data from all the log 
files, sorted in ascending order, for example by calling an API: 

void appendLogLinesToOutput(List<LogLine> lines);"

@author: Eric Czech
'''
import heapq

class LogLine:
    """ Model class for individual log file entries """
    
    def __init__(self, timestamp, message):
        
        # Long value containing timestamp of message
        self.timestamp = timestamp
        
        # String value of message
        self.message = message
        
    def toTuple(self):
        return (self.timestamp, self.message)
    

class API:
    """ Log API class for fetching log file info and content """

    def getTotalNumberOfLogFiles(self):
        """ Returns total number of log files as an int """
    
    def getTotalNumberOfLinesInFile(self, k):
        """ Returns number of lines in kth log file """

    def readAllLogLinesFromFile(self, k):
        """ Returns all LogLine instances in kth log file """

    def appendLogLinesToOutput(self, lines):
        """ Appends all given LogLine instances to some output somewhere """


def merge_sort_practical(list1, list2):
    """ Same thing as 'merge_sort_ideal' using existing libraries """
    
    # Check some edge cases to avoid errors with heapq.merge
    if not list1:
        return list2 if list2 else []
    if not list2:
        return list1 if list1 else []
    
    return list(heapq.merge(list1, list2))

def merge_sort_ideal(list1, list2, key=lambda x: x[0]):
    """ Merges given *sorted* input lists of tuples, using the value provided    
    by the 'key' function in each tuple as the basis for comparison, and returns a single 
    list of sorted, resulting tuples.
        
    * Note that the results will be wrong if the input lists aren't already sorted
    
    * IMPORTANT: the items in the given list are consumed during the merge (to save memory),
      so do not attempt to use those lists after this call or copy them first
    
    Args:
        list1: first list of tuples to merge
        list2: second list of tuples to merge
        key: lambda function for fetching tuple element for comparison
    Returns:
        Single, sorted list of all tuples contained in both input lists 
    """ 
    
    result = []
    while list1 or list2:
        
        # If the first list is empty, pop one off the second until its empty too
        if not list1:
            result.append(list2.pop(0))
            continue
        
        # If the second list is empty, pop one off the first until its empty too
        if not list2:
            result.append(list1.pop(0))
            continue
        
        # Otherwise, pop an element of the list whose first element is smallest
        result.append(list1.pop(0) if key(list1[0]) <= key(list2[0]) else list2.pop(0))

    return result
    
def merge_sort(list1, list2):
    # Route to the custom merge sort implementation
    return merge_sort_ideal(list1, list2)

def merge_logs():
    
    # Get a magical api instance 
    api = API()
    
    # Figure out how many files there are to merge
    num_files = api.getTotalNumberOfLogFiles()
    
    # Sorted list of resulting log line tuples
    result = []
    
    # Add each file to the result (assume 1-based indexing for file numbers)
    for k in range(1, num_files+1):
        
        # Get all the log lines for this file as a list of tuples 
        # * Tuples have the form (timestamp, message)
        lines = [line.toTuple() for line in api.readAllLogLinesFromFile(k)]
        
        # Merge sort the current result and the given tuples
        # * This is only possible because the api returns the log lines already
        #   sorted by timestamp
        result = merge_sort(result, lines)
        
    # Finally, write the merged result to some output, first converting
    # each tuple back into a LongLine instance
    api.appendLogLinesToOutput([LogLine(t[0], t[1]) for t in result])

if __name__ == '__main__':
    merge_logs()