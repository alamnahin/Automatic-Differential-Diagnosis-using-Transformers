# -*- coding: utf-8 -*-
"""
@author: Adnan-Sadi
"""

import random

def get_adjacent_characters(char, word):
    """
    This function takes a character as input and returns a list of characters that are adjacent to the input character when
    considering the keyboard layout.
    
    args:
        char: a string containing a character
    returns:
        adj_char_list: a list containing the adjacent characters
    """
    adjacent_keys = {
        'a': ['q','w','s','x','z'],
        'b': ['v','g','h','n'],
        'c': ['x','d','f','v'],
        'd': ['s','e','r','f','c','x'],
        'e': ['w','s','d','r'],
        'f': ['d','r','t','g','v','c'],
        'g': ['f','t','y','h','b','v'],
        'h': ['g','y','u','j','n','b'],
        'i': ['u','j','k','o'],
        'j': ['h','u','i','k','n','m'],
        'k': ['j','i','o','l','m'],
        'l': ['k','o','p'],
        'm': ['n','j','k','l'],
        'n': ['b','h','j','m'],
        'o': ['i','k','l','p'],
        'p': ['o','l'],
        'q': ['w','a','s'],
        'r': ['e','d','f','t'],
        's': ['w','e','d','x','z','a'],
        't': ['r','f','g','y'],
        'u': ['y','h','j','i'],
        'v': ['c','f','g','v','b'],
        'w': ['q','a','s','e'],
        'x': ['z','s','d','c'],
        'y': ['t','g','h','u'],
        'z': ['a','s','x'],
    }
    try:
        adj_char_list = adjacent_keys[char]
    except KeyError:
        print(word)
    return adj_char_list

def replace_with_adjacent_char(word):
    """
    This function takes a word as an input and randomly replaces one of the characters of that word with an adjacent 
    character from the keyboard layout. It returns the new word with the inserted typo.
    
    args:
        word: a string containing a word
    returns:
        typo_word: a string containing the word after inserting the typo
    """
    
    if " " in word:
        raise Exception("The string can not contain spaces!")
        
    word = list(word)
    num_chars = len(word)
    
    if num_chars < 2:
        raise Exception("The word must contain atleast two characters!")
        
    # select a random character index
    char_idx = random.sample(range(0, num_chars),1)[0]
    char = word[char_idx]
    
    char_is_upper = char.isupper()
    # list of adjacent characters
    adj_char = get_adjacent_characters(char.lower(), word)
    
    replacement_char = random.choice(adj_char)
    # replace character
    word[char_idx] = replacement_char.upper() if char_is_upper == True else replacement_char
    typo_word = ''.join(word)
    
    return typo_word

def add_extra_adjacent_char(word):
    """
    This function randomly selects one of the characters of that word and adds an extra adjacent 
    character(from the keyboard layout) next to the selected character. It returns the new word with the inserted typo.
    
    args:
        word: a string containing a word
    returns:
        typo_word: a string containing the word after inserting the typo
    """
    
    if " " in word:
        raise Exception("The string can not contain spaces!")
        
    word = list(word)
    num_chars = len(word)
    
    if num_chars < 1:
        raise Exception("The input string can not be empty!")
        
    # select a random character index
    char_idx = random.sample(range(0, num_chars),1)[0]
    char = word[char_idx]
    
    # list of adjacent characters
    adj_char = get_adjacent_characters(char.lower(), word)
    
    extra_char = random.choice(adj_char)
    # insert extra character after the selected character
    word.insert(char_idx+1, extra_char)
    
    typo_word = ''.join(word)
    return typo_word

def swap_consecutive_chars(word):
    """
    This function randomly selects one of the characters of a word and then swaps with the next consecutive character in the
    that word. It returns the new word with the inserted typo.
    
    args:
        word: a string containing a word
    returns:
        typo_word: a string containing the word after inserting the typo
    """
    
    if " " in word:
        raise Exception("The string can not contain spaces!")

    word = list(word)
    num_chars = len(word)
    
    if num_chars < 2:
        raise Exception("The word must contain atleast two characters!")
    
    elif num_chars == 2:
        temp_word = []
        temp_word.append(word[1])
        temp_word.append(word[0])

        typo_word = ''.join(temp_word)
    else:
        # select a random character index. excludes the index of the last character.
        char_idx = random.sample(range(0, num_chars-1),1)[0]
        temp_char = word[char_idx]
        word[char_idx] = word[char_idx+1]
        word[char_idx+1] = temp_char

        typo_word = ''.join(word)

    return typo_word

def skip_char(word):
    """
    This function randomly selects one of the characters of a word and removes it from the word. 
    It returns the new word with the inserted typo.
    
    args:
        word: a string containing a word
    returns:
        typo_word: a string containing the word after inserting the typo
    """
    
    if " " in word:
        raise Exception("The string can not contain spaces!")
        
    word = list(word)
    num_chars = len(word)
    
    if num_chars < 2:
        raise Exception("The word must contain atleast two characters!")
        
    # select a random character index
    char_idx = random.sample(range(0, num_chars),1)[0]
    # removes the selected index from list
    word.pop(char_idx)
    
    typo_word = ''.join(word)
    return typo_word

def repeat_char(word):
    """
    This function randomly selects one of the characters of a word and repeats it by placing the same character next to 
    the selected character. It returns the new word with the inserted typo.
    
    args:
        word: a string containing a word
    returns:
        typo_word: a string containing the word after inserting the typo
    """
    
    if " " in word:
        raise Exception("The string can not contain spaces!")
        
    word = list(word)
    num_chars = len(word)
    
    if num_chars < 1:
        raise Exception("The input string can not be empty!")
        
    # select a random character index
    char_idx = random.sample(range(0, num_chars),1)[0]
    char = word[char_idx]
    # insert the same character in the next index
    word.insert(char_idx+1, char)
    
    typo_word = ''.join(word)
    return typo_word
