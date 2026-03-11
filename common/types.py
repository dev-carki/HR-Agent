from typing import Annotated
from pydantic import Field

PhoneNumber = Annotated[
    str,
    Field(pattern=r"^010-\d{4}-\d{4}$")
]