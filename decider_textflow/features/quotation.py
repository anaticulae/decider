# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import typing

import german
import iamraw
import konrad.quotation.german
import protocol
import textflow.quotation.serialize
import utila

MAX_CITATION_LENGTH = 50  # TODO: HOLY VALUE


def work(text: str, pages: tuple) -> typing.Tuple[str, str]:
    quotations = textflow.quotation.serialize.load_quotations(text)

    # filter pages, TODO: remove after upgrading textflow
    quotations = [
        item for item in quotations if not utila.should_skip(item.page, pages)
    ]

    linter = protocol.from_module(__name__)

    linting(quotations, linter)
    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)

    return user, developer


def from_sentence(page, sentence):
    return iamraw.Location.fromstr(f's{sentence}p{page}')


def linting(quotations, linter: protocol.Linter):
    checkers = protocol.parse_checkers(__name__)
    for checker in checkers:
        for quote in quotations:
            location = from_sentence(page=quote.page, sentence=quote.index)
            call = functools.partial(
                linter.add_finding,
                msgid=checker.msgid,
                location=location,
                sentence=quote.index,
            )
            tokens = german.split_token(quote.sentence)
            checker(call, tokens)


SOLUTION_7100 = """\
Nicht geschlossenes Zitat

Satz {{sentence}} enthält eine ungerade Anzahl von Anführungszeichen.

{darstellung/satzzeichen#anfuhrungszeichen}
"""


def check_7100_german_quote_not_closed(linter: callable, tokens: list):
    if not german.isger(tokens):
        return
    validated = konrad.quotation.german.double_quotation_closed(tokens)
    if validated:
        return

    linter()


SOLUTION_7101 = """\
Doppelte Anführungszeichen im Zitat

Satz {{sentence}} enthält doppelte Anführungszeichen im Zitat. Ersetzen
Sie diese doppelten Anführungszeichen durch einfache Anführungszeichen.

{darstellung/satzzeichen#anfuhrungszeichen}
"""


def check_7101_german_quote_double_quote_inside(linter: callable, tokens: list):
    if not german.isger(tokens):
        return
    validated = konrad.quotation.german.double_quotation_closed(tokens)
    if not validated:
        return
    if konrad.quotation.german.no_double_quotes_inside_double(tokens):
        return

    linter()


SOLUTION_7110 = """\
Zitat zu lang

Konzentrieren Sie sich auf den wichtigen Teil des Zitats und stellen Sie
die eigene Denkleistung in den Vordergrund.

{text/zitat#umfang}
"""


def check_7110_max_citation_length(linter: callable, tokens: list):
    if len(tokens) <= MAX_CITATION_LENGTH:
        return
    linter()
