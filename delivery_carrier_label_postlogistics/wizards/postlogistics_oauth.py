# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import requests

from odoo import models, fields, api

from requests_oauthlib import OAuth2Session


class PostlogisticsAuth(models.TransientModel):
    _name = 'postlogistics.auth'
    _description = 'Postlogistics Auth'

    client_id = fields.Char(
        string='Client ID',
        required=True,
    )

    client_secret = fields.Char(
        string='Client Secret',
        required=True,
    )

    state = fields.Selection([
        ('todo', 'OAuth Config'),
        ('done', 'Complete')
    ], default='todo')

    @api.multi
    def generate_access_token(self):
        authorization_base_url = (
            'https://wedec.post.ch/WEDECOAuth/authorization'
        )
        token_base_url = (
            'https://wedec.post.ch/WEDECOAuth/token'
        )

        # # 3.3.1 Authentication request
        # authentication_session = OAuth2Session(self.client_id)
        # authorization_url, authentication_state = (
        #     authentication_session.authorization_url(authorization_base_url)
        # )
        #
        # # 3.3.2 Authentication response
        # authorization_response = requests.get(authorization_url)
        #
        # # 3.3.3 Authentication response validation
        # if authorization_response.status_code != 302:
        #     raise
        # location_url = authorization_response.headers['Location']
        # if not location_url:
        #     raise
        #
        # # 3.3.4 Token request
        # token_session = OAuth2Session(
        #     self.client_id,
        #     state=authentication_state
        # )
        # token = token_session.fetch_token(
        #     token_base_url,
        #     client_secret=self.client_secret,
        #     authorization_response=location_url
        # )
        #
        # # 3.3.5 Token response
        # token_response = requests.post(token.url)
        #
        # # 3.3.6 Token response validation
        # if token_response.status_code != 200:
        #     raise
        # id_token = token_response.headers['id_token']
        # if not id_token:
        #     raise
        # access_token = token_response.headers['access_token']
        # if not access_token:
        #     raise
        #
        # # Save the access token
        # icp = self.env['ir.config_parameter']
        # icp.set_param('postlogistics.oauth.token', access_token)

        # Define configuration as done
        self.state = 'done'

        # Display configuration
        act = self.env['ir.actions.act_window'].for_xml_id(
            'delivery_carrier_label_postlogistics', 'action_postlogistics_auth'
        )
        act['res_id'] = self.id
        return act
