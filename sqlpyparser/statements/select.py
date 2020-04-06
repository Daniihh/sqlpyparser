from typing import Optional as OptionalType
from pyparsing import CaselessKeyword, Optional, ParseExpression, Suppress, \
	delimitedList
from . import SQLStatement
from .expressions import ColumnExpression, TableExpression

# SELECT SYNTAX
# The full implemented SELECT syntax.
# Source: https://dev.mysql.com/doc/refman/5.7/en/select.html
class SelectStatement(SQLStatement):
	statement_type = "SELECT"
	parse_expression = (
		CaselessKeyword("SELECT").setResultsName("statement_type") +
		(delimitedList(ColumnExpression.parse_expression) ^ CaselessKeyword("*"))
			.setResultsName("columns") +
		CaselessKeyword("FROM") +
		delimitedList(TableExpression.parse_expression).setResultsName("tables") +
		Suppress(Optional(";"))
	)

	def __init__(self, expression: ParseExpression):
		self.parse_results = expression
		self.columns = [
			ColumnExpression(column_data) for column_data
				in expression.get("columns")
		] if expression.get("columns")[0] != "*" else None
		self.tables = [
			TableExpression(table_data) for table_data
				in expression.get("tables")
		]

	def __str__(self):
		return "SELECT {} FROM {}".format(
			"*" if self.columns is None else ", ".join(map(str, self.columns)),
			", ".join(map(str, self.tables))
		)

target = SelectStatement
