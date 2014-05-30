'''
Created on May 29, 2014

Solutions for the following problem:

"A) Write a function where the input is a binary search tree of integers and the
output is the Nth-greatest value in the tree. The BST is defined by a root node 
and the property: every node on the right subtree has to be larger than the 
current node and every node on the left subtree has to be smaller (or equal) than 
the current node."

@author: Eric Czech
'''

class Node:
    
    def __init__(self, left, right, value):
        self.left = left
        self.right = right
        self.value = value

    def __str__(self):
        return self.to_string(0)
    
    def to_string(self, indent):
        left_node = '\n'+self.left.to_string(indent + 1) if self.left else None
        right_node = '\n'+self.right.to_string(indent + 1) if self.right else None
        
        return '{0}left = {2},\n{0}value = {1}\n{0}right = {3}'\
            .format('\t' * indent, self.value, left_node, right_node)
     
def findNthGreatestValueInBST(root, n):
    # Precondition root on being present
    if not root:
        return None
    
    # Precondition the search rank to being greater than 0 (indexing is 1-based) 
    if not n or n <= 0:
        return None
    
    node = traverse(root, n, [0])
    return node.value if node else None

def traverse(root, n, i): 
    
    if root.left is not None:
        result = traverse(root.left, n, i)
        if result: 
            return result 

    i[0] += 1
    if i[0] == n:
        return root 

    if root.right is not None:
        result = traverse(root.right, n, i)
        if result: 
            return result

    
    