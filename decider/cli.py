#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import groupme
import groupme.cli
import protocol
import utila
import words

import decider

DESCRIPTION = ''

TOC = 'toc'
FOOTNOTE = 'footnote'

WORKPLAN = [
    utila.create_step(
        'abbreviation_text',
        [
            utila.ResultFile(groupme.PROCESS, 'abbreviation_abbreviation'),
            utila.ResultFile(words.PROCESS, 'abbreviation_detected'),
        ],
        protocol.ResultDefault,
    ),
    utila.create_step(
        'color',
        [
            utila.ResultFile('color', 'statistics_statistics'),
        ],
        protocol.ResultDefault,
    ),
    utila.create_step(
        'header',
        [
            utila.ResultFile('groupme', 'footer_footerheader'),
        ],
        protocol.ResultDefault,
    ),
    utila.create_step(
        'links',
        [
            utila.ResultFile('weblink', 'biblio_biblio'),
            utila.ResultFile('weblink', 'footer_footer'),
            utila.ResultFile('weblink', 'sentence_sentence'),
        ],
        protocol.ResultDefault,
    ),
    utila.create_step(
        'page',
        [
            utila.ResultFile('groupme', 'footer_footerheader'),
        ],
        protocol.ResultDefault,
    ),
    utila.create_step(
        'titlepage',
        [
            utila.ResultFile('detector', 'titlepage_detected'),
        ],
        protocol.ResultDefault,
    ),
]

USER_LINT_OUTPUT = f'{decider.PROCESS}__titlepage_user.yaml'
DEVELOPER_LINT_OUTPUT = f'{decider.PROCESS}__titlepage_developer.yaml'


def main():
    hook = protocol.integrate(root=decider.ROOT, features='decider.features')
    utila.featurepack(
        workplan=WORKPLAN,
        root=decider.ROOT,
        featurepackage='decider.features',
        config=utila.FeaturePackConfig(
            cli_hook=hook,
            description=DESCRIPTION,
            multiprocessed=True,
            name=decider.PROCESS,
            pages=True,
            version=decider.__version__,
        ),
    )
