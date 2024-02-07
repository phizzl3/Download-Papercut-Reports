"""

Checks to see if a json file exists at json_path, and returns a 
python data type of the contents read from the json file. If the 
json file doesn't exist, outputs json file using the python data 
type (json compatible) optionally passed as default_data, then 
loads from the file.

Args:
    json_path (Path): pathlib.Path pointing to json file location.
    
    default_data (any, optional): python data type (json compatible) 
    to output to json file. Defaults to None.

Returns:
    any: python data type read from json data.
    
"""

__version__ = "1.0.2 - Modified"

import json
from pathlib import Path

from modules import display


def loadjson(json_path: Path, default_data=None):
    """Checks to see if a json file exists at json_path, and returns a
    python data type of the contents read from the json file. If the
    json file doesn't exist, outputs json file using the python data
    type (json compatible) optionally passed as default_data, then
    loads from the file.

    Args:
        json_path (Path): pathlib.Path pointing to json file location.
        default_data (any, optional): python data type (json compatible) to
        output to json file. Defaults to None.

    Returns:
        any: python data type read from json data.
    """
    # Convert to Path if passed as str
    if not isinstance(json_path, Path):
        json_path = Path(json_path)
    # Checks to see if the target file exists and creates
    # the folder path if it doesn't exist.
    if not json_path.exists():
        if not json_path.parent.is_dir():
            json_path.parent.mkdir(parents=True)

        if default_data:
            # Writes the python data to output json file.
            with open(json_path, "w", encoding="utf-8") as json_file:
                json.dump(default_data, json_file, indent=2)
            display.readme()
            print(
                f"""
                Default config.json written to the following directory:\n
                [ {json_path} ]\n
                Exit this program and navigate to that file and update
                it with the correct query information before running.
                (Specifically, update the email address listed.)
                You should also verify your credentials.json file is present
                in the same directory as it is required to access Gmail's API.
                (View README.md for details.)
                This program should run without you updating the config, but
                it will never find any matching messages.
                """
            )
            input()

    # Load the data from the json file at the target location.
    try:
        with open(json_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except json.decoder.JSONDecodeError:
        print(
            """
            Error loading json data. Check your json for formatting errors.
            Verify that you don't have any missplaced/missing/trailing commas, etc.
            Close this program and make any necessary corrections and run again. 
            If you want to revert to the defaults, delete your current config.json
            and then run the program again.
            """
        )
        input()
