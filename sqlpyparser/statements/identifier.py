from pyparsing import FollowedBy, Optional, Or, QuotedString, Suppress, Word, \
	alphanums
from .utils import stripQuotes

#
# SCHEMA OBJECT NAMES (IDENTIFIERS)
#
# Source: https://dev.mysql.com/doc/refman/5.7/en/identifiers.html
#

identifier_syntax: Or = Or([
	Word(alphanums + "_$"),
	QuotedString('"'),
	QuotedString("`"),
	QuotedString("'")
]).setParseAction(stripQuotes)

database_name_syntax = (Optional(identifier_syntax + FollowedBy('.') +
								 Suppress('.'), default=None)
						.setParseAction(lambda s, l, toks: toks[0]))
