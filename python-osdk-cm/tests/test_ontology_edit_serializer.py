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

import pytest
from foundry_sdk_runtime.ontology_edit import AddLink  # RemoveLink,
from foundry_sdk_runtime.ontology_edit import (
    AddObject,
    DeleteObject,
    ModifyObject,
    ObjectLocator,
)

from src.ontology_edit_serializer import (
    LinkTypeIdReference,
    ObjectTypeIdReference,
    OntologyTypeIdDict,
    serialize_ontology_edits,
)

types: OntologyTypeIdDict = {
    "SkruyswykPokemon": ObjectTypeIdReference(
        type_id="skruyswyk-pokemon",
        primary_key="name",
        property_ids={
            "attack": "attack",
            "defense": "defense",
            "generation": "generation",
            "hp": "hp",
            "id": "id",
            "legendary": "legendary",
            "spAtk": "sp_atk",
            "spDef": "sp_def",
            "speed": "speed",
            "total": "total",
            "type1": "type_1",
            "type2": "type_2",
        },
    ),
    "homeTeam": LinkTypeIdReference(type_id="skruyswyk-pokemon-skruyswyk-pokemon"),
    "awayTeam": LinkTypeIdReference(type_id="skruyswyk-pokemon-skruyswyk-pokemon"),
}

test_cases = [
    (
        ModifyObject(
            locator=ObjectLocator(
                object_api_name="SkruyswykPokemon",
                primary_key="Ivysaur",
            ),
            fields={"spDef": 81},
        ),
        {
            "type": "modifyObject",
            "modifyObject": {
                "locator": {
                    "typeId": "skruyswyk-pokemon",
                    "primaryKey": {"name": "Ivysaur"},
                },
                "propertyValues": {"sp_def": 81},
            },
        },
    ),
    (
        AddObject(
            locator=ObjectLocator(
                object_api_name="SkruyswykPokemon",
                primary_key="Marshmallow",
            ),
            fields={
                "id": 999,
                "type1": "Normal",
                "type2": "Delicious",
                "generation": "10",
                "spDef": 60,
                "speed": 80,
                "spAtk": 70,
                "attack": 90,
                "hp": 100,
                "legendary": True,
                "total": 500,
                "defense": 100,
            },
        ),
        {
            "type": "addObject",
            "addObject": {
                "locator": {
                    "typeId": "skruyswyk-pokemon",
                    "primaryKey": {"name": "Marshmallow"},
                },
                "propertyValues": {
                    "id": 999,
                    "type_1": "Normal",
                    "type_2": "Delicious",
                    "generation": "10",
                    "sp_def": 60,
                    "speed": 80,
                    "sp_atk": 70,
                    "attack": 90,
                    "hp": 100,
                    "legendary": True,
                    "total": 500,
                    "defense": 100,
                },
            },
        },
    ),
    (
        DeleteObject(
            locator=ObjectLocator(
                object_api_name="SkruyswykPokemon",
                primary_key="Gyrados",
            )
        ),
        {
            "type": "deleteObject",
            "deleteObject": {
                "locator": {
                    "typeId": "skruyswyk-pokemon",
                    "primaryKey": {"name": "Gyrados"},
                },
            },
        },
    ),
    (
        AddLink(
            relationship_api_name="homeTeam",
            source=ObjectLocator(
                object_api_name="SkruyswykPokemon",
                primary_key="Charmander",
            ),
            target=ObjectLocator(
                object_api_name="SkruyswykPokemon",
                primary_key="Bulbasaur",
            ),
        ),
        {
            "type": "addLink",
            "addLink": {
                "locator": {
                    "relationId": "skruyswyk-pokemon-skruyswyk-pokemon",
                    "sourceObjectLocator": {
                        "typeId": "skruyswyk-pokemon",
                        "primaryKey": {"name": "Charmander"},
                    },
                    "targetObjectLocator": {
                        "typeId": "skruyswyk-pokemon",
                        "primaryKey": {"name": "Bulbasaur"},
                    },
                }
            },
        },
    ),
]


@pytest.mark.parametrize("edit_object, expected_result", test_cases)
def test_serialize_ontology_edits(edit_object, expected_result) -> None:
    assert serialize_ontology_edits([edit_object], types) == [expected_result]
