'''
Created on May 29, 2014

Unit tests for merge_sort implementation in 'solutionA' module

@author: Eric Czech
'''
import unittest

import solutionA

class Test(unittest.TestCase):


    def validateMergeSort(self, list1, list2, expected):
        
        # Get results for both solutions (copy lists first)
        ideal_res = solutionA.merge_sort_ideal(
                list(list1) if not list1 is None else None, 
                list(list2) if not list2 is None else None
        )
        
        practical_res = solutionA.merge_sort_practical(
                list(list1) if not list1 is None else None, 
                list(list2) if not list2 is None else None
        )
        
        # Verify that the results from both methods are equal to the expected value
        self.assertEqual(ideal_res, expected)
        self.assertEqual(practical_res, expected)
        
        # Print the results of the case validation
        print 'Problem 2 - Solution A: Input list 1 = {}, Input list 2 = {}, Result = {}'\
            .format(list1, list2, ideal_res)
    
    def testSolutionA(self):
        # Edge cases for empty inputs
        self.validateMergeSort(None, None, [])
        self.validateMergeSort([], None, [])
        self.validateMergeSort(None, [], [])
        self.validateMergeSort([], [], [])
        
        # Test cases with two non-empty lists
        self.validateMergeSort(
            [ (2,1), (3,1) ],
            [ (1,1), (4,1) ],
            [ (1,1), (2,1), (3,1), (4,1) ]
        )
        self.validateMergeSort(
            [ (1,1), (1,1), (3,1), (7,1) ],
            [ (1,1), (2,1), (8,1), (9,1), (10,1) ],
            [ (1,1), (1,1), (1,1), (2,1), (3,1), (7,1), (8,1), (9,1), (10,1) ]
        )
        
        # Test cases with single empty lists
        self.validateMergeSort(
            [ (2,1), (3,1) ],
            [ ],
            [ (2,1), (3,1) ]
        )
        
        self.validateMergeSort(
            [ ],
            [ (2,1), (3,1) ],
            [ (2,1), (3,1) ]
        )
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()