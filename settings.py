from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {

    'participation_fee': 0.00,
    'doc': "",

}

SESSION_CONFIGS = [
    {
        'name': 'cheating_entitlement_ret',
        'display_name': "Cheating_Entitlement_RET",
        'num_demo_participants': 12,
        'real_world_currency_per_point': 0.002,
        'app_sequence': ['M1_dictator',
                         'M2_die_match_RET',
                         'M3_die_match_progressive_RET',
                         'M4_risk_pref',
                         'M5_number_add1',
                         'M5_number_add2',
                         'M5_number_add3',
                         'M5_number_add4',
                         'M5_number_add5',
                         'LastModel'],
        
    },
     {'name': 'cheating_entitlement_dieroll',
        'display_name': "Cheating_Entitlement_DieRoll",
        'num_demo_participants': 6,
        'real_world_currency_per_point': 0.0033,
        'app_sequence': ['M1_dictator',
                         'M2_die_match_dieroll',
                         'M3_die_match_progressive_dieroll',
                         'M4_risk_pref',
                         'M5_number_add1',
                         'M5_number_add2',
                         'M5_number_add3',
                         'M5_number_add4',
                         'M5_number_add5',
                         'LastModel_RET'],
    },
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
POINTS_CUSTOM_NAME = 'ECUs'
USE_POINTS = True

ROOMS = []


# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')


# Consider '', None, and '0' to be empty/false
# DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})
DEBUG = 1
DEMO_PAGE_INTRO_HTML = """ """

# don't share this with anybody.
SECRET_KEY = 'wl_6r27l8&3%u4%%=c1h6tdr+k26*d)vl%j8(9!t4ei@-lle8!'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
