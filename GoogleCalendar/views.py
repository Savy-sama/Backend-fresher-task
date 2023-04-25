from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.shortcuts import redirect
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import os


# Set to True to enable OAuthlib's HTTPs verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


class GoogleCalendarInitView(View):
    """
    Initiate the OAuth2 authorization flow.
    """

    def get(self, request, *args, **kwargs):
        # Create a flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
        flow = InstalledAppFlow.from_client_secrets_file('credential.json',
            scopes=['https://www.googleapis.com/auth/calendar.events']
        )

        # The URI created here must exactly match one of the authorized redirect URIs
        # for the OAuth 2.0 client, which you configured in the API Console. If this
        # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
        # error.
        flow.redirect_uri = 'http://localhost:8000/rest/v1/calendar/redirect'

        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true',
        )

        # Store the state so the callback can verify the auth server response.
        request.session['state'] = state

        # Redirect the user to the authorization URL.
        return redirect(authorization_url)


