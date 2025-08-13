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

FROM --platform=linux/amd64 python:3.12

COPY requirements.txt .

# IMPORTANT: Use --mount=type=secret to securely access your dependency
RUN --mount=type=secret,id=FOUNDRY_TOKEN,env=FOUNDRY_TOKEN \
    pip install -r requirements.txt --upgrade \
    --extra-index-url "https://user:$FOUNDRY_TOKEN@stack.palantirfoundry.com/artifacts/api/repositories/ri.artifacts.main.repository.8d6eacb5-058c-47c7-a601-cf38cf76de8f/contents/release/pypi/simple" \\
    --extra-index-url "https://user:$FOUNDRY_TOKEN@stack.palantirfoundry.com/artifacts/api/repositories/ri.foundry-sdk-asset-bundle.main.artifacts.repository/contents/release/pypi/simple"

COPY src .
USER 5000
ENTRYPOINT ["python", "app.py"]
