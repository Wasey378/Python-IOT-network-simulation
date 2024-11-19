import json
import logging
from logging.handlers import SysLogHandler
# Initialize the SysLogHandler
syslog_handler = SysLogHandler(address=("192.168.0.103", 514))

# Initialize the logger
logger = logging.getLogger()
logger.addHandler(syslog_handler)
logger.setLevel(logging.INFO)

# Read JSON data from a file line by line
json_file_path = "ddos_events.json"

try:
    with open(json_file_path, "r") as json_file:
        for line in json_file:
            try:
                # Parse JSON from each line
                json_data = json.loads(line)

                # Log information for each line
                logger.info(json_data )

            except json.JSONDecodeError:
                logger.error(f"data: {line.strip()}")

except FileNotFoundError:
    logger.error(f"File not found: {json_file_path}")

