# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import json
import requests

from odoo import models, fields, api


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

        authentication_url = 'https://wedecint.post.ch/WEDECOAuth/token'

        response = requests.post(
            url=authentication_url,
            headers={'content-type': 'application/x-www-form-urlencoded'},
            data={
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': 'WEDEC_BARCODE_READ',
            },
            timeout=60,
        )

        if response.status_code != 200:
            raise

        response_dict = json.loads(response.content.decode("utf-8"))
        access_token = response_dict['access_token']

        if not access_token:
            raise

        # Save the client credentials token
        icp = self.env['ir.config_parameter']
        icp.set_param('postlogistics.oauth.client_id', self.client_id)
        icp.set_param('postlogistics.oauth.client_secret', self.client_secret)

        # Define configuration as done
        self.state = 'done'

        # Display configuration
        act = self.env['ir.actions.act_window'].for_xml_id(
            'delivery_carrier_label_postlogistics', 'action_postlogistics_auth'
        )
        act['res_id'] = self.id
        return act
