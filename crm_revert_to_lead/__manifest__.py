{
    'name': 'CRM Revert to Lead',
    'version': '15.0.1.0.0',
    'category': 'CRM',
    'summary': 'Add a button to revert an opportunity back to a lead',
    'description': """
CRM Revert to Lead
==================
Adds a button on the Opportunity form to revert it back to a Lead.
The button is only visible if the opportunity is in the first two stages of the pipeline.
Changing the type back to Lead preserves all other fields, activities, and messages.
""",
    'author': 'Kais Akram',
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/crm_revert_lead_wizard_views.xml',
        'views/crm_lead_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
