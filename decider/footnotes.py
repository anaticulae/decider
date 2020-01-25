# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
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
import collections
import dataclasses
import os
import statistics
import typing

import hey.path
import iamraw
import serializeraw
import utila

# TODO: REPLACE AFTER UPGRADING IAMRAW
FootNotes = typing.List[iamraw.FootNote]
iamraw.FootNotes = FootNotes

PageContentFootnote = collections.namedtuple(
    'PageContentFootnotes',
    'content, page',
)
PageContentFootnotes = typing.List[PageContentFootnote]


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


def footnotes(headerfooters: iamraw.PageContentFooterHeaders,
             ) -> PageContentFootnotes:
    result = []
    for item in headerfooters:
        try:
            selected = item.footer.notes
        except AttributeError:
            pass
        else:
            assert selected
            result.append(PageContentFootnote(content=selected, page=item.page))
    return result


def load(path: str, pages: tuple = None) -> PageContentFootnotes:
    """Load list of `PageContentFootnote` from given `path`

    Args:
        path: path to content file
        pages: tuple of pages to process
    Returns:
        loaded list of PageContentFootnote
    """
    loaded = serializeraw.load_headerfooter(path, pages=pages)
    selected = footnotes(loaded)
    return selected


def load_frompath(
        path: str,
        prefix: str = '',
        pages: tuple = None,
) -> PageContentFootnotes:
    """Determine path to footer file from given directory `path` and
    optional `prefix`."""
    assert os.path.isdir(path), f'invalid result directory {path}'
    source = hey.path.headerfooters(path, prefix=prefix)
    loaded = load(source, pages=pages)
    return loaded


def validate(note: iamraw.FootNote) -> Validated:
    text = note.text.strip()

    start_with_uppercase = text[0].isupper()
    ends_with_dot = text[-1] == '.'

    result = Validated(
        content=note,
        uppercase=start_with_uppercase,
        ends=ends_with_dot,
    )
    return result


def most_common_font(items: iamraw.FootNotes) -> FootNoteStyle:
    """Compute general footer font family and font size to judge single
    foot note."""
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
    highnote_size = statistics.mode(highnote_size)
    highnote_rise = statistics.mode(highnote_rise)
    highnote_fontid = statistics.mode(highnote_fontid)
    content_size = statistics.mode(content_size)
    content_fontid = statistics.mode(content_fontid)

    result = FootNoteStyle(
        content_fontid=content_fontid,
        content_size=content_size,
        highnote_fontid=highnote_fontid,
        highnote_rise=highnote_rise,
        highnote_size=highnote_size,
    )
    return result
