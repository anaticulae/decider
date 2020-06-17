# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import textflow
import utila

import decider_textflow

DESCRIPTION = ''

CONTENT_INPUT = [
    utila.ResultFile('words', 'headlines_headlines'),
    utila.ResultFile('rawmaker', 'oneline_text_text'),
    utila.ResultFile('rawmaker', 'oneline_text_positions'),
    utila.ResultFile('rawmaker', 'border_pages'),
    utila.ResultFile('groupme', 'footer_footerheader'),
]

LINT_OUT = ('user', 'developer')

WORKPLAN = [
    utila.create_step(
        'lineending',
        inputs=[utila.ResultFile(textflow.PROCESS, 'lineending_lastchar')],
        output=LINT_OUT,
    ),
    utila.create_step(
        'paragraph',
        inputs=CONTENT_INPUT + [
            utila.ResultFile('doctextstyle', 'textstyle'),
            utila.ResultFile('magic', 'content_content'),
        ],
        output=LINT_OUT,
    ),
    utila.create_step(
        'quotation',
        inputs=[utila.ResultFile(textflow.PROCESS, 'quotation_quotation')],
        output=LINT_OUT,
    ),
    utila.create_step(
        'startend',
        inputs=CONTENT_INPUT,
        output=LINT_OUT,
    ),
    utila.create_step(
        'writing',
        inputs=CONTENT_INPUT,
        output=LINT_OUT,
    ),
]


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=decider_textflow.ROOT,
        featurepackage='decider_textflow.features',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            name=decider_textflow.PROCESS,
            pages=True,
            version=decider_textflow.__version__,
        ),
    )
