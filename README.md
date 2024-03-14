# RoboRobot

Discord bot created to interact with servers and Twitch streams.

## Getting OAuth Token

Follow instructions under 'Implicit Grant Flow' at the [Twitch Docs](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/).

Your resulting URI should look like:

```
https://id.twitch.tv/oauth2/authorize
    ?response_type=token
    &client_id=<YOUR APP CLIENT ID HERE>
    &redirect_uri=http://localhost:3000
    &scope=channel_editor
    &response_type=token
```

You will need to click 'Authorize' and a blank page will be presented.
You will find the response URI in your address bar and it should look like:

```
http://localhost:3000/
    #access_token=<YOUR TOKEN IS HERE (from the equals to the ampersand)>
    &scope=channel_editor
    &token_type=bearer
```

Copy your access token & add it into the secrets.yaml file.
