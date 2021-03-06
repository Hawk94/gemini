from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse, redirect
from django.core.urlresolvers import reverse_lazy
from django.views import View
from requests_oauthlib import OAuth2Session

class SalesforceAuthView(LoginRequiredMixin, View):
    login_url = reverse_lazy('account_login')
    redirect_field_name = 'salesforce:oauth'

    def post(self, request, *args, **kwargs):
        callback_uri = settings.SALESFORCE_CALLBACK_URL
        auth_url = settings.SALESFORCE_BASE_URL + settings.SALESFORCE_AUTHORIZATION_URL
        oauth = OAuth2Session(client_id=settings.SALESFORCE_CONSUMER_KEY, redirect_uri='https://toreda.co.uk')
        authorization_url, state = oauth.authorization_url(auth_url)
        request.session['oauth_state'] = state
        return redirect(authorization_url)


class SalesforceCallbackView(LoginRequiredMixin, View):
    login_url = reverse_lazy('account_login')
    redirect_field_name = 'salesforce:callback'

    def save_credentials(self, user, token):
        SalesforceCredential.objects.create(user=user,
                                            id_url = token['id'],
                                            issued_at = token['issued_at'],
                                            scope = token['scope'],
                                            instance_url = token['instance_url'],
                                            token_type = token['token_type'],
                                            refresh_token = token['refresh_token'],
                                            id_token = token['id_token'],
                                            signature = token['signature'],
                                            access_token = token['access_token'])

    def get(self, request, *args, **kwargs):
        oauth = OAuth2Session(client_id=settings.SALESFORCE_CONSUMER_KEY, state=request.session['oauth_state'])
        token = oauth.fetch_token(token_url, client_secret=settings.SALESFORCE_CONSUMER_SECRET,
                                  authorization_response=request.url)
        request.session['oauth_token'] = token
        self.save_credentials(request.user, request.oauth_token)
        return redirect('home')
