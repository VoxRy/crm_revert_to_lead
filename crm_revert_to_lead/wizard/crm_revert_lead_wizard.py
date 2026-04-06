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

        # Filter: only records that are currently of type 'opportunity'
        valid_leads = leads.filtered(
            lambda l: l.type == 'opportunity'
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

        for lead in valid_leads:
            # Handle stage history if the module is installed
            if hasattr(self.env['crm.lead'], 'cr_crm_stage_change_history_ids'):
                # Update the previous entry's date_out
                last_history = self.env['cr.crm.stage.change.history'].search([
                    ('crm_lead_id', '=', lead.id)
                ], limit=1, order='id desc')
                if last_history:
                    last_history.write({
                        'date_out': fields.Datetime.now(),
                        'date_out_by_id': self.env.user.id,
                    })

                # Create a new entry for "Lead" using original creation date
                self.env['cr.crm.stage.change.history'].create({
                    'crm_lead_id': lead.id,
                    'stage_name': _('Lead'),
                    'date_in': lead.create_date or fields.Datetime.now(),
                    'date_in_by_id': self.env.user.id,
                })
            lead.write({'type': 'lead'})
        
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
