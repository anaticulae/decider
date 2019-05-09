# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from typing import Tuple

from pytest import raises

from decider.feature import HOOK
from decider.feature import INPUT
from decider.feature import NAME
from decider.feature import OUTPUT
from decider.feature import create_step
from decider.feature import read_workplan


# pylint:disable=unused-argument
def workplan_workhook(input_a, input_b) -> Tuple[str, str, str]:
    pass


WORKPLAN = [
    {
        NAME: 'bordercontrol',
        INPUT: [
            ('groupme', 'chapter'),
            ('iamraw', 'toc'),
        ],
        OUTPUT: ('butter', 'tart', 'cream'),
        HOOK: workplan_workhook,
    },
    {
        NAME: 'worldcontrol',
        INPUT: [
            ('groupme', 'chapter'),
            ('iamraw', 'toc'),
        ],
        OUTPUT: ('butter', 'tart', 'cream'),
        HOOK: workplan_workhook,
    },
]


def test_create_workplan():
    workplan = [
        create_step(
            'bordercontrol',
            workplan_workhook,
            [
                ('groupme', 'chapter'),
                ('iamraw', 'toc'),
            ],
            ('butter', 'tart', 'cream'),
        ),
        create_step(
            'worldcontrol',
            workplan_workhook,
            [
                ('groupme', 'chapter'),
                ('iamraw', 'toc'),
            ],
            ('butter', 'tart', 'cream'),
        )
    ]
    assert workplan == WORKPLAN


def test_read_workplan(testdir):
    result = read_workplan(WORKPLAN, inspace=str(testdir), verify=False)
    assert len(result) == 2


def test_read_workplan_without_resources(testdir):
    with raises(SystemExit):
        read_workplan(WORKPLAN, inspace=str(testdir), verify=True)
