from __future__ import annotations
from ..constructs import SQLStatement
from ..utilities import OneOrMore, ZeroOrMore, as_list
from pyparsing import CaselessKeyword, ParseExpression, ParseResults, \
	delimitedList
from typing import Callable, Generic, List, Optional, Type, TypeVar, Union

C = TypeVar("C")
T = TypeVar("T")

# SELECT SYNTAX
# The full implemented SELECT syntax.
# Source: https://dev.mysql.com/doc/refman/5.7/en/select.html
class SelectStatement(SQLStatement, Generic[C, T]):
	statement_type = "SELECT"

	@classmethod
	def create_parse_expression(cls, column_expr: ParseExpression,
			table_expr: ParseExpression) -> ParseExpression:
		return \
			CaselessKeyword("SELECT").setResultsName("statement_type") + \
			(delimitedList(column_expr) ^ CaselessKeyword("*")) \
				.setResultsName("columns") + \
			CaselessKeyword("FROM") + \
			delimitedList(table_expr).setResultsName("tables")

	@classmethod
	def from_results(cls, results: ParseResults,
			column_from_results: Callable[[ParseResults], C],
			table_from_results: Callable[[ParseResults], T]) -> SelectStatement[C, T]:
		return cls(
			column_from_results(results.get("columns")),
			table_from_results(results.get("tables")),
			results=results
		)

	columns: List[C]
	tables: List[T]

	def __init__(self, columns: ZeroOrMore[Union[C]], tables: OneOrMore[Union[T]],
			*, results: Optional[ParseResults] = None) -> None:
		self.parse_results = results
		self.columns = as_list(columns)
		self.tables = as_list(tables)

	def __str__(self):
		return "SELECT {} FROM {}".format(
			"*" if len(self.columns) == 0 else ", ".join(map(str, self.columns)),
			", ".join(map(str, self.tables))
		)

target = [SelectStatement]
