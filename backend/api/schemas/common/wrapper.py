from typing import Generic, Optional, TypeVar, Union
from uuid import UUID

from pydantic import BaseModel

T = TypeVar("T")


class BaseResponseWrapper(BaseModel, Generic[T]):
    code: Union[int, UUID]
    message: str
    data: Optional[T] = None
