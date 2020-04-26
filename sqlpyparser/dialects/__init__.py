from ..constructs import SQLDialect
from typing import List, Type

dialects: List[Type[SQLDialect]] = []

def register_dialect(dialect: Type[SQLDialect]):
	global dialects
	dialects = [*dialects, dialect]
