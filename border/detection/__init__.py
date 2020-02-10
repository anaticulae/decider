# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

# TODO: MOVE THIS DETECTOR TO HEY PACKAGE LATER

# def border(page):

import iamraw

import border.detection.leftright
import border.detection.most


def determine_border(
        textpositions: iamraw.PageContentTextPositions,
        pagesizes: iamraw.PageSizeBorderList,
):
    most = border.detection.most.run(pagesizes)
    leftright = border.detection.leftright.run(textpositions, pagesizes)

    def border_detector(page: int):
        # left, right, top, down
        # TODO: CHECK THAT PAGE CALL IS CORRECT
        left = leftright.left
        if isinstance(left, tuple):
            left = left[page % 2]  # pylint:disable=E1136

        right = leftright.right
        if isinstance(right, tuple):
            right = right[page % 2]  # pylint:disable=E1136

        result = (left, right, most.top, most.bottom)
        return result

    return border_detector
