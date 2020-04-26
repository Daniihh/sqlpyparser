from __future__ import annotations
from .utilities import RawText
from abc import ABC, abstractmethod
from pyparsing import ParseExpression, ParseResults
from typing import Any, List, Optional, TypeVar

T = TypeVar("T")

class SQLExpression(ABC):
	parse_results: Optional[ParseResults] = None

	@classmethod
	@abstractmethod
	def create_parse_expression(cls) -> ParseExpression: ...

	@classmethod
	@abstractmethod
	def from_results(cls: T, results: ParseResults) -> T: ...

	def __init__(self, results: ParseResults):
		self.parse_results = results

	def __getitem__(self, key: int) -> List[str]:
		return self.parse_results[key]

	def __getattr__(self, attribute: str) -> ParseResults:
		if self.parse_results is None:
			raise AttributeError("This SQLExpression was not created with " +
				"ParseResults.")
		return self.parse_results.get(attribute)

	def __repr__(self, class_props_shown: int = 3, results_props_shown: int = 2):
		class_props = [
			key for key, val in vars(self).items() if not key.startswith("_")
		]
		class_props_short = class_props[:class_props_shown]
		class_props_not_shown = len(class_props) - class_props_shown
		results_props = {
			key: val if not isinstance(val, ParseResults) else RawText("...")
				for key, val in dict(self.parse_results or {}).items()
		}
		results_props_short = dict([*results_props.items()][:results_props_shown])
		results_props_not_shown = len(results_props) - results_props_shown

		return "<{} {}{} {}{}>".format(
			type(self).__name__,
			class_props_short,
			f"; {class_props_not_shown} hidden" if class_props_not_shown > 0
				else "",
			results_props_short,
			f"; {results_props_not_shown} hidden" if results_props_not_shown > 0
				else ""
		)

	def get(self, item: str, defaultValue: Any = None) -> ParseResults:
		if self.parse_results is None:
			raise AttributeError("This SQLExpression was not created with " +
				"ParseResults.")
		return self.parse_results.get(item, defaultValue)

class SQLStatement(SQLExpression):
	statement_type: str

class SQLDialect(ABC):
	def __init__(self):
		pass

	@abstractmethod
	def parse(self, string) -> SQLStatement: ...
