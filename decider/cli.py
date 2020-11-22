#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import detector
import detector.cli
import groupme
import groupme.cli
import utila
import words

import decider

DESCRIPTION = ''

TOC = 'toc'
FOOTNOTE = 'footnote'

USER = 'user'
DEVELOPER = 'developer'

WORKPLAN = [
    utila.create_step(
        'abbreviation_table',
        [
            utila.ResultFile(groupme.PROCESS, 'abbreviation_abbreviation'),
        ],
        (USER, DEVELOPER),
    ),
    utila.create_step(
        'abbreviation_text',
        [
            utila.ResultFile(groupme.PROCESS, 'abbreviation_abbreviation'),
            utila.ResultFile(words.PROCESS, 'abbreviation_detected'),
        ],
        (USER, DEVELOPER),
    ),
    utila.create_step(
        'bibliography',
        [
            utila.ResultFile(detector.PROCESS, 'bibliography_detected'),
        ],
        (USER, DEVELOPER),
    ),
    utila.create_step(
        'header',
        [
            utila.ResultFile('groupme', 'footer_footerheader'),
        ],
        (USER, DEVELOPER),
    ),
    utila.create_step(
        'links',
        [
            utila.ResultFile('words', 'links_links'),
        ],
        (USER, DEVELOPER),
    ),
    utila.create_step(
        'page',
        [
            utila.ResultFile('groupme', 'footer_footerheader'),
        ],
        (USER, DEVELOPER),
    ),
    utila.create_step(
        'titlepage',
        [
            utila.ResultFile(detector.PROCESS, 'titlepage_detected'),
        ],
        (USER, DEVELOPER),
    ),
]

USER_LINT_OUTPUT = f'{decider.PROCESS}__titlepage_{USER}.yaml'
DEVELOPER_LINT_OUTPUT = f'{decider.PROCESS}__titlepage_{DEVELOPER}.yaml'


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=decider.ROOT,
        featurepackage='decider.features',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=decider.PROCESS,
            version=decider.__version__,
        ),
    )
