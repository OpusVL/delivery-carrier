# coding: utf-8
# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


class InvalidAccountNumber(Exception):
    print "InvalidAccountNumber"
    pass


class InvalidSequence(Exception):
    pass


class InvalidWeight(Exception):
    pass


class InvalidSize(Exception):
    pass


class InvalidType(Exception):
    print "InvalidType"
    pass


class InvalidValue(Exception):
    pass


class InvalidValueNotInList(Exception):
    print "InvalidValueNotInList"
    pass


class InvalidMissingField(Exception):
    print "InvalidMissingField"
    pass


class InvalidZipCode(Exception):
    pass


class InvalidCountry(Exception):
    pass


class InvalidDate(Exception):
    pass


class InvalidCode(Exception):
    pass


class InvalidKeyInTemplate(Exception):
    pass
