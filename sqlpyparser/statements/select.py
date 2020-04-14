from pyparsing import CaselessKeyword, Optional, ParseResults, Suppress, \
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

	def __init__(self, results: ParseResults):
		self.parse_results = results
		self.columns = [
			ColumnExpression(column_data) for column_data
				in results.get("columns")
		] if results.get("columns")[0] != "*" else None
		self.tables = [
			TableExpression(table_data) for table_data
				in results.get("tables")
		]

	def __str__(self):
		return "SELECT {} FROM {}".format(
			"*" if self.columns is None else ", ".join(map(str, self.columns)),
			", ".join(map(str, self.tables))
		)

target = [SelectStatement]
