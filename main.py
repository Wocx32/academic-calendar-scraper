import requests
import bs4
import datetime
from zoneinfo import ZoneInfo

endpoint = 'https://www.fccollege.edu.pk/academic-calendar/'

req = requests.get(endpoint)
soup = bs4.BeautifulSoup(req.content, 'html.parser')


data = []

table = soup.find('table')
table_body = table.find('tbody')

rows = table_body.find_all('tr')

for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append(cols)



def current_semester(override=None):

    format = '%a %d %b %y %z'

    if not override:
        datetime_obj_today = datetime.datetime.now(tz=ZoneInfo('Asia/Karachi'))
    else:
        datetime_obj_today = datetime.datetime.strptime(f'{override} +0500', format)
        
    terms = data[2]
    terms = [term.split('-') for term in terms if term]

    indices = [6, 17, 27]
    sem = ''
    prev = None

    for term_index, i in enumerate(range(1, len(data[indices[0]]), 2)):
        
        for idx in indices:
            
            if idx == 6:
                sem = 'FA'
            elif idx == 17:
                sem = 'SP'
            elif idx == 27:
                sem = 'SU'

            if idx == 6:
                start_year = terms[term_index][0][-2:]
                end_year = terms[term_index][1][-2:]
            else:
                start_year = end_year = terms[term_index][1][-2:]
            
            start_date_string = data[idx][i].split(' ')
            start_date_string[2] = start_date_string[2][:3]
            start_date_string = ' '.join(start_date_string)

            end_date_string = data[idx][i+1].split(' ')
            end_date_string[2] = end_date_string[2][:3]
            end_date_string = ' '.join(end_date_string)

            
            start_datetime_obj = datetime.datetime.strptime(f'{start_date_string} {start_year} +0500', format)
            end_datetime_obj = datetime.datetime.strptime(f'{end_date_string} {end_year} +0500', format)

            if start_datetime_obj <= datetime_obj_today <= end_datetime_obj or datetime_obj_today < start_datetime_obj:
                return start_datetime_obj.strftime('%Y'), sem

            prev = start_datetime_obj

    return prev.strftime('%Y'), sem


def generate_terms(semester_tuple):
    terms = []
    terms.append(semester_tuple[0]+semester_tuple[1])
    for term in ('PH', 'IE'):
        terms.append(term + semester_tuple[0][-2:] + semester_tuple[1])
    
    return terms

if __name__ == '__main__':
    print(generate_terms(current_semester('Mon 17 Jan 24')))