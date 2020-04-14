from typing import Any
from pyparsing import CaselessKeyword, Or, ParseResults
from . import SQLExpression

class DataTypeName(str):
	def __new__(cls, value: str, argument: Any):
		return str.__new__(cls, value) # type: ignore

	def __init__(self, value: str, argument: Any):
		self._secondary_argument = None if argument is None else str(argument)

	def __getitem__(self, thing: int):
		value = {0: str(self), 1: self._secondary_argument}[thing]
		if value is None:
			raise AttributeError()
		return value

class DataType(SQLExpression):
	parse_expression = Or((
		CaselessKeyword("BOOL"), # For now this is fine.
		CaselessKeyword("TEXT"),
		CaselessKeyword("INT")
	)).setResultsName("type_name")

	def __init__(self, expression: ParseResults):
		self.parse_results = expression
		self.type_name = expression.get("type_name")
