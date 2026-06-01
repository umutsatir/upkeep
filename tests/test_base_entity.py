# OWNER: MEMBER-1
from datetime import datetime, timezone

import pytest
from bson import ObjectId

from app.models.base import BaseEntity, PyObjectId


def test_base_entity_has_generated_id():
    entity = BaseEntity()
    assert ObjectId.is_valid(entity.id)


def test_base_entity_timestamps_are_utc():
    entity = BaseEntity()
    assert entity.created_at.tzinfo is not None
    assert entity.updated_at.tzinfo is not None


def test_touch_updates_updated_at():
    entity = BaseEntity()
    original = entity.updated_at
    entity.touch()
    assert entity.updated_at >= original


def test_to_mongo_converts_id_to_object_id():
    entity = BaseEntity()
    doc = entity.to_mongo()
    assert "_id" in doc
    assert "id" not in doc
    assert isinstance(doc["_id"], ObjectId)


def test_from_mongo_round_trip():
    entity = BaseEntity()
    doc = entity.to_mongo()
    restored = BaseEntity.from_mongo(doc)
    assert restored.id == entity.id
    assert restored.created_at.replace(microsecond=0) == entity.created_at.replace(microsecond=0)


def test_py_object_id_accepts_valid_string():
    oid = str(ObjectId())
    assert PyObjectId.validate(oid) == oid


def test_py_object_id_rejects_invalid_string():
    with pytest.raises(ValueError):
        PyObjectId.validate("not-an-object-id")
