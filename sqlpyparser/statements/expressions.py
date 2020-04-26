from typing import Optional as OptionalT
from pyparsing import CaselessKeyword, Group, Optional, ParseResults
from . import SQLExpression
from .data_types import DataType, DataTypeName
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

	database: OptionalT[str]
	name: str
	alias: OptionalT[str]

	def __init_from_args__(self, name: str, database: OptionalT[str] = None,
			alias: OptionalT[str] = None):
		self.name = name
		self.database = database
		self.alias = alias

	def __init_from_results__(self, results: ParseResults):
		self.parse_results = results
		self.database = results.get("database_name") \
			if not isinstance(results.get("database_name"), ParseResults) else None
		self.name = results.get("table_name")
		self.alias = results.get("alias_name")

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

	name: str
	alias: OptionalT[str]

	def __init_from_args__(self, name: str, alias: OptionalT[str] = None):
		self.name = name
		self.alias = name

	def __init_from_results__(self, results: ParseResults):
		self.parse_results = results
		self.name = results.get("column_name")
		self.alias = results.get("alias_name")

	def __str__(self):
		return self.name if self.alias is None else f"{self.name} AS {self.alias}"

class ColumnDefinitionExpression(SQLExpression):
	parse_expression = Group(
		identifier_syntax.setResultsName("column_name") +
		DataType.parse_expression
	)

	def __init_from_args__(self):
		pass

	def __init_from_results__(self, results: ParseResults):
		data_type = results.get("data_type")
		type_argument = data_type[1] if len(data_type) > 1 else None
		self.parse_results = results
		self.column_name: str = results.get("column_name")
		self.type_name: DataTypeName = \
			DataTypeName(data_type[0], type_argument)
		self.type_argument: Optional[int] = \
			None if type_argument is None else int(type_argument)
