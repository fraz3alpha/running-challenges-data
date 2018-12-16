
import xml.etree.ElementTree as ET
import json
import os

from bs4 import BeautifulSoup

def parse_special_events_table(table, dates):
    special_events = dict()

    table_rows = table.find_all('tr')

    print('{} table rows found'.format(len(table_rows)))

    if table_rows:
        column_map = dict()
        event_types = dict()
        header_row = table_rows[0]

        for index, th in enumerate(header_row.find_all('th')):
            column_heading = th.get_text().strip()
            column_map[column_heading] = index
            # The first two colums contain the event, the later columns contain
            # the events which vary between countries
            if index >= 2:
                event_types[column_heading] = {
                    'index': index,
                    'date': dates.get(column_heading, None),
                    'events': dict()
                }



        # print(column_map)
        print(event_types)

        content_rows = table_rows[1:]
        print('{} content rows found'.format(len(content_rows)))
        for r in content_rows:
            cells = r.find_all('td')
            event = cells[column_map['Event']].get_text().strip()

            for special_event_type in event_types.keys():
                event_time = cells[column_map[special_event_type]].get_text().strip()
                if len(event_time) > 2:
                    # print('{} @ {}'.format(special_event_type, event_time))
                    event_types[special_event_type]['events'][event] = event_time

        # print(event_types)
        # for event_type in event_types:
        #     print('{} x{}'.format(event_type, len(event_types[event_type]['events'])))

    return event_types


year_details = {
    'string': '2018-19',
    'dates': {
        'Christmas Day': '2018-12-25',
        'New Year\'s Day': '2019-01-01',
        'Christmas Eve': '2018-12-24',
        'Thanksgiving': '2018-11-22'
    }

}

# Load the entire page, in all its messy glory

input_files = dict()

raw_data_directory = '../../data/parkrun-special-events/{}/raw/'.format(year_details['string'])
for file in os.listdir(raw_data_directory):
    if file.endswith('.html'):
        # String the ending off
        country_code = os.path.splitext(file)[0]
        input_files[country_code] = os.path.join(raw_data_directory, file)

print(input_files)

all = dict()

for country_code, raw_file_path in input_files.items():

    print('Processing {} - {}'.format(country_code, raw_file_path))

    soup = None
    with open(raw_file_path, 'r') as FH:
        html_doc = FH.read()
        soup = BeautifulSoup(html_doc, 'html.parser')

    # Find the 'results' table that contains the data for what parkruns are putting
    # on the special events
    main_table = soup.find_all(id="results")
    print('{} matching tables found'.format(len(main_table)))

    # Assume it is the only table
    if len(main_table) >= 1:
        special_events = parse_special_events_table(main_table[0], year_details['dates'])

        # Merge this country's special events into the master list
        for event_type, event_details in special_events.items():
            # If this event, e.g. Christmas Day is not known about yet, then
            # pre-populate it with this country's info
            if event_type not in all:
                all[event_type] = event_details
            # Else, append the lists of parkrun events from this country to the
            # existing list
            else:
                all[event_type]['events'].update(event_details['events'])

        with open('../../data/parkrun-special-events/2018-19/parsed/{}.json'.format(country_code), 'w') as FH:
            json.dump(special_events, FH, sort_keys=True, indent=2)
    # print(json.dumps(geo_data, sort_keys=True, indent=2))

# Worldwide summary:
for event_type, event_details in all.items():
    print('{} - {} events'.format(event_type, len(event_details['events'])))

with open('../../data/parkrun-special-events/2018-19/parsed/all.json', 'w') as FH:
    json.dump(all, FH, sort_keys=True, indent=2)

# print(soup.prettify())

exit(0)
