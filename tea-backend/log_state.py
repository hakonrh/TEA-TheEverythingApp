from typing import List
from contextvars import ContextVar

logs: List[dict] = []
db_counter: ContextVar[int] = ContextVar("db_counter", default=0)
