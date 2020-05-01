[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/rshad/Extract-Information-from-Log-files-using-Python/blob/master/LICENSE)
# Extract data from Log file and Parse it using Python

### Project Description
Extract the last alert, found after a date, given as a parameter. In this case the file is .log file, and was tested with Wazuh agent log file.

### Directory structure
* In `/src` you can find the source code of the script.
* In `/output` you can find an example of the output after running the script
* In `/data` you can find the log file to be parsed.

### How to run it
An example to run the log, can be like:
```
python getLastAlertLog.py -i ../data/alerts.log -o ../output/lastAlert.txt -d 2018/01/14
```

