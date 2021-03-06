import datetime
import lxml.html
import re

from billy.scrape.legislators import LegislatorScraper, Legislator


PARTY_DICT = {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent'}

class WILegislatorScraper(LegislatorScraper):
    state = 'wi'
    latest_only = True

    def scrape(self, chamber, term):

        if chamber == 'upper':
            url = "http://legis.wi.gov/w3asp/contact/legislatorslist.aspx?house=senate"
        else:
            url = "http://legis.wi.gov/w3asp/contact/legislatorslist.aspx?house=assembly"

        with self.urlopen(url) as body:
            page = lxml.html.fromstring(body)

            for row in page.cssselect("#ctl00_C_dgLegData tr"):
                if len(row.cssselect("td a")) > 0:
                    rep_url = list(row)[0].cssselect("a[href]")[0].get("href")
                    rep_url = 'http://legis.wi.gov/w3asp/contact/' + rep_url

                    legpart = re.findall(r'([\w\-\,\s\.]+)\s+\(([\w])\)', list(row)[0].text_content())
                    if legpart:
                        full_name, party = legpart[0]

                        # skip if the legislator is vacant
                        if full_name == 'Vacant':
                            continue

                        party = PARTY_DICT[party]

                        district = str(int(list(row)[2].text_content()))

                        leg = Legislator(term, chamber, district, full_name,
                                         party=party, url=rep_url)
                        leg.add_source(rep_url)

                        leg = self.add_committees(leg, rep_url, term, chamber)
                        self.save_legislator(leg)

    def add_committees(self, legislator, rep_url, term, chamber):
        url = rep_url + '&display=committee'
        with self.urlopen(url) as body:
            body = unicode(body, 'latin-1')
            doc = lxml.html.fromstring(body)

            img = doc.xpath('//img[@id="ctl00_C_picHere"]/@src')
            if img:
                legislator['photo_url'] = img[0]

            cmts = doc.cssselect("#ctl00_C_lblCommInfo a")
            for c in cmts:
                c = c.text_content().split('(')[0].strip()
                # skip subcommittees -- they are broken
                if 'Subcommittee' in c:
                    continue

                if 'Joint' in c or 'Special' in c:
                    c_chamber = 'joint'
                else:
                    c_chamber = chamber
                legislator.add_role('committee member', term, committee=c,
                                    chamber=c_chamber)
            return legislator
