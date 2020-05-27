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

WORKPLAN = [
    utila.create_step(
        'lineending',
        inputs=[utila.ResultFile(textflow.PROCESS, 'lineending_lastchar')],
        output=('user', 'developer'),
    ),
    utila.create_step(
        'quotation',
        inputs=[utila.ResultFile(textflow.PROCESS, 'quotation_quotation')],
        output=('user', 'developer'),
    ),
    utila.create_step(
        'writing',
        inputs=[
            utila.ResultFile('words', 'headlines_headlines'),
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
        ],
        output=('user', 'developer'),
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
