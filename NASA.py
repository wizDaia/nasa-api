import requests
from datetime import datetime

def get_date_range():
    
    start_date = datetime.fromisoformat(input('Enter start date (YYYY-MM-DD): ')).date()
    end_date = datetime.fromisoformat(input('Enter end date (YYYY-MM-DD): ')).date()
    assert end_date > start_date, 'End date must be greater than start date.'
    
    return start_date, end_date

def _extract_data(near_earth_objects):
    asteroid_dict = {}

    for date in near_earth_objects:
        for entry in near_earth_objects[date]:
            key_dict = date
            temp_dict = {'neo_reference_id': entry['neo_reference_id'],
                         'name': entry['name'],
                         'absolute_magnitude_h': entry['absolute_magnitude_h'],
                         'is_potentially_hazardous_asteroid': entry['is_potentially_hazardous_asteroid']}
            asteroid_dict.setdefault(key_dict, []).append(temp_dict)
    dict1 = dict(sorted(asteroid_dict.items(), key=lambda item: len(item)))
      
    for d in dict1:
        dict1[d].sort(key=lambda x: x['absolute_magnitude_h'], reverse=True)
    return dict1


def get_data_dictionary(start_date, end_date):
    path = 'https://api.nasa.gov/neo/rest/v1/feed?start_date={}&end_date={}&api_key=DEMO_KEY'
    url = path.format(start_date, end_date)
    rsp = requests.get(url)

    neo = rsp.json()['near_earth_objects']
    asteroid_dict = _extract_data(neo)

    return asteroid_dict

def main():
    start_date, end_date = get_date_range()
    data = get_data_dictionary(start_date, end_date)
    res = {}
    limit = int(input('Enter limit: '))
    for d in data:
        for l in data[d]:
            res[d + " " + l['neo_reference_id']] = {'name': l['name'],
                    'absolute_magnitude_h': l['absolute_magnitude_h'],
                    'is_potentially_hazardous_asteroid': l['is_potentially_hazardous_asteroid']}
    count = 0
    
    for r in res:
        if count < limit:
            print('{}:{}'.format(r, res[r]))
            count += 1
            

if __name__ == '__main__':
    main()