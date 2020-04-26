from . import register_dialect
from ..constructs import SQLDialect
from ..statements.data_types import DataType
from typing import List

class CustomizableSQLDialect(SQLDialect):
	def __init__(self, *, types: List[DataType]):
		self.types = types

register_dialect(CustomizableSQLDialect)
