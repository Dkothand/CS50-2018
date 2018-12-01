# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

Considered one of the longest words in the English language, it refers to a lung disease caused by inhaling silica dust.

## According to its man page, what does `getrusage` do?

Returns the resource usage for the argument passed into getrusage(), usages are returned in a struct pointed to in second argument of getrusage.

## Per that same man page, how many members are in a variable of type `struct rusage`?

16, however not all fields will be filled. Unmaintained fields are set to zero.

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

By referencing 'before' and 'after' you are avoiding copying the entire struct to the stack and taking up unnecessary space on the stack.

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

'main' reads words from a file as follows. First, a 'for' loop is established using fgetc() to iterate through the characters in a file and stores them to variable c.

The loop continues until c is equal to the end of file. The loop increments by one character each pass by calling fgetc() on the file pointer a second time. A conditional statement is set up with if/else if statements.

The first condition checks if the current character c is an alphabetical character with function isalpha() OR if c is an apostrophe not at the beginning of a word. If true, c is added to array word and the index of which is incremented.

The index is then checked to see if the characters passed into array word do not exceed the maximum length a word can be established by LENGTH + 1. If the string is deemed too long to be a word, a 'while' loop runs the cursor through the rest of the string and the index is reset.

Next, if c does not fulfill the first conditional statement, it is checked with isdigit() to see if it is a number. If so the same 'while' loop is employed to run through the rest of the unnecessary alphanumberic string.

If c does not fulfill the first conditional statement and index shows we have characters stored in array word, then it is determined that we have reached the end of a word.

word[index] is then set to a NULL-terminator to end the word and index is reset to get ready for the next word and words counter is incremented.

Once a word has been identified, it is checked for spelling by passing it to check() which will return a bool value of False if misspelled. The time to check is measured and stored in struct rusage with getrusage().

If the word is misspelled, the word is printed to the terminal and misspellings counter is incremented. Index is then reset to zero to prepare for the next word.

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

'fscanf' can be used to read through words in the file. However if the word contains commas and periods fscanf will interpret them as part of the word when they might not be.

So after reading through a word, an extra step would need to be taken to iterate through the word checking for other characters.

Using fgetc() allows us to check for this character by character in the first step.

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

'const' serves to declare that the variable specified will not change size.

Ensures there won't be any modification by the functions calling them and adds a layer of protection from possible modification as the complier will now recognize and enforce the values as constant.
