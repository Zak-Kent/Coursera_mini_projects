"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

#import user41_cymI9racho_8 as zk 

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    output = [] 
    for item in list1: 
        if item not in output: 
            output.append(item) 
    return output
         
def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    output = []   
    for item in list1: 
        if item in list1 and item in list2: 
            output.append(item)
    return output

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """
    # creates a copy of lists to avoid mutating originals 
    output = [] 
    copy1 = list1[:]
    copy2 = list2[:]
    
    # while there is something in copy1/2 pop the smaller element at idx
    # append the smaller to output 
    while copy1 and copy2: 
        if copy1[0] < copy2[0]:
            output.append(copy1.pop(0))
        else: 
            output.append(copy2.pop(0))
    
    #once the while loop is over add left over elements from comparison 
    output += copy1 + copy2 
    
    return output

def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    
    if list1 == []:
        return list1
    else:
        pivot = list1[0]
        lesser = [number for number in list1 if number < pivot]
        pivots = [number for number in list1 if number == pivot]
        greater = [number for number in list1 if number > pivot]
        return merge_sort(lesser) + pivots + merge_sort(greater)
      

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    permutations = []
    
    if len(word) == 1: 
        permutations = [word]
    else: 
        for idx, letter in enumerate(word): 
            # index slices below remove the letter in the loop above from word
            # ex. if letter is 'h' in 'hello' slices call func on 'ello' and 
            # then if letter is 'e' you get 'hllo' with func call 
            for perm in gen_all_strings(word[:idx] + word[idx+1:]):
                permutations += [letter + perm] 
    
    # I'm appending empty string way too many times. However if I add it to base case 
    # it ends up getting left out of final answer 
    permutations.append('')
    return permutations 

#zk.run_suite(gen_all_strings)

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    return []

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()

    
    
