# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import textflow
import utila

import decider_textflow

DESCRIPTION = ''

CONTENT_INPUT = [
    utila.ResultFile('words', 'headlines_oneline'),
    utila.ResultFile('rawmaker', 'oneline_text_text'),
    utila.ResultFile('rawmaker', 'oneline_text_positions'),
    utila.ResultFile('rawmaker', 'border_pages'),
    utila.ResultFile('groupme', 'footer_footerheader'),
]

LINT_OUT = ('user', 'developer')

WORKPLAN = [
    utila.create_step(
        'character',
        inputs=CONTENT_INPUT + [utila.ResultFile('magic', 'content_content')],
        output=LINT_OUT,
    ),
    utila.create_step(
        'docref',
        inputs=[
            utila.ResultFile('docref', 'figure_parsed'),
            utila.ResultFile('docref', 'section_parsed'),
            utila.ResultFile('docref', 'table_parsed'),
            utila.ResultFile('caption', 'figure_caption'),
            utila.ResultFile('caption', 'image_caption'),
            utila.ResultFile('caption', 'table_caption'),
            utila.ResultFile('words', 'text_text'),
            utila.ResultFile('words', 'headlines_headlines'),
        ],
        output=LINT_OUT,
    ),
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
        'physical',
        inputs=CONTENT_INPUT + [
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
        inputs=CONTENT_INPUT + [
            utila.ResultFile('magic', 'content_content'),
        ],
        output=LINT_OUT,
    ),
    utila.create_step(
        'writing',
        inputs=CONTENT_INPUT + [
            utila.ResultFile('magic', 'content_content'),
        ],
        output=LINT_OUT,
    ),
]


def main():
    root, features = decider_textflow.ROOT, 'decider_textflow.features'
    hook = protocol.integrate(root=root, features=features)
    utila.featurepack(
        workplan=WORKPLAN,
        root=root,
        featurepackage=features,
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            cli_hook=hook,
            multiprocessed=True,
            name=decider_textflow.PROCESS,
            pages=True,
            version=decider_textflow.__version__,
        ),
    )
