# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    stage_sequence = fields.Integer(
        related='stage_id.sequence',
        string='Stage Sequence',
        readonly=True
    )

    def action_revert_to_lead(self):
        """
        Opens a confirmation wizard to revert an opportunity back to a lead.
        """
        self.ensure_one()
        return {
            'name': _('Revert to Lead'),
            'type': 'ir.actions.act_window',
            'res_model': 'crm.revert.lead.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_lead_id': self.id,
            }
        }
