#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================
"""Decider
=======

Decider judges different features based on previous feature extraction.

Currently `decider` supports to validate:

- :ref:`decider_features_footnote`
- :ref:`decider_features_header`
- :ref:`decider_features_page`
- :ref:`decider_features_titlepage`
- :ref:`decider_features_toc`

There are two different definition of **Solution IDs**. The internal one
uses only numbers, the external Solution IDs which span over different
applications contains a Letter for program name and one till two letters
to describe the used feature. To sort Soluton IDs it is required to use
the lower described **Ranges**.

Solution IDs
------------
.. code-block:: none

    - border       B    B0000   -  B5999
    - decider      D
        + footnote      DF0000  -  DF5999
        + header        DH0000  -  DH5999
        + page          DP0000  -  DP5999
        + titlepage     DTI1000 -  DTI5999
        + toc           DTO1000 -  DTO5999
    - fonts             F0000   -  F5999

Ranges
------

.. code-block:: none

    Reserved:       0    - 499
    Fatal:          500  - 999
    Error:          1000 - 1999
    Warnings:       2000 - 2999
    Convention:     3000 - 3999
    Refactor:       4000 - 4999
    Info:           5000 - 5999


.. note:: see `protocol` for more information.
"""

import os

__version__ = '0.11.3'

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# public API for further processing steps to gather correct file names and
# configuration.
# pylint:disable=wrong-import-position

PACKAGE = 'decider'
PROCESS = 'decider'

from decider.cli import DEVELOPER_LINT_OUTPUT  # isort:skip
from decider.cli import USER_LINT_OUTPUT  # isort:skip
