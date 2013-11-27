# CS 141 Progress Report

## Strategy

### Alignment Algorithm

We plan to use a modified edit distance algorithm to find the optimal alignment score, using a table to hold alignment scores at given indeces of the input strings.  The table is then backtraced through to find the path of maximum scores, whose indeces are used to determine where an insertion, deletion, or substitution needs to occur.  The backtraced process is then used to construct the aligned string, which has insertions, deletions, and substitutions matching those from the backtrace.  

To compute gap penalties and substitution penalties for substrings, the algorithm we use will track gap sizes and call functions defining penalties for given gaps and another function defining penalties for given character subtitutions.  

### Sorting Algorithm

We plan to use the built-in Python `sort()` function as it is extremely unlikely that we can create an implementation in Python that would outperform the finely tuned, compiled code that `sort()` uses. The algorithm that `sort()` uses is called timsmort and is detailed in [this blog post](http://www.hatfulofhollow.com/posts/code/timsort/index.html).

## Dividing Work

In order to divide the work we first seperated the assignment into discrete tasks. We defined several interfaces and contracts that would allow meaningful work on pieces of code that depend on other (as of yet unfinished) pieces of code.

The GitHub issue tracker is being used to keep track of these tasks.

**Breakdown of who is doing what needed here.**

## What you have accomplished to date

**Should be completed shortly before submission.**
