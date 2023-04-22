This is a simple script that automates uploading your meter reading to the evcounter platform.

Simply download the python script and fill in the right value for these variables:
 * `wallbox_ip`: should be the ip address of your wallbox
 * `username`: your username for the evcounter platform
 * `password`: your password for the evcounter platform

Save the file in a suitable location (e.g. `~/meter/meter.py`)

Next set up a cronjob:
 * `crontab -e`
 * Append this line to the end of the file: 
 ```0 */4 * * * python ~/meter/meter.py```
 * Save your new config.

This will ensure that the script is run every 4 hours. It will check to see if your meter has a new reading and, if so, upload it to evcounter.
