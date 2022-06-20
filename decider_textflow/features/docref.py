# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import serializeraw

import decider_textflow.docref.basic


def work(  # pylint:disable=W0613
    ref_figure: str,
    ref_section: str,
    ref_table: str,
    caption_image: str,
    caption_table: str,
    text: str,
    headlines: str,
    pages: tuple = None,
) -> protocol.ResultType:
    driver = create_driver(**locals())
    result = protocol.run(
        modulename=[
            decider_textflow.docref.basic,
        ],
        driver=driver,
    )
    return result


def create_driver(
    ref_figure: str,
    ref_section: str,
    ref_table: str,
    caption_image: str,
    caption_table: str,
    text: str,
    headlines: str,
    pages: tuple = None,
) -> 'Driver':
    ref_figure = serializeraw.load_docref(ref_figure, pages=pages)
    ref_section = serializeraw.load_docref(ref_section, pages=pages)
    ref_table = serializeraw.load_docref(ref_table, pages=pages)
    headlines = serializeraw.load_headlines(headlines, pages=pages)
    text = serializeraw.load_text(text, headlines=headlines, pages=pages)
    caption_image = serializeraw.load_captions(caption_image, pages=pages)
    caption_table = serializeraw.load_captions(caption_table, pages=pages)
    # prepare
    driver = protocol.driver(
        ref_figure=ref_figure,
        ref_section=ref_section,
        ref_table=ref_table,
        headlines=headlines,
        text=text,
        caption_image=caption_image,
        caption_table=caption_table,
    )
    return driver
