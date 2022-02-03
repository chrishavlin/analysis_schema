import argparse
import json

from .schema_model import ytModel
from typing import Union, Optional


def show_plots(schema_result: list, image_type: str):
    """
    This function accepts results of a schema model run, which returns
    a list. This function iterates through the list and displays each output.

    Parameters
    ----------
    schema_result: list
        the result of an analysis schema .run()
    image_type: str
        if "Jupyter" will call show, otherwise save
    """

    for output in schema_result:
        if image_type == "Jupyter":
            output.show()
        if image_type != "Jupyter":
            output.save()


def load_and_run(
    json_file: str, show_plots: Optional[bool] = True, image_type: Optional[str] = None
):
    """
    A function to load the JSON file into the analysis schema model, and
    the run that model to produce an output.

    Parameters
    ----------
    json_file: str
        the json file to load
    show_plots: bool
        if True, will either save or show any resulting plots, depending on
        the value of the `files` parameter (default is True)
    image_type: str
        if show_plots is True, this string determines how the plot is returned.
        If image_type=="Jupyter", the plot will be displayed with .show(),
        otherwise it will be saved to file.
    """

    # open the file where the user is entering values
    with open(json_file, "r") as live_json:
        # assign to a variable
        live_schema = json.load(live_json)
    # remove schema line
    live_schema.pop("$schema")

    result = validate_and_run(live_schema)

    if show_plots:
        show_plots(result, image_type)

    return result


def validate_and_run(json_contents: Union[str, dict]) -> list:
    """
    validates a json string or a python dict as a ytModel then executes
    the model, returning results

    Parameters
    ----------
    json_contents: Union[str, dict]
        either a raw json string or a python dictionary containing json contents

    Returns
    -------
    list
        the results of running the analysis schema, stored in a list
    """

    # this is useful for an api server endpoint
    if isinstance(json_contents, str):
        analysis_model = ytModel.parse_raw(json_contents)
    elif isinstance(json_contents, dict):
        analysis_model = ytModel.parse_obj(json_contents)
    return analysis_model._run()


if __name__ == "__main__":

    # create a parser
    parser = argparse.ArgumentParser(description="Handling Filenames for Analysis")

    # add the JSON file name agrument
    parser.add_argument("JSONFile", help="Call the JSON with the Schema to run")

    parser.add_argument(
        "ImageFormat",
        nargs="*",
        help="Enter 'Jupyter' to run .show() or a filename to run .save()",
    )

    args = parser.parse_args()

    # run the analysis
    _ = load_and_run(args.JSONFile, image_type=args.ImageFormat)
