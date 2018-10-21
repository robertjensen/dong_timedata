import login
import requests
from datetime import datetime


def _find_pod_number(response):
    text = response.text
    podnumber_start = text.find("'", text.find('podNumber'))
    podnumber_end = text.find("'", podnumber_start + 1)
    assert(podnumber_start > 0)
    podnumber = text[podnumber_start+1:podnumber_end]
    return podnumber


def read_my_consumption(kundenummer, aftagenummer):
    URL = 'https://orsted.dk/Privat/Kundeservice/Selvbetjening/Se-dit-forbrug'
    DATA_URL = ('https://orsted.dk/api/feature/consumption/exportcsv?' +
                'podnumber={}&granularity=hour&' +
                'from=2018-10-01T10:33:54.440Z&to=2018-10-19T20:33:54.440Z')

    r = requests.get(URL)
    token_pos = r.text.find('__RequestVerificationToken')
    value_pos = r.text.find('value', token_pos) + len('value="')
    value_pos_end = r.text.find('"', value_pos+2)
    token = r.text[value_pos:value_pos_end]
    login_data = {'CustomerNumber': str(kundenummer),
                  'PointOfDeliveryNumber': str(aftagenummer),
                  'RememberMeBusiness': 'False',
                  'submittingBusinessData': 'Log ind',
                  'fhController': 'MaineAuthenticationController',
                  'fhAction': 'ShowLoginBox',
                  '__RequestVerificationToken': token}

    with requests.session() as s:
        r = s.post(URL, login_data)
        r = s.get(URL)
        podnumber = _find_pod_number(r)

        csv_data = s.get(DATA_URL.format(podnumber))

    for hour in csv_data.text.split('\r\n'):
        print(hour.split(';'))


if __name__ == '__main__':
    read_my_consumption(login.kundenummer, login.aftagenummer)
