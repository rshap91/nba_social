# README

## PYTHON FACEBOOK-SDK

http://facebook-sdk.readthedocs.io/en/latest/install.html

#### Install

pip install -e git+https://github.com/mobolic/facebook-sdk.git#egg=facebook-sdk


#### Authenticate

# EASY WAY IS JUST GET TOKEN FROM HERE https://developers.facebook.com/tools/explorer/

https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow

https://stackoverflow.com/questions/3058723/programmatically-getting-an-access-token-for-using-the-facebook-graph-api

https://developers.facebook.com/tools/explorer/
http://nodotcom.org/python-facebook-tutorial.html
https://towardsdatascience.com/how-to-use-facebook-graph-api-and-extract-data-using-python-1839e19d6999

Flow:
___Get Code___

GET
https://www.facebook.com/v2.12/dialog/oauth?
  client_id={app-id}
  &redirect_uri={redirect-uri}
  &state={state-param}

state is dict with keys st, dt. Not sure what they have to be, looks like anything.


___Get Access Token___

GET
"https://graph.facebook.com/oauth/access_token?"
  client_id={app-id}
  &redirect_uri={redirect-uri}
  &client_secret={app-secret}
  &code={code-parameter}
