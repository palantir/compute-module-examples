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

import logging
from dataclasses import dataclass
from typing import Optional

from compute_modules.auth import retrieve_third_party_id_and_creds
from compute_modules.context import QueryContext
from compute_modules.logging import get_logger
from foundry_sdk_runtime import ObjectLocator, OntologyEdit
from foundry_sdk_runtime.auth import ConfidentialClientAuth
from pokemon_app_sdk import FoundryClient
from pokemon_app_sdk.ontology.objects import SkruyswykPokemon

from ontology_edit_serializer import (
    LinkTypeIdReference,
    ObjectTypeIdReference,
    OntologyTypeIdDict,
    serialize_ontology_edits,
)

logger = get_logger(__name__)
logger.setLevel(logging.INFO)


@dataclass
class PokemonFilterParams:
    type1: Optional[str] = None
    type2: Optional[str] = None
    generation: Optional[int] = None


HOSTNAME = "<INSERT STACK URL>"
CLIENT_ID, CLIENT_SECRET = retrieve_third_party_id_and_creds()
assert CLIENT_ID, "CLIENT_ID not set"
assert CLIENT_SECRET, "CLIENT_SECRET not set"
AUTH = ConfidentialClientAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    hostname=HOSTNAME,
    should_refresh=True,
)
AUTH.sign_in_as_service_user()

CLIENT = FoundryClient(auth=AUTH, hostname=HOSTNAME)

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


def count_pokemon(context: QueryContext, event: PokemonFilterParams) -> int:
    """Count pokemon by the given params"""
    if CLIENT is None:
        raise RuntimeError("3pa mode not enabled")
    base_query = CLIENT.ontology.objects.SkruyswykPokemon
    if event.type1:
        base_query = base_query.where(SkruyswykPokemon.object_type.type1 == event.type1)
    if event.type2:
        base_query = base_query.where(SkruyswykPokemon.object_type.type2 == event.type2)
    if event.generation:
        base_query = base_query.where(
            SkruyswykPokemon.object_type.generation == event.generation
        )
    return int(base_query.count().compute())


@dataclass
class PokemonEditParams:
    name: str
    property: str
    value: int


def ontology_edit_function(
    context: QueryContext,
    event: PokemonEditParams,
) -> list[OntologyEdit]:
    ontology_edits = CLIENT.ontology.edits()
    editable_object = ontology_edits.objects.SkruyswykPokemon.edit(event.name)
    setattr(editable_object, event.property, event.value)
    return serialize_ontology_edits(
        edits=ontology_edits.get_edits(),
        types=types,
    )


@dataclass
class PokemonAddDeleteParams:
    name: str


def ontology_add_function(
    context: QueryContext,
    event: PokemonAddDeleteParams,
) -> list[OntologyEdit]:
    ontology_edits = CLIENT.ontology.edits()
    ontology_edits.objects.SkruyswykPokemon.create(
        name=event.name,
        id=999,
        type1="Normal",
        type2="Delicious",
        generation="10",
        sp_def=60,
        sp_atk=70,
        speed=80,
        attack=90,
        defense=100,
        hp=100,
        total=500,
        legendary=True,
    )
    return serialize_ontology_edits(
        edits=ontology_edits.get_edits(),
        types=types,
    )


def ontology_delete_function(
    context: QueryContext,
    event: PokemonAddDeleteParams,
) -> list[OntologyEdit]:
    ontology_edits = CLIENT.ontology.edits()
    ontology_edits.objects.SkruyswykPokemon.delete("Ivysaur")
    return serialize_ontology_edits(
        edits=ontology_edits.get_edits(),
        types=types,
    )


@dataclass
class PokemonBattleParams:
    home: str
    away: str


def ontology_link_function(
    context: QueryContext,
    event: PokemonBattleParams,
) -> list[OntologyEdit]:
    ontology_edits = CLIENT.ontology.edits()
    home_locator = ObjectLocator(SkruyswykPokemon.api_name(), event.home)
    away_locator = ObjectLocator(SkruyswykPokemon.api_name(), event.away)
    ontology_edits.add_link("homeTeam", source=away_locator, target=home_locator)
    return ontology_edits.get_edits()
