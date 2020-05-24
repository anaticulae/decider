# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Page order validator
====================

There are two different types of page numbers. The common **Arabic
Numbers (0,1,3,...)** and **Roman Numbers (I, II, III, ...)**. Arabic
numbers are mainly used for page content and Roman numbers for tables
etc.

In some works Roman numbers are nor used anymore cause there are a
relict of old times. Arabic numbers are used for the whole document.
"""

import dataclasses
import typing

import iamraw
import iamraw.toc
import texmex.numbers
import utila

import decider_toc.utils


@dataclasses.dataclass
class InvalidPage:
    current: str
    before: str
    text: str
    raw_location: int = None


InvalidPages = typing.List[InvalidPage]


def validate(toc: iamraw.Toc) -> InvalidPages:
    toc = decider_toc.utils.flat(toc)
    items = [(item.page, item.title, item.raw_location) for item in toc]
    result = validate_pageorder(items)
    return result


def validate_pageorder(items) -> InvalidPages:
    """Validate list of (page number, page number raw/description). The
    number can contain roman and arabic numbers.

    >>> validate_pageorder([('1', 'Einleitung 1', 1), ('2', 'Beschreibung 2', 1)])
    []
    >>> validate_pageorder([('II', 'Anhang II', 1), ('I', 'Inhaltsverzeichnis I', 1)])
    [InvalidPage(current='I', before='II', text='Inhaltsverzeichnis I', raw_location=1)]
    """
    # TODO: MOVE TO A MORE GENERAL PLACE/NAME
    result = []
    arabic = 0
    roman = 'I'
    for pagenumber, title, raw_location in items:
        if raw_location is None:
            utila.error(f'no `raw_location` for toc: `{title}`')
            raw_location = 0  # TODO: REMOVE LATER
        raw_location = int(raw_location)
        try:
            current_arabic = int(pagenumber)
            if current_arabic < arabic:
                # invald
                result.append(
                    InvalidPage(
                        current_arabic,
                        arabic,
                        title,
                        raw_location=raw_location,
                    ))
            arabic = current_arabic
        except ValueError:
            current_roman = texmex.numbers.arabic(pagenumber)
            if current_roman < texmex.numbers.arabic(roman):
                result.append(
                    InvalidPage(
                        pagenumber,
                        roman,
                        title,
                        raw_location=raw_location,
                    ))
            roman = pagenumber
    return result
