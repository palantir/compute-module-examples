# platform-apis

This repo contains a working example of how to call Foundry Platform APIs from a compute module.

Assumes you are running Functions mode with Application Permissions.

## Set up

### Configure your compute module   

Go to your compute module's `Configure` tab. 

In the Execution mode card: 

1. Select `Functions module` as the Execution mode
2. Select `Application's permissions` under permissions
3. Select `Create new credentials`

### Grant access to the Application User
The client ID created in your App needs to have access to whatever data resources you've added if you want the SDK to be able to access those objects/actions/etc. You can do this by going to the "Security" tab of the given resource, searching for your app's client ID (found under the `OAuth & Scopes` tab of the application), then adding that user. 

### Add environment variables
This example depends on a `FOUNDRY_URL` environment variable.
 
1. Upload this image as a container 
2. Select the `Configure` tab
3. Click the new container's row
4. Select `Add Foundry URL` in the environment variables section 