# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import serializeraw
import utila


def create(images, contentborder=None, docinfo=None, pages: tuple = None):
    if contentborder is not None:
        contentborder = serializeraw.load_pageborders(
            contentborder,
            pages=pages,
        )
    if docinfo is not None:
        docinfo = serializeraw.load_docinfo(docinfo, pages=pages)
    # skip_hidden: do not judge or analyze raw images which are part of
    # figures.
    loaded = serializeraw.load_image_infos_fromfiles(
        images,
        pages=pages,
        skip_hidden=True,
    )
    loaded = utila.flatten_content(loaded)
    result = []
    for image in loaded:
        if image.figure:
            # do not judge figures with decider_imgfig
            continue
        if not utila.rectangle_width(image.bounding):
            utila.error(f'skip zero-width image: {image.bounding}')
            continue
        if not utila.rectangle_height(image.bounding):
            utila.error(f'skip zero-height image: {image.bounding}')
            continue
        result.append(image)
    # create driver
    driver = protocol.driver(
        images=result,
        contentborder=contentborder,
        docinfo=docinfo,
    )
    return driver
