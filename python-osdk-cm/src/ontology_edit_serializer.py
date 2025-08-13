#  Copyright 2025 Palantir Technologies, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from dataclasses import dataclass
from typing import Any, Union


@dataclass
class ObjectTypeIdReference:
    type_id: str
    primary_key: str
    property_ids: dict[str, str]


@dataclass
class LinkTypeIdReference:
    type_id: str


OntologyTypeIdReference = Union[ObjectTypeIdReference, LinkTypeIdReference]
OntologyTypeIdDict = dict[str, OntologyTypeIdReference]


def serialize_ontology_edits(
    edits: list[Any],
    types: OntologyTypeIdDict,
) -> list[dict[str, Any]]:
    return list(
        map(lambda edit: _serialize_ontology_edit(edit=edit, types=types), edits)
    )


def _serialize_ontology_edit(
    edit: Any,
    types: OntologyTypeIdDict,
) -> dict[str, Any]:
    if _is_add_object(edit):
        return _serialize_add_object(edit=edit, types=types)
    if _is_modify_object(edit):
        return _serialize_modify_object(edit=edit, types=types)
    if _is_delete_object(edit):
        return _serialize_delete_object(edit=edit, types=types)
    if _is_add_link(edit):
        return _serialize_add_link(edit=edit, types=types)
    if _is_remove_link(edit):
        return _serialize_remove_link(edit=edit, types=types)
    raise ValueError(f"Unrecognized ontology edit type: {type(edit).__name__}")


def _get_object_type_info_or_throw(
    types: OntologyTypeIdDict,
    api_name: str,
) -> ObjectTypeIdReference:
    if api_name not in types:
        raise ValueError(f"Could not determine object type id for api name: {api_name}")
    assert isinstance(
        types[api_name], ObjectTypeIdReference
    ), f"Expected object reference but got {type(types[api_name]).__name__}"
    return types[api_name]  # type: ignore


def _get_link_type_info_or_throw(
    types: OntologyTypeIdDict,
    api_name: str,
) -> LinkTypeIdReference:
    if api_name not in types:
        raise ValueError(f"Could not determine object type id for api name: {api_name}")
    assert isinstance(
        types[api_name], LinkTypeIdReference
    ), f"Expected link reference but got {type(types[api_name]).__name__}"
    return types[api_name]  # type: ignore


def _is_add_object(edit: Any) -> bool:
    return type(edit).__name__ == "AddObject"


def _serialize_add_object(
    edit: Any,
    types: OntologyTypeIdDict,
) -> dict[str, Any]:
    type_info = _get_object_type_info_or_throw(
        types=types,
        api_name=edit.locator.object_api_name,
    )
    return {
        "type": "addObject",
        "addObject": {
            "locator": {
                "typeId": type_info.type_id,
                "primaryKey": {type_info.primary_key: edit.locator.primary_key},
            },
            "propertyValues": {
                type_info.property_ids[key]: value for key, value in edit.fields.items()
            },
        },
    }


def _is_modify_object(edit: Any) -> bool:
    return type(edit).__name__ == "ModifyObject"


def _serialize_modify_object(
    edit: Any,
    types: OntologyTypeIdDict,
) -> dict[str, Any]:
    type_info = _get_object_type_info_or_throw(
        types=types,
        api_name=edit.locator.object_api_name,
    )
    return {
        "type": "modifyObject",
        "modifyObject": {
            "locator": {
                "typeId": type_info.type_id,
                "primaryKey": {type_info.primary_key: edit.locator.primary_key},
            },
            "propertyValues": {
                type_info.property_ids[key]: value for key, value in edit.fields.items()
            },
        },
    }


def _is_delete_object(edit: Any) -> bool:
    return type(edit).__name__ == "DeleteObject"


def _serialize_delete_object(
    edit: Any,
    types: OntologyTypeIdDict,
) -> dict[str, Any]:
    type_info = _get_object_type_info_or_throw(
        types=types,
        api_name=edit.locator.object_api_name,
    )
    return {
        "type": "deleteObject",
        "deleteObject": {
            "locator": {
                "typeId": type_info.type_id,
                "primaryKey": {type_info.primary_key: edit.locator.primary_key},
            },
        },
    }


def _is_add_link(edit: Any) -> bool:
    return type(edit).__name__ == "AddLink"


def _serialize_add_link(
    edit: Any,
    types: OntologyTypeIdDict,
) -> dict[str, Any]:
    source_type_info = _get_object_type_info_or_throw(
        types=types,
        api_name=edit.source.object_api_name,
    )
    target_type_info = _get_object_type_info_or_throw(
        types=types,
        api_name=edit.target.object_api_name,
    )
    link_type_info = _get_link_type_info_or_throw(
        types=types,
        api_name=edit.relationship_api_name,
    )
    return {
        "type": "addLink",
        "addLink": {
            "locator": {
                "relationId": link_type_info.type_id,
                "sourceObjectLocator": {
                    "typeId": source_type_info.type_id,
                    "primaryKey": {
                        source_type_info.primary_key: edit.source.primary_key
                    },
                },
                "targetObjectLocator": {
                    "typeId": target_type_info.type_id,
                    "primaryKey": {
                        target_type_info.primary_key: edit.target.primary_key
                    },
                },
            }
        },
    }


def _is_remove_link(edit: Any) -> bool:
    return type(edit).__name__ == "RemoveLink"


def _serialize_remove_link(
    edit: Any,
    types: OntologyTypeIdDict,
) -> dict[str, Any]:
    return {}
