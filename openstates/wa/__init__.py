metadata = dict(
    name='Washington',
    abbreviation='wa',
    legislature_name='Washington State Legislature',
    upper_chamber_name='Senate',
    lower_chamber_name='House of Representatives',
    upper_chamber_title='Senator',
    lower_chamber_title='Representative',
    upper_chamber_term=4,
    lower_chamber_term=2,
    terms=[
        {'name': '2009-2010', 'start_year': 2009, 'end_year': 2010,
         'sessions': ['2009-2010']},
        {'name': '2011-2012', 'start_year': 2011, 'end_year': 2012,
         'sessions': ['2011-2012']},
        ],
    session_details = {
        '2009-2010': {'display_name': '2009-2010 Regular Session',
                      '_scraped_name': '2009-10',
                     },
        '2011-2012': {'display_name': '2011-2012 Regular Session',
                      '_scraped_name': '2011-12',
                     },
    },
    feature_flags = ['events', 'subjects'],
    _ignored_scraped_sessions=['2007-08'],
)

def session_list():
    from billy.scrape.utils import url_xpath
    return url_xpath('http://apps.leg.wa.gov/billinfo/',
     '//td[starts-with(@id, "ctl00_ContentPlaceHolder1_TabControl1")]/text()')

