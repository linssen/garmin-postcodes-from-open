import csv
import os
import sys

from bng_to_latlon import OSGB36toWGS84


def get_postcodes():
    fieldnames = [
        'Postcode', 'Positional_quality_indicator', 'Eastings', 'Northings',
        'Country_code', 'NHS_regional_HA_code', 'NHS_HA_code',
        'Admin_county_code', 'Admin_district_code', 'Admin_ward_code'
    ]
    locations = []

    sys.stdout.write('Finding CSV files...\n')
    for root, dirs, files in os.walk(os.path.join('download', 'CSV')):
        for file_path in (name for name in files if name.endswith('csv')):
            with open(os.path.join(root, file_path), 'r') as csv_file:
                reader = csv.DictReader(csv_file, fieldnames=fieldnames)
                for row in reader:
                    lat, lng = OSGB36toWGS84(
                        int(row['Eastings']),
                        int(row['Northings'])
                    )
                    locations.append((row['Postcode'], lng, lat))

    sys.stdout.write('\nWriting {0} postcodes to csv'.format(len(locations)))
    with open(os.path.join('download', 'all-postcodes.csv'), 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['lat', 'lng', 'postcode'])
        for postcode, lng, lat in locations:
            writer.writerow({'postcode': postcode, 'lng': lng, 'lat': lat})
    sys.stdout.write('\nDone!\n')
    sys.exit(0)


if __name__ == '__main__':
    get_postcodes()
