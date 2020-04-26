from typing import Any, List, Optional, Tuple, Type, TypeVar, Union

T = TypeVar("T")

OneOrMore = Union[T, List[T]]
ZeroOrMore = Optional[OneOrMore[T]]

def as_list(item: ZeroOrMore[T]) -> List[T]:
	return item if isinstance(item, list) else [item] if item is not None else []

def tupleisinstance(value: Any, check: Tuple[Type[Any], ...]) -> bool:
	return isinstance(value, tuple) and len(check) == len(value) and \
		all((isinstance(value[ind], check[ind]) for ind in range(0, len(check))))

class RawText:
	def __init__(self, text: str):
		self.text = text

	def __repr__(self):
		return self.text
