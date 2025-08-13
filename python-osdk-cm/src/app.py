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

from compute_modules import add_function, start_compute_module

from pokemon import count_pokemon  # type: ignore[import-not-found]
from pokemon import (
    ontology_add_function,
    ontology_delete_function,
    ontology_edit_function,
    ontology_link_function,
)

if __name__ == "__main__":
    add_function(count_pokemon)
    add_function(ontology_edit_function)
    add_function(ontology_add_function)
    add_function(ontology_delete_function)
    add_function(ontology_link_function)
    start_compute_module()
