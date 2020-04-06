from typing import Optional as OptionalType
from pyparsing import CaselessKeyword, Group, Optional, ParseResults
from . import SQLExpression
from .identifier import database_name_syntax, \
	identifier_syntax

# TABLE REFERENCE
# Specifies a table from a database to use, and an optional alias given.
class TableExpression(SQLExpression):
	parse_expression = Group(
		(
			database_name_syntax.setResultsName("database_name") +
			identifier_syntax.setResultsName("table_name") +
			Optional(
				(
					CaselessKeyword("AS") +
					identifier_syntax.setResultsName("alias_name")
				)
			)
		)
	)

	def __init__(self, results: ParseResults):
		self.parse_results = results
		self.database: OptionalType[str] = results.get("database_name") \
			if not isinstance(results.get("database_name"), ParseResults) else None
		self.name: str = results.get("table_name")
		self.alias: OptionalType[str] = results.get("alias_name")

	def __str__(self):
		return "{}{}{}".format(
			f"{self.database}." if self.database is not None else "",
			self.name,
			f" AS {self.alias}" if self.alias is not None else ""
		)

# COLUMN REFERENCE
class ColumnExpression(SQLExpression):
	parse_expression = Group(
		(
			identifier_syntax.setResultsName("column_name") +
			Optional(
				(
					CaselessKeyword("AS") +
					identifier_syntax.setResultsName("alias_name")
				)
			)
		)
	)

	def __init__(self, results: ParseResults):
		self.parse_results = results
		self.name: str = results.get("column_name")
		self.alias: OptionalType[str] = results.get("alias_name")

	def __str__(self):
		return self.name if self.alias is None else f"{self.name} AS {self.alias}"
