HHLtools
========

HHLtools is a small collection of Python utilities for algorithms, data
structures, debugging, terminal output, and basic mathematics.

Requirements
------------

HHLtools requires Python 3.10 or later.

Installation
------------

Install the package from PyPI:

.. code-block:: console

   python -m pip install hhltools

To install the current checkout for development:

.. code-block:: console

   python -m pip install -e .

Quick start
-----------

Algorithms
~~~~~~~~~~

``binary_search`` returns the index of a value in an ascending, sorted
sequence, or ``-1`` when the value is absent:

.. code-block:: python

   from HHLtools.algorithm import binary_search

   index = binary_search([1, 3, 5, 7], 5)
   assert index == 2

Data structures
~~~~~~~~~~~~~~~

Queues and stacks can be bounded or unbounded:

.. code-block:: python

   from HHLtools.data_structure import Queue, Stack

   queue = Queue()
   queue.push("first")
   queue.push("second")
   assert queue.pop() == "first"

   stack = Stack()
   stack.push("first")
   stack.push("second")
   assert stack.pop() == "second"

``Array`` supports explicit, inclusive bounds and runtime element-type
checking:

.. code-block:: python

   from HHLtools.data_structure import Array

   matrix = Array[1:2, 1:3] @ int
   matrix[1, 1] = 42
   assert matrix[1, 1] == 42

Debugging
~~~~~~~~~

Use ``print_obj`` to inspect nested object attributes as a tree:

.. code-block:: python

   from HHLtools.debug import print_obj

   print_obj({"status": "ready"})

Package modules
---------------

``algorithm``
   General-purpose algorithms.

``chinese``
   Chinese aliases for selected Python built-ins and constants.

``clstools``
   Class decorators and runtime class utilities.

``data_structure``
   Queues, stacks, linked lists, and typed multidimensional arrays.

``debug``
   Call-stack and object-inspection helpers.

``error``
   Exception-reporting helpers and package-specific exceptions.

``math``
   Helpers for functions, vectors, and three-dimensional lines.

``prettyprint``
   ANSI terminal formatting and tree-display constants.

``utils``
   Shared type-inspection helpers.

Version history
---------------

2.1.1 (2026-09-05)
   Refactored parts of the package.

2.1.0 (2026-09-05)
   Added ``Array``.

2.0.2 (2026-09-04)
   Added recursive-reference detection to ``print_obj``.

2.0.1 (2026-09-04)
   Fixed minor bugs.

2.0.0 (2026-09-04)
   Expanded the debugging tools and documentation.

Earlier releases
~~~~~~~~~~~~~~~~

* 1.2.7 (2026-09-03): Fixed bugs.
* 1.2.6 (2026-02-12): Fixed bugs in ``prints``.
* 1.2.2--1.2.4 (2023-12-20): Fixed bugs.
* 1.2.1 (2023-04-22): Fixed bugs and removed ``fibonacci``.
* 1.2.0 (2023-04-22): Added ``Vector`` and improved error reporting.
* 1.1.0 (2023-04-21): Added linked lists and updated existing functions.
* 1.0.7--1.0.8.1 (2022-10-28 to 2022-11-04): Added ``prints`` and the
  Chinese aliases, enabled Python 3.11, and fixed bugs.
* 1.0.4--1.0.6 (2022-09-17 to 2022-10-02): Added stacks, queues, and
  mathematical helpers, and fixed bugs.
* 1.0.0--1.0.3 (2022-08-07): Initial releases.

License
-------

HHLtools is distributed under the MIT License. See ``LICENSE.txt`` for
details.
