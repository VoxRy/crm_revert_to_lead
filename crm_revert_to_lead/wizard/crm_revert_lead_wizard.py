# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class CrmRevertLeadWizard(models.TransientModel):
    _name = 'crm.revert.lead.wizard'
    _description = 'Wizard to Revert Opportunity to Lead'

    lead_id = fields.Many2one('crm.lead', string='Lead', required=False)

    def action_confirm_revert(self):
        # Determine the records to process: either from the wizard's lead_id, 
        # or from active_ids if triggered from the Action menu.
        active_ids = self._context.get('active_ids', [])
        if self.lead_id:
            leads = self.lead_id
        elif active_ids:
            leads = self.env['crm.lead'].browse(active_ids)
        else:
            return {'type': 'ir.actions.act_window_close'}

        # Filter: only opportunities in the first two stages (sequence <= 2)
        # and only records that are currently of type 'opportunity'
        valid_leads = leads.filtered(
            lambda l: l.type == 'opportunity' and l.stage_id.sequence <= 2
        )

        if not valid_leads:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('No Valid Opportunities'),
                    'message': _('No selected records meet the criteria to be reverted to leads.'),
                    'type': 'danger',
                    'sticky': False,
                    'next': {'type': 'ir.actions.act_window_close'}
                }
            }

        valid_leads.write({'type': 'lead'})
        
        count = len(valid_leads)
        message = _('One opportunity has been successfully reverted to a lead.') if count == 1 else \
                  _('%s opportunities have been successfully reverted to leads.') % count

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Reverted to Lead'),
                'message': message,
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'}
            }
        }
