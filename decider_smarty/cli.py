# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import decider_smarty

DESCRIPTION = ''

LINT_OUT = ('user', 'developer')

WORKPLAN = [
    utila.create_step(
        'badwords',
        inputs=[
            utila.ResultFile('smarty', 'badwords_invalid_prefix'),
            utila.ResultFile('smarty', 'badwords_phrases'),
            utila.ResultFile('smarty', 'badwords_pleonasms'),
            utila.ResultFile('words', 'word_result'),
            utila.ResultFile('words', 'headlines_headlines'),
        ],
        output=LINT_OUT,
    ),
]


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=decider_smarty.ROOT,
        featurepackage='decider_smarty.features',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=decider_smarty.PROCESS,
            pages=True,
            version=decider_smarty.__version__,
        ),
    )
