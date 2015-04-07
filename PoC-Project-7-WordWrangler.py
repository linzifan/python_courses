"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    res = []
    for item in list1:
        if item not in res:
            res.append(item)
    return res

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    res = []
    for item in list1:
        if item in list2 and item not in res:
            res.append(item)
    return res

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """  
    res = []
    lst1, lst2 = list1[:], list2[:]
    while len(lst1) > 0 and len(lst2) > 0:
        if lst1[0] < lst2[0]:
            res.append(lst1[0])
            lst1.pop(0)
        else:
            res.append(lst2[0])
            lst2.pop(0)
    if len(lst1) > 0:
        res += lst1
    else:
        res += lst2
    return res
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    half_ind = len(list1) / 2
    return merge(merge_sort(list1[:half_ind]), merge_sort(list1[half_ind:]))
    

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return [""]
    first = word[0]
    rest = word[1:]
    rest_strings = gen_all_strings(rest)
    answer = []
    for item in rest_strings:
        for ind in range(len(item) + 1):
            answer.append(item[:ind] + first + item[ind:])
    return rest_strings + answer

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

    
    

