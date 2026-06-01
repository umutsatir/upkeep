# OWNER: MEMBER-1
from datetime import datetime, timezone
from typing import Annotated

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class PyObjectId(str):
    """Thin wrapper so Pydantic v2 accepts bson.ObjectId as a plain string field."""

    @classmethod
    def __get_validators__(cls):  # pragma: no cover  (pydantic v1 compat hook)
        yield cls.validate

    @classmethod
    def validate(cls, v: object) -> "PyObjectId":
        if isinstance(v, ObjectId):
            return cls(str(v))
        if isinstance(v, str) and ObjectId.is_valid(v):
            return cls(v)
        raise ValueError(f"Invalid ObjectId: {v!r}")

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):  # noqa: ANN001
        from pydantic_core import core_schema

        return core_schema.no_info_plain_validator_function(cls.validate)


class BaseEntity(BaseModel):
    """Root domain object.  All entities inherit from this class.

    id maps to MongoDB's _id.  created_at / updated_at are managed here so
    repositories never have to think about timestamps.
    """

    id: PyObjectId = Field(default_factory=lambda: PyObjectId(str(ObjectId())))
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)

    model_config = {"populate_by_name": True, "arbitrary_types_allowed": True}

    def touch(self) -> None:
        """Bump updated_at to now — call before persisting a mutation."""
        self.updated_at = _utcnow()

    def to_mongo(self) -> dict:
        """Serialise to a dict suitable for Motor / PyMongo insertion.

        Converts `id` → `_id` and stores it as bson.ObjectId.
        """
        data = self.model_dump()
        data["_id"] = ObjectId(data.pop("id"))
        return data

    @classmethod
    def from_mongo(cls, data: dict) -> "BaseEntity":
        """Deserialise from a raw MongoDB document."""
        if data is None:
            raise ValueError("Cannot deserialise None document")
        data = dict(data)  # don't mutate caller's dict
        data["id"] = str(data.pop("_id"))
        return cls(**data)
