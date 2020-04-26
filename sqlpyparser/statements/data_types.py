from __future__ import annotations
from ..constructs import SQLExpression
from abc import abstractmethod
from pyparsing import CaselessKeyword, ParseExpression, ParseResults, \
	QuotedString
from typing import Any, List, Union

def add_key_value(key: str, value: Any):
	def set_parse_action(toks: ParseResults):
		toks[key] = value
	return set_parse_action

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
	type_name: str
	type_arguments: Union[List[DataType], DataType]

	@abstractmethod
	def as_python_value(self) -> Any: ...

class DataLiteral(SQLExpression):
	parse_expression = (
		(
			CaselessKeyword("TRUE") ^
			CaselessKeyword("FALSE")
		).setParseAction(add_key_value("type", "boolean")) ^
		QuotedString('"')
			.setParseAction(add_key_value("type", "string"))
	).setResultsName("value")

	type: str
	value: Any

	def __init_from_args__(self, type: str, value: Any):
		self.type = type
		self.value = value

	def __init_from_results__(self, results: ParseResults):
		self.parse_results = results
		self.type = results.get("type")
		self.value = results.get("value")
