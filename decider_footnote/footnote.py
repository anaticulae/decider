# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Footnotes
=========

* Every note is a sentence.
* The note starts with an upper case.
* and ends with a Dot.
* An exception is a http-url

[Wissenschaftliches Schreiben - Manuel Rene Theisen: page 202]
"""

import dataclasses

import iamraw
import utila


@dataclasses.dataclass
class FootNoteStyle:

    content_fontid: int = None
    content_size: float = None

    highnote_fontid: int = None
    highnote_rise: float = None
    highnote_size: float = None


@dataclasses.dataclass
class Validated:
    content: iamraw.FootNote = None
    """Validated FootNote"""
    uppercase: bool = False
    """FootNote starts with an uppercase letter"""
    ends: bool = False
    """FootNote ends with dot"""

    @property
    def valid(self):
        return self.uppercase and self.ends


def most_common_font(items: iamraw.FootNotes) -> FootNoteStyle:
    """Compute general footer font family and font size to judge single
    footnote."""
    if not items:
        return None
    # font_size
    # font_rise
    # font_id
    highnote_size = []
    highnote_rise = []
    highnote_fontid = []
    content_size = []
    content_fontid = []
    for item in items:
        if not item.style:
            utila.error(f'no footnote style: {item}')
            continue
        highnote, content = item.style
        highnote_size.append(highnote.size)
        highnote_rise.append(highnote.rise)
        highnote_fontid.append(highnote.font)
        content_size.extend(
            utila.flatten([[item.size] * (item.end - item.start)
                           for item in content.content]))
        content_fontid.extend(
            utila.flatten([[item.font] * (item.end - item.start)
                           for item in content.content]))

    highnote_rise = utila.roundme(highnote_rise, digits=1, convert=False)  # pylint:disable=R0204
    content_size = utila.roundme(content_size, digits=1, convert=False)  # pylint:disable=R0204

    # TODO: Add more information when returning multiple sizes?
    highnote_size = utila.modes(highnote_size) if highnote_size else None
    highnote_rise = utila.modes(highnote_rise) if highnote_rise else None
    highnote_fontid = utila.modes(highnote_fontid) if highnote_fontid else None
    content_size = utila.modes(content_size) if content_size else None
    content_fontid = utila.modes(content_fontid) if content_fontid else None

    result = FootNoteStyle(
        content_fontid=content_fontid,
        content_size=content_size,
        highnote_fontid=highnote_fontid,
        highnote_rise=highnote_rise,
        highnote_size=highnote_size,
    )
    return result
