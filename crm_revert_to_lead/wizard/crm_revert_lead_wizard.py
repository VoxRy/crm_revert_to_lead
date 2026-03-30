# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class CrmRevertLeadWizard(models.TransientModel):
    _name = 'crm.revert.lead.wizard'
    _description = 'Wizard to Revert Opportunity to Lead'

    lead_id = fields.Many2one('crm.lead', string='Lead', required=True)

    def action_confirm_revert(self):
        self.ensure_one()
        # Change the type to 'lead' using write to avoid UI onchange triggers
        # and specifically update ONLY the type field to keep everything else.
        self.lead_id.write({'type': 'lead'})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Reverted to Lead'),
                'message': _('The opportunity has been successfully reverted to a lead.'),
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'}
            }
        }
