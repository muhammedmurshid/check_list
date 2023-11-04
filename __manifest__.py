{
    'name': "Check List",
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['base', 'mail'],
    'data': [
        # 'data/activity_leads.xml',
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'views/check_list.xml',
        'views/class_rooms.xml',
        'views/works.xml',
        'views/work_lists.xml',
    ],

    'demo': [],
    'summary': "logic_check_list",
    'description': "logic_dauly_activities",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': False
}
