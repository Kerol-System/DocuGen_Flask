"""The SwiftDoc Project."""

import logging
import logging.config
import os
import platform
import sys
import time

import requests
import shutil

logging.config.fileConfig(
    "logging.conf",
    defaults={"logfilename": "SwiftDoc.log"},
    disable_existing_loggers=False,
)
logger = logging.getLogger(__name__)


class PanHelpers:
    """Things for preparing logs, connecting to devices, etc."""

    # current_dir = str(pathlib.Path(__file__).parents[1])
    my_separator = "/"  # default to Linux/Mac

    if os.name != "posix":
        my_separator = "\\"
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + my_separator + 'flask-swiftdoc-1.0'
    customer = "Secured by Palo Alto Networks"
    date_string = ""
    input_path = ""
    output_path = ""
    tmp_path = ""
    save_temp_dir = False  # Set this to true if you want to preserve the temp files for some reason.

    def debug_info(self):
        """Method to log some end user details."""
        logger.info("Running on platform: %s", platform.platform())
        logger.info("Python version: %s", platform.python_version())
        logger.info("Requests module version: %s", requests.__version__)

    def set_separator(self):
        """Slash or backslash depending on if it's Linux, Mac, or other OS."""
        if os.name != "posix":
            self.my_separator = "\\"
        logger.debug("Separator set to: %s", self.my_separator)

    def set_path(self, psusername):
        """Update the input file/yaml path if this is a posix system.

        https://security.openstack.org/guidelines/dg_using-temporary-files-securely.html
        # script_path = sys.path[0]  # Refers to the directory of where this script gets executed
        # logger.debug("os name: %s", os.name) # leaving this here to debug other OS
        """
        self.input_path = (
            self.current_dir + self.my_separator + f"uploads{psusername}" + self.my_separator
        )
        logger.debug("Input path set to: %s", self.input_path)
        self.make_directory(self.input_path)
        self.output_path = (
            self.current_dir + self.my_separator + "output" + self.my_separator
        )
        logger.debug("Output path set to: %s", self.output_path)
        self.make_directory(self.output_path)
        self.tmp_path = (self.current_dir + self.my_separator + f"tmp{psusername}" + self.my_separator)
        logger.debug("Temp path set to: %s", self.tmp_path)
        self.make_directory(self.tmp_path)

    def make_directory(self, my_dir):
        """Make a directory."""
        try:
            os.mkdir(my_dir)
        except FileNotFoundError as e:
            logger.error("Unable to create directory %s because: %s", my_dir, e)
        except FileExistsError as fe:
            logger.error(
                "Unable to create directory %s because it already exists.",
                my_dir, fe
            )
        logger.debug("Created directory: %s", my_dir)

    def print_help(self):
        """Display script help."""
        logger.debug("Starting print_help().")
        my_file = open("logo.txt")

        print(" ")
        print("-" * 80)
        for line in my_file:
            print(line.rstrip())
        print("-" * 80 + "\n\n")

    def print_output(self, message):
        """Print a message to the console."""
        sys.stdout.write("\033[K")
        message = "\033[5;36;40m" + message + "\033[0;0m"
        print(message, end="\r", flush=True)
        time.sleep(1)

    def remove_tmp_dir(self):
        """Blow away the temp dir at the end of the run."""
        if not self.save_temp_dir:
            if os.path.exists(self.tmp_path):
                shutil.rmtree(self.tmp_path)
        logger.debug("Removed temp directory: %s", self.tmp_path)
