=======
dam_lev
=======

:Author: Daniel Walker
:Version: 0.1.0
:Date: 2022-11-24

Overview
========

The :code:`dam_lev` package implements the
`Damerau–Levenshtein diff algorithm <https://en.wikipedia.org/wiki/Damerau–Levenshtein_distance>`_.  That is,
it will take two sequences and determine the minimum number of transpositions, substitutions, insertions, and
deletions needed to transform the first sequence into the second.

Usage
=====

The package exposes a single function, :code:`dam_lev.get_changes`.  It takes two sequences (i.e., they must
implement the :code:`__len__` and :code:`__getitem__` methods) and returns a list of :code:`dam_lev.Mutation`
objects.  There are four subclasses of :code:`dam_lev.Mutation` corresponding to the four types of
transformations.  For example,

.. code-block:: python

    diffs = dam_lev.get_changes('abcdef', 'bcedxy')
    print(diffs) # [Deletion(at=0), Transposition(at=3), Substitution(at=5, at2=4), Insertion(at=6, at2=5)]

We see that the sequence of transformations is:

* Delete the item at index 0 (:code:`'a'`)
* Transpose the item at index 3 (:code:`'d'`) with its successor
* Substitute the item at index 5 (:code:`'f'`) with the item from the second sequence at index 4 (:code:`'x'`)
* Insert at index 6 the item from the second sequence at index 5 (:code:`'y'`)

Note the index for the transposition.  Even though, after the deletion, the :code:`'d'` is at index 2, it's at
index 3 in the original version of the sequence.  Likewise for the successive mutations.

Key function
------------

You can also pass a callable as the :code:`key` keyword argument to :code:`dam_lev.get_changes`.  Similar to
:code:`list.sort`, this callable will be used to compare the elements of the sequences.  For example,

.. code-block:: python

    diffs = dam_lev.get_changes('aBc', 'AbC', key=str.upper)
    print(diffs) # []
