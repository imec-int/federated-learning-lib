#!/usr/bin/env python3
import abc
import os
from pathlib import Path
import logging


logger = logging.getLogger(__name__)


class HelloWorld(abc.ABC):
    def __init__(self, script_name,
                 script_spec,
                 keras_model=None,
                 **kwargs):
        """
        Initializes an `script` object

        :param script_name: String describing the script
        :type script_name: `str`
        :param kwargs: Dictionary of model-specific arguments.
        :type kwargs: `dict`
        """
        self.script_name = script_name
        self.result = "init value"

    def execute(self):
        """
        Execute is a placeholder script for executing python code
        """
        self.result = str("helloWorld")

    def fetch_results(self):
        """
        Fetch results
        placeholder function for returning the results gathered in execute
        passes results on to the party local training handler
        """
        return self.result


if __name__ == '__main__':
    """
    Main function can be used to create an application out
    of our Party class which could be interactive
    """
    logging.info('hello cold cold world')
