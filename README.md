# Download and convert UK postcodes to Garmin .gpi file

## Instructions

1. Download CSV data from https://www.ordnancesurvey.co.uk/business-government/products/code-point-open
1. Extract files to `download/CSV` directory
1. Run `docker compose up`
1. When that completes, run `docker compose run gpsbabel bash`
1. In the shell, run `gpsbabel -i csv -f all-postcodes.csv -o garmin_gpi,category="Postcodes" -F postcodes.gpi`
1. Wait a very long time for that to complete
1. Copy the resulting `postcodes.gpi` file that will be written to the `downloads` folder to your Garmin's SD card at the location `Garmin/POI/postcodes.gpi`.
1. Disconnect and reboot the unit
