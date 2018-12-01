// Implements a dictionary's functionality

#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h" // Contains struct for loading dictionary into memory

#define ALPHABET 27 // Size of array for all values in dictionary

// Word count for dictionary loaded
unsigned int counter = 0;

// Structure for storing dictionary; trie
typedef struct node
{
    // Bool for checking if at the end of a word
    bool is_word;
    struct node *children[ALPHABET];
}
node;

node* root;

// Function to generate a new node in trie, sets elements in array to NULL and is_word to false.
node *new_node(void)
{
    node *get_node = NULL;
    get_node = malloc(sizeof(node));
    if (get_node)
    {
        get_node->is_word = false;
        for (int i = 0; i < ALPHABET; i++)
        {
            get_node->children[i] = NULL;
        }
    }
    return get_node;
}

// Function to convert character in dictionary to alphaetical index number
int index(char c)
{
    if (c == '\'')
    {
        return 26;
    }
    else if (c >= 'a' && c <= 'z')
    {
        return c - 'a';
    }
    else
    {
        return c - 'A';
    }
}

// Function to unload all nodes from memory
void free_all(node* travel)
{
    int i;
    for (i = 0; i < 27; i++)
    {
        if (travel->children[i] != NULL)
        {
            free_all(travel->children[i]);
        }
    }

    free(travel);
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int k;
    int length = strlen(word);
    node* travel = root;
    // for each letter in input word
    for (k = 0; k <= length; k++)
    {
        // Convert letter in word to alphabetical index
        int num = index(word[k]);

        // Checking if word exists once at end of word
        if (word[k] == '\0')
        {
            if (travel->is_word == true)
            {
                return true;
            }
            else
            {
                return false;
            }
        }
        // Checking if word exists in dictionary
        if (travel->children[num] == NULL)
        {
            // Word is misspelled
            return false;
        }
        // Move to next letter
        travel = travel->children[num];
    }
    return false;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Pointer to dictionary file
    FILE* dict_ptr = fopen(dictionary, "r");
    if (dict_ptr == NULL)
    {
        fprintf(stderr, "File not found\n");
        return false;
    }

    // Constructing root node and setting travel pointer
    root = new_node();
    node* travel = root;

    // Iterate through chars in dictionary, adding to trie nodes
    for (char c = fgetc(dict_ptr); c != EOF; c = fgetc(dict_ptr))
    {
        // Checking not at end of word
        if (c != '\n')
        {
            int num = index(c);
            // Creating node if pointer is NULL using new_node() function
            if (travel->children[num] == NULL)
            {
                travel->children[num] = new_node();
            }
            // Moving into node corresponding to index value
            travel = travel->children[num];
        }
        // Else we have found the end of a word
        else
        {
            // Mark end of word
            travel->is_word = true;
            // Increment global word counter
            counter++;
            // Move travel ptr to root node for next word
            travel = root;
        }
    }
    // Close file
    fclose(dict_ptr);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // Calls global variable counter
    return counter;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    node* travel = root;
    free_all(travel);
    return true;
}
