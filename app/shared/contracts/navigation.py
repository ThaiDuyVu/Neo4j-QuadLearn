from dataclasses import dataclass
from typing import Callable
from app.core.context import AppContext

@dataclass(frozen=True)
class PageSpec:
    title: str
    path: str
    render: Callable[[AppContext], None]
