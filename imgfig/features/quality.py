# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import iamraw
import serializeraw
import utila


def work(*images: str, pages: tuple = None) -> typing.Tuple[str, str]:
    loaded = load_image_info(*images, pages=pages)
    return '', ''


def load_image_info(
        *images: str,
        pages: tuple = None,
) -> iamraw.ImageInformations:
    loaded = [serializeraw.load_image_info(item) for item in images]
    result = [
        item for item in loaded if not utila.should_skip(item.page, pages)
    ]
    return result
