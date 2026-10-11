# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protoerror
import serializeraw
import utilo


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
    loaded = utilo.flatten_content(loaded)
    result = []
    for image in loaded:
        if image.figure:
            # do not judge figures with decider_imgfig
            continue
        if not utilo.rect_width(image.bounding):
            utilo.error(f'skip zero-width image: {image.bounding}')
            continue
        if not utilo.rect_height(image.bounding):
            utilo.error(f'skip zero-height image: {image.bounding}')
            continue
        result.append(image)
    # create driver
    driver = protoerror.driver(
        images=result,
        contentborder=contentborder,
        docinfo=docinfo,
    )
    return driver
