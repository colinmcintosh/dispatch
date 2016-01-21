import logging
import sys
from logging.handlers import RotatingFileHandler

import dispatch.exceptions as exceptions



# Configure logging
log_format = logging.Formatter("%(asctime)s [%(name)s.%(funcName)s():%(lineno)d]\n\t%(levelname)8s: %(message)s\n")

logger = logging.getLogger("dispatch")

stderr_handler = logging.StreamHandler()
stderr_handler.setLevel(logging.DEBUG)
stderr_handler.setFormatter(log_format)
logger.addHandler(stderr_handler)

file_handler = RotatingFileHandler("dispatch.log", maxBytes=10000, backupCount=2)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)

logger.setLevel(logging.DEBUG)

logger.info("Logging Configured at Level {}".format(logger.getEffectiveLevel()))


def parse_arguments():
    """Examples:
        $ dispatch ([host:]hostname | [hostfile:]file_path)+ [action:](get|set|create|delete) ([parameter:]parameter[=set_value])+ [option+]
        $ dispatch switch01 get ntp.client.skew
        $ dispatch switch01 switch02 get ntp.client.skew --output=json
        $ dispatch switch01 get interfaces.name network.interface.description network.interface.name
        -- switch01
            network.interface.description = "Connected to the WAN"
            network.interface.name = "Ethernet1/1"
    """

    def find_action_word(args):
        pattern = "^(?:action:)?(get|set|create|delete)$"
        import re
        for i, word in enumerate(args):
            if re.match(pattern, word, re.IGNORECASE):
                return i

    n = find_action_word(sys.argv)
    if n is None:
        raise exceptions.DispatchSyntaxException("Could not find any action word: get, set, create, delete")
    hosts = sys.argv[1:n]   # Get the host list before the action word.
    parameters_and_options = sys.argv[n:]   # Get the list of parameters after the action word.






