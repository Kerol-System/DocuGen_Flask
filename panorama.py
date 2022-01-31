"""Settings for Panorama"""

import datetime
import logging
import logging.config
import os
import pathlib
from docxtpl import DocxTemplate

logging.config.fileConfig(
    "logging.conf",
    defaults={"logfilename": "SwiftDoc.log"},
    disable_existing_loggers=False,
)
logger = logging.getLogger(__name__)


class Panorama:
    """Class to populate all the panorama tables"""
    now = datetime.datetime.now()  # this time is used for start of execution
    pan_hosts = []  # list will get populated from main.py
    my_separator = "/"  # default to Linux/Mac

    if os.name != "posix":
        my_separator = "\\"

    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + my_separator + 'flask-swiftdoc-1.0'

    t1Info = []
    t2Info = []
    t3Info = []
    t4Info = []
    t5Info = []
    t6Info = []
    t7Info = []
    t24Info = []
    t25Info = []
    t26Info = []

    def __init__(self, date_string, input_path, output_path, report_name, template1, info):
        """Make a SwiftDoc."""
        self.date_string = date_string
        self.input_path = input_path  # an empty string, we get this from itemplate1.py
        self.output_path = output_path + report_name + ".docx"
        if os.name != "posix":
            self.my_separator = "\\"
        self.doc_path = self.current_dir + self.my_separator + "static" + self.my_separator + "template_file" + self.my_separator + str(
            template1)
        self.template = DocxTemplate(self.doc_path)
        self.info = info

    def check_panorama_model(self, device):
        """Check to see what model of Panorama this is, if any."""
        panorama_models = ["Panorama", "M-100", "M-500", "M-200", "M-600"]
        is_panorama = False
        if device.model in panorama_models:
            is_panorama = True
            logger.debug("Found a Panorama: %s", device.model)
        else:
            logger.debug("Not a Panorama: %s", device.model)
        return is_panorama

    def func_name(self):
        """Return the name of the method."""
        import traceback
        return traceback.extract_stack(None, 2)[0][2]

    def t1_info(self):
        """
        # Populate the values for Table 1 - Procured Systems.
        Panorama: yes
        FW: yes
        """
        global t1_dictionary
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            # logger.debug("t1Info for %s", fw.hostname)
            t1_dictionary = {
                "t1serial": fw.serial,
                "t1devicename": fw.hostname,
                "t1model": fw.model,
            }
            self.t1Info.append(dict(t1_dictionary))

    def t2_info(self):
        """Populate the values for Table 2 - Licenses.

        Panorama: yes
        FW: yes
        """
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            t2_dictionary = {
                "t2devicename": fw.hostname,
                "t2licenses": fw.licenses,
            }
            self.t2Info.append(dict(t2_dictionary))

    def t3_info(self):
        """# Populate the values for Table 3 - PAN-OS Versions.

        Panorama: yes
        FW: yes
        """
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            # logger.debug("T3 panos version for %s: %s", fw.hostname, fw.panos)
            t3_dictionary = {
                "t3devicename": fw.hostname,
                "t3panos": fw.panos,
            }
            self.t3Info.append(dict(t3_dictionary))

    def t4_info(self):
        """Populate the values for Table 4 - Panorama.
        Panorama: yes
        FW: no
        """
        logger.debug("Running %s", self.func_name())

        for panorama in self.pan_hosts:
            if self.check_panorama_model(panorama):
                t4_dictionary = {
                    "t4serial": panorama.serial,
                    "t4devicename": panorama.hostname,
                    "t4model": panorama.model,
                }
                self.t4Info.append(dict(t4_dictionary))

    def t5_info(self):
        """Populate the values for Table 5 - Panorama Licenses.

        Panorama: yes
        FW: no
        """
        logger.debug("Running %s", self.func_name())

        for panorama in self.pan_hosts:
            if self.check_panorama_model(panorama):
                t5_dictionary = {
                    "t5devicename": panorama.hostname,
                    "t5licenses": panorama.licenses,
                    "t5role": panorama.opmode,
                }
                self.t5Info.append(dict(t5_dictionary))

    def t6_info(self):
        """Populate the values for Table 6 - Panorama PAN-OS Versions.
        Panorama: yes
        FW: no
        """
        logger.debug("Running %s", self.func_name())

        for panorama in self.pan_hosts:
            if self.check_panorama_model(panorama):
                t6_dictionary = {
                    "t6devicename": panorama.hostname,
                    "t6panos": panorama.panos,
                }
                self.t6Info.append(dict(t6_dictionary))

    def t7_info(self):
        """Populate the values for Table 7 - Firewall/Panorama Admins.

        Panorama: yes
        FW: yes
        """
        logger.debug("Running %s", self.func_name())

        t7_dictionary = {}

        for fw in self.pan_hosts:
            logger.debug(str(fw.admins))
            if fw.admins is not None:
                for entry in fw.admins:
                    t7_dictionary["t7devicename"] = fw.hostname + fw.hapeername
                    t7_dictionary["t7adminname"] = entry["admin_name"]
                    t7_dictionary["t7adminrole"] = entry["admin_role"]
                    t7_dictionary["t7authprofile"] = entry["auth_profile"]
                    t7_dictionary["t7passprofile"] = entry["pass_profile"]
                    t7_dictionary["t7roleprof"] = entry["role_profile"]
                    t7_dictionary["t7accessdomain"] = entry["access_domain"]
                    self.t7Info.append(dict(t7_dictionary))

    def t24_info(self):
        """# Populate the values for Table 24 - Panorama MGT Port Settings

        # Pending Implementation of HA priority
        """
        logger.debug("Running %s", self.func_name())

        for panorama in self.pan_hosts:
            if self.check_panorama_model(panorama):
                t24_dictionary = {
                    "t24devicename": panorama.hostname,
                    "t24mgmtIP": panorama.mgmtinfo["ip"],
                    "t24mgmtnetmask": panorama.mgmtinfo["mask"],
                    "t24mgmtgateway": panorama.mgmtinfo["gw"],
                    "t24mgmtipv6": panorama.mgmtinfo["ipv6"],
                    "t24mgmtspeed": panorama.mgmtinfo["speed"],
                    "t24mgmtmtu": panorama.mgmtinfo["mtu"],
                    "t24mgmtservices": panorama.mgmtinfo["services"],
                    "t24mgmtpermittedips": panorama.mgmtinfo["permitted_ips"],
                    "t24hapriority": panorama.hapriority,
                }
                self.t24Info.append(dict(t24_dictionary))

    def t25_info(self):
        """# Populate the values for Table 25 – Panorama Templates."""
        logger.debug("Running %s", self.func_name())

        t25_dictionary = {}
        for panorama in self.pan_hosts:
            if self.check_panorama_model(panorama):
                for entry in panorama.templates:
                    t25_dictionary["t25devicename"] = panorama.hostname
                    t25_dictionary["t25templatename"] = entry["template_name"]
                    t25_dictionary["t25stackname"] = entry["stack_name"]
                    t25_dictionary["t25stackmembers"] = entry["members"]
                    self.t25Info.append(dict(t25_dictionary))

    def t26_info(self):
        """# Populate the values for Table 26 – Panorama Device Groups."""
        logger.debug("Running %s", self.func_name())

        t26_dictionary = {}

        for panorama in self.pan_hosts:
            if self.check_panorama_model(panorama):
                for entry in panorama.devicegroups:
                    t26_dictionary["t26devicename"] = panorama.hostname
                    t26_dictionary["t26tier1"] = entry["tier1"]
                    t26_dictionary["t26tier2"] = entry["tier2"]
                    t26_dictionary["t26tier3"] = entry["tier3"]
                    t26_dictionary["t26tier4"] = entry["tier4"]
                    t26_dictionary["t26masterdevice"] = entry["master"]
                    self.t26Info.append(dict(t26_dictionary))

        final = {
            "Customer": self.info["Customer"],
            "Month": self.info["Month"],
            "Year": self.info["Year"],
            "t1": self.t1Info,
            "t2": self.t2Info,
            "t3": self.t3Info,
            "t4": self.t4Info,
            "t5": self.t5Info,
            "t6": self.t6Info,
            "t7": self.t7Info,
            "t24": self.t24Info,
            "t25": self.t25Info,
            "t26": self.t26Info
        }
        self.template.render(final)

    def clean(self):
        self.t1Info.clear()
        self.t2Info.clear()
        self.t3Info.clear()
        self.t4Info.clear()
        self.t5Info.clear()
        self.t6Info.clear()
        self.t7Info.clear()
        self.t24Info.clear()
        self.t25Info.clear()
        self.t26Info.clear()

    def populate_lists(self):
        """Run all the methods in preparation for doc generation."""
        logger.debug("Starting populate_lists()")
        self.t1_info()
        self.t2_info()
        self.t3_info()
        self.t4_info()
        self.t5_info()
        self.t6_info()
        self.t7_info()
        self.t24_info()
        self.t25_info()
        self.t26_info()
        self.clean()

    def gen_doc(self):
        """Generate the document.

        # Write out the completed word document
        """
        logger.debug("Setting input template to: %s", self.doc_path)
        try:
            self.template.save(self.output_path)
        except Exception as e:
            logger.error("Unable to write the output.")

        print("-" * 112)
        logger.info("-" * 112)
        print(
            "Finished in "
            + (
                str(
                    float(
                        "{0:.2f}".format(
                            (datetime.datetime.now() - self.now).total_seconds()
                        )
                    )
                )
            )
            + " seconds."
        )
        logger.info(
            "Finished in "
            + (
                str(
                    float(
                        "{0:.2f}".format(
                            (datetime.datetime.now() - self.now).total_seconds()
                        )
                    )
                )
            )
            + " seconds."
        )
        print("Output document stored at " + self.output_path)
        logger.info("Output document stored at " + self.output_path)
        print("-" * 112)
        logger.info("-" * 112)
