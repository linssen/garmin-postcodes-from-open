import csv
import itertools
import os
import subprocess
import sys
from typing import List


from bng_to_latlon import OSGB36toWGS84


def main() -> None:
    files = convert_postcodes()
    create_gpi(files)


def convert_postcodes() -> List[str]:
    fieldnames = [
        'Postcode', 'Positional_quality_indicator', 'Eastings', 'Northings',
        'Country_code', 'NHS_regional_HA_code', 'NHS_HA_code',
        'Admin_county_code', 'Admin_district_code', 'Admin_ward_code'
    ]

    sys.stdout.write('Finding CSV files...\n')
    csvs = []
    for root, dirs, files in os.walk(os.path.join('download', 'CSV')):
        csvs.extend(os.path.join(root, f) for f in files if f.endswith('csv'))
    num = len(csvs)
    sys.stdout.write('Converting %d CSV files...\n' % num)
    for idx, file_path in enumerate(csvs):
        locations = []
        sys.stdout.write('{0:.0%} ({1}/{2}) {3}\n'.format(
            (idx + 1) / num, idx + 1, num, file_path,
        ))
        # Read the OSGB36 file
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f, fieldnames=fieldnames)
            for row in reader:
                lat, lng = OSGB36toWGS84(
                    int(row['Eastings']),
                    int(row['Northings'])
                )
                locations.append((row['Postcode'], lng, lat))
        # Write the WGD84 file with the same name
        with open(os.path.join('download', 'latlng', file_path), 'w') as f:
            writer = csv.DictWriter(f, fieldnames=['lat', 'lng', 'postcode'])
            for postcode, lng, lat in locations:
                writer.writerow({'postcode': postcode, 'lng': lng, 'lat': lat})
    return csvs


def create_gpi(files: List[str]) -> None:
    # gpsbabel -i csv -f a.csv -f b.csv -f c.csv -o garmin_gpi,category="Postcodes" -F postcodes.gpi
    sys.stdout.write('Writing GPI file from %d csv files\n' % len(files))
    in_args = [
        ['-f', './download/latlng/%s' % os.path.basename(f)]
        for f in files
    ]

    subprocess.run([
        'gpsbabel',
        '-i', 'csv',
    ] + list(itertools.chain(*in_args)) + [
        '-o', 'garmin_gpi,category="Postcodes"',
        '-F', './download/postcodes.gpi'
    ])


if __name__ == '__main__':
    main()
