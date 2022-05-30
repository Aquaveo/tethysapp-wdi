"""
********************************************************************************
* Name: __init__.py
* Author: msouff
* Created On: Dec 2, 2019
* Copyright: (c) Aquaveo 2019
********************************************************************************
"""
import argparse
from tethysapp.wdi.cli.init_command import init_wdi


def wdi_command():
    """
    wdi commandline interface function.
    """
    # Create parsers
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='Commands')
    # init command ----------------------------------------------------------------------------------------------------#
    init_parser = subparsers.add_parser(
        'init',
        help="Initialize the wdi app."
    )
    init_parser.add_argument(
        'gsurl',
        help='GeoServer url to geoserver rest endpoint '
             '(e.g.: "http://admin:geoserver@localhost:8181/geoserver/rest/").'
    )
    init_parser.set_defaults(func=init_wdi)

    # Parse commandline arguments and call command --------------------------------------------------------------------#
    args = parser.parse_args()
    args.func(args)
