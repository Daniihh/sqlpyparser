from pyparsing import CaselessKeyword, Optional, ParseResults, Suppress, \
	delimitedList
from typing import List, Optional as OptionalType, Union
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

	columns: List[ColumnExpression]
	tables: List[TableExpression]

	def __init_from_args__(self,
			columns: OptionalType[Union[List[Union[str, ColumnExpression]], str,
				ColumnExpression]],
			tables: Union[List[Union[str, TableExpression]], str, TableExpression]):
		column_list = columns if isinstance(columns, list) else [columns] \
			if columns is not None else []
		table_list = tables if isinstance(tables, list) else [tables] \
			if tables is not None else []

		if len(table_list) == 0:
			raise ValueError("tables cannot be empty")

		self.columns = [
			column if isinstance(column, ColumnExpression) \
				else ColumnExpression(column) for column in column_list
		]
		self.tables = [
			table if isinstance(table, TableExpression) \
				else TableExpression(table) for table in table_list
		]

	def __init_from_results__(self, results: ParseResults):
		self.parse_results = results
		self.columns = [
			ColumnExpression(column_data) for column_data
				in results.get("columns")
		] if results.get("columns")[0] != "*" else []
		self.tables = [
			TableExpression(table_data) for table_data
				in results.get("tables")
		]

	def __str__(self):
		return "SELECT {} FROM {}".format(
			"*" if len(self.columns) == 0 else ", ".join(map(str, self.columns)),
			", ".join(map(str, self.tables))
		)

target = [SelectStatement]
