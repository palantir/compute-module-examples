# python-osdk-cm

This repo contains a working example of how to call a Python OSDK from Compute Modules. Below are detailed instructions.

## How to call the Python OSDK from a compute module

### Create the application & SDK

1. Go to `Developer Console` and create a new application
2. Make sure to generate an ontology SDK & add your ontology objects
3. Make sure `Python` SDk is selected
4. Select `Backend service` application type
5. Select `Application's permissions` under permissions

### Grant access to the Application User
The client ID created in your App needs to have access to whatever data resources you've added if you want the SDK to be able to access those objects/actions/etc. You can do this by going to the "Security" tab of the given resource, searching for your app's client ID (found under the `OAuth & Scopes` tab of the application), then adding that user. 

Note: if you want to grant access to an ontology object backed by a dataset, you will need to grant access to both the ontology set _and_ the underlying dataset.


### Create & add a source to your compute module
By default, all egress is disabled in Compute Modules. So in order to use the OSDK from a compute module you will need to set up a source for the hostname that you will pass into the OSDK. 

- When creating the source, make sure to check the "Allow this source to be imported into compute modules" option.
- Add the client ID and client secret as secrets to the source.
- Once the source is created, go to the `Configure` tab of the compute module and import the source you just created.
- Once imported, click on the source to open the configuration panel. In there, you will see the "mapped" named of the secrets you created in your source. For example, a secret named `CLIENTID` may look like `additionalSecretCLIENTID`


You can now access the client ID/secret of your application user like this:
```python
from compute_modules.sources import get_source_secret

# `PokemonOsdk` corresponds to the API Name of my source
# additionalSecretCLIENTID/additionalSecretCLIENTSECRET correspond to the names of the secrets mounted to this source
CLIENT_ID = get_source_secret("PokemonOsdk", "additionalSecretCLIENTID")
CLIENT_SECRET = get_source_secret("PokemonOsdk", "additionalSecretCLIENTSECRET")
```

### Build your docker container

In the "Start developing" tab of your Dev Console application, you will find a command similar to the one below to install your OSDK library via pip:

```sh
pip install pokemon_app_sdk --upgrade \
    --index-url "https://user:$FOUNDRY_TOKEN@stack.palantirfoundry.com/artifacts/api/repositories/ri.artifacts.main.repository.8d6eacb5-058c-47c7-a601-cf38cf76de8f/contents/release/pypi/simple" \
    --extra-index-url "https://user:$FOUNDRY_TOKEN@stack.palantirfoundry.com/artifacts/api/repositories/ri.foundry-sdk-asset-bundle.main.artifacts.repository/contents/release/pypi/simple"
```

You can use this same command to build a docker image with that dependency by adding an `ARG` to your dockerfile. 

For example, below is a working `requirements.txt` and corresponding `Dockerfile`

**requirements.txt:**
```plaintext
pokemon_app_sdk
foundry-compute-modules>=0.9.0
```

**Dockerfile:**
```docker
FROM --platform=linux/amd64 python:3.12

COPY requirements.txt .

# IMPORTANT: Use --mount=type=secret to securely access your dependency
RUN --mount=type=secret,id=FOUNDRY_TOKEN,env=FOUNDRY_TOKEN \
    pip install -r requirements.txt --upgrade \
    --index-url "https://user:$FOUNDRY_TOKEN@stack.palantirfoundry.com/artifacts/api/repositories/ri.artifacts.main.repository.8d6eacb5-058c-47c7-a601-cf38cf76de8f/contents/release/pypi/simple" \\
    --extra-index-url "https://user:$FOUNDRY_TOKEN@stack.palantirfoundry.com/artifacts/api/repositories/ri.foundry-sdk-asset-bundle.main.artifacts.repository/contents/release/pypi/simple"

COPY src .
USER 5000
ENTRYPOINT ["python", "app.py"]
```

Then you pass your docker image by passing your `FOUNDRY_TOKEN` in using `--build-arg`:

```sh
FOUNDRY_TOKEN=<your-foundry-token>

docker build --build-arg FOUNDRY_TOKEN=$FOUNDRY_TOKEN -t stack-container-registry.palantirfoundry.com/your-compute-module:0.0.1 .
```
