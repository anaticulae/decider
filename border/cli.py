#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila

import decider

PROCESS = 'decider_border'

FEATURE_NAME = 'detection'
DESCRIPTION = """\
The border_decider detects overlapping content to different extracted
border. There are four types of border.

1. The crop-border which contains the every element in the document.
2. The left-right border describes the border in books which is different
   for the left page and the right page.
3. The page border excludes page number on the bottom of the page.
4. The footer border excludes the area of the footer.
"""

WORKPLAN = [
    utila.create_step(
        FEATURE_NAME,
        [
            utila.ResultFile('rawmaker', 'border_boundingboxes'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('rawmaker', 'text_positions'),
        ],
        ('hits', 'user', 'developer'),
    )
]


def main():
    ret = utila.featurepack(
        description=DESCRIPTION,
        featurepackage='border.features',
        name=PROCESS,
        pages=True,
        root=decider.ROOT,
        version=decider.__version__,
        workplan=WORKPLAN,
    )
    return ret
