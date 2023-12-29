from typing import Literal
from dataclasses import dataclass

@dataclass
class Error:
    code: Literal['auth_error', 'fs_error']
    message: str