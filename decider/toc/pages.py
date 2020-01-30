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

import decider.toc.utils


@dataclasses.dataclass
class InvalidPage:
    current: str
    before: str
    text: str


InvalidPages = typing.List[InvalidPage]


def validate(toc: iamraw.Toc) -> InvalidPages:
    toc = flat(toc)
    items = [(item.page, item.title) for item in toc]
    result = validate_pageorder(items)
    return result


def validate_pageorder(items) -> InvalidPages:
    """Validate list of (page number, page number raw/description). The
    number can contain roman and arabic numbers."""
    # TODO: MOVE TO A MORE GENERAL PLACE/NAME
    result = []
    arabic = 0
    roman = 'I'
    for item in items:
        try:
            current_arabic = int(item[0])
            if current_arabic < arabic:
                # invald
                result.append(InvalidPage(
                    current_arabic,
                    arabic,
                    item[1],
                ))
            arabic = current_arabic
        except ValueError:
            current_roman = decider.toc.utils.roman_to_arabic(item[0])
            if current_roman < decider.toc.utils.roman_to_arabic(item[0]):
                result.append(InvalidPage(
                    current_roman,
                    roman,
                    item[1],
                ))
            roman = current_roman
    return result


def flat(toc: iamraw.Toc):
    """Remove nested order and deliver a top down list of pages and
    sections."""
    result = []

    def godown(item: iamraw.toc.TocLinkMixin):
        result.append(item)
        for children in item:
            godown(children)

    for item in toc:
        godown(item)

    return result
