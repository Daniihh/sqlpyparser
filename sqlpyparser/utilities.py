from typing import Any, Tuple, Type

def tupleisinstance(value: Any, check: Tuple[Type[Any], ...]) -> bool:
	return isinstance(value, tuple) and len(check) == len(value) and \
		all((isinstance(value[ind], check[ind]) for ind in range(0, len(check))))

class RawText:
	def __init__(self, text: str):
		self.text = text

	def __repr__(self):
		return self.text
