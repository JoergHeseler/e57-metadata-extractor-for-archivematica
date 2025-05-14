# Title: e57-validator
# Version: 1.0.0
# Publisher: NFDI4Culture
# Publication date: May 6, 2025
# Author: Joerg Heseler
# License: CC BY-SA 4.0

from __future__ import print_function
import json
import subprocess
import sys
import re
import platform


class E57ValidatorException(Exception):
    pass

def get_validator_path_from_arguments():
    for arg in sys.argv:
        if arg.lower().startswith("--validator-path="):
            return arg.split("=", 1)[1].rstrip('/\\')
    return '/usr/share'

def parse_e57_validator_data(target):
    try:
        validator_file = 'e57validate.exe'
        validator_file_path = get_validator_path_from_arguments()
        if platform.system() == 'Windows':
            args = [get_validator_path_from_arguments() + '\\' + validator_file, '-i', target]
        else:
            args = ['wine', get_validator_path_from_arguments() + '/' + validator_file, '-i', target]
        return subprocess.check_output(args).decode("utf8")
    except FileNotFoundError:
        raise E57ValidatorException("e57validate not found. Use --validator-path= to specify its path.")
    except subprocess.CalledProcessError as e:
        return e.stdout.decode("utf8")

def get_error_count(doc):
    try:
        error_count = int(re.search("Error count: .*?(\d+)", doc).group(1))
    except:
        return 1
    return error_count

def get_outcome(error_count):
    if error_count == 0:
        return "pass"
    else:
        return "fail"

def format_event_outcome_detail_note(format, version, result):
    note = 'format="{}";'.format(format)
    if version is not None:
        note = note + ' version="{}";'.format(version)
    note = note + ' result="{}"'.format(result)

    return note

def main(target):
    try:
        result = parse_e57_validator_data(target)
        error_count = get_error_count(result)
        version = '1.0'
        format = 'E57'
        outcome = get_outcome(error_count)
        note = format_event_outcome_detail_note(format, version, result)

        out = {
            "eventOutcomeInformation": outcome,
            "eventOutcomeDetailNote": note
        }
        print(json.dumps(out))

        return 0
    except E57ValidatorException as e:
        return e

if __name__ == '__main__':
    target = sys.argv[1]
    sys.exit(main(target))
