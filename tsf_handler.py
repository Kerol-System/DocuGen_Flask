"""The SwiftDoc Project."""

import glob
import logging
import logging.config
import os
import re
import tarfile

import defusedxml.ElementTree as et

from xml_handler import PanXMLHandler

logging.config.fileConfig(
    "logging.conf",
    defaults={"logfilename": "SwiftDoc.log"},
    disable_existing_loggers=False,
)
logger = logging.getLogger(__name__)


class PanTSFHandler:
    """Methods for Tech Support Files."""

    def __init__(self, input_path, tmp_path, my_separator):
        """Make a set of PAN devices from the file at the input path."""
        self.input_path = input_path  # an empty string, we get this from itemplate1.py
        self.tmp_path = tmp_path
        self.my_separator = my_separator

    def check_panorama_model(self, device):
        """Check to see what model of Panorama this is, if any."""
        panorama_models = ["Panorama", "M-100", "M-500", "M-200", "M-600"]
        is_panorama = False

        if device.model in panorama_models:
            is_panorama = True
            # logger.debug("Found a Panorama: %s", device.model)
        # else:
        #    logger.debug("Not a Panorama: %s", device.model)

        return is_panorama

    def load_tsf_archive(self):
        """Put the .tgz files into the input directory."""
        logger.debug("Starting load_tsf_archive()")

        customer_files = []

        for f in os.listdir(self.input_path):
            # logger.debug("Found file: %s%s", self.input_path, f)
            if not f.endswith(".tgz") or f.endswith(".tar.gz"):  # check if it is a gzip
                logger.debug("Skipping non tar/gzip TSF file: %s", f)
            else:
                logger.info("Found customer TSF:  %s%s", self.input_path, f)
                customer_files.append(f)

        return customer_files

    def extract_info_from_tsf(self, filename):
        """Extract info from TSF"""
        logger.debug(
            "Starting extract_info_from_tsf() for filename: %s",
            (self.input_path + filename),
        )
        tar = tarfile.open(self.input_path + filename, "r:gz")
        tarfiles = tar.getnames()

        # for myfile in tarfiles:
        #    logger.debug("Tar file : %s", myfile)

        isPanorama = True  # assume Panorama until we prove otherwise.

        for filename in tarfiles:
            if "cli/techsupport" in filename:
                logger.debug("Extracting cli/techsupport: %s", filename)
                tar.extract(member=filename, path=self.tmp_path)
            elif "opt/pancfg/mgmt/saved-configs/.merged-running-config.xml" in filename:
                tar.extract(member=filename, path=self.tmp_path)
                isPanorama = False  # not a Panorama.
            elif "./opt/pancfg/mgmt/saved-configs/running-config.xml" in filename:
                tar.extract(member=filename, path=self.tmp_path)
            elif "./tmp/cli/logs/sdb.txt" in filename:
                tar.extract(member=filename, path=self.tmp_path)
        tar.close()
        logger.debug("TAR file decompression completed")

        tsf_info = {}  # a dictionary to hold the results.

        if isPanorama:
            logger.debug("Looks like a Panorama")
            ssi = self.cli_output_check(
                "> show system info", "operational-mode"
            )
            tsf_info["opmode"] = re.search("system-mode: (.*)", ssi).group(1)
            logger.debug("Setting opmode: %s", tsf_info["opmode"])
        else:
            logger.debug("Looks like a firewall")
            ssi = self.cli_output_check("> show system info", "operational-mode")
            tsf_info["multivsys"] = re.search("multi-vsys: (.*)", ssi).group(1)
            logger.debug("Setting multivsys: %s", tsf_info["multivsys"])

        tsf_info["hostname"] = re.search("hostname: (.*)", ssi).group(1)
        logger.debug("Hostname: %s\n", tsf_info["hostname"])
        tsf_info["model"] = re.search("model: (.*)", ssi).group(1)
        logger.debug("Settting model to %s", tsf_info["model"])
        tsf_info["serial"] = re.search("serial: (.*)", ssi).group(1)
        logger.debug("Serial number: %s", tsf_info["serial"])
        tsf_info["panos"] = re.search("sw-version: (.*)", ssi).group(1)
        tsf_info["licenses"] = self.get_tsf_licenses(isPanorama)

        if tsf_info["model"] not in ["Panorama", "M-100", "M-500", "M-200", "M-600"]:
            # tsf_info["hainfo"] = self.get_tsf_ha_info(tmp_path)
            # tsf_info["haotherinfo"] = self.get_tsf_ha_otherinfo(tmp_path)
            tsf_info["hapeername"] = ""
            tsf_info["admins"] = self.get_tsf_info("admins")
            tsf_info["vsys"] = self.get_tsf_info("vsys")
            tsf_info["antivirus"] = self.get_tsf_info("av")
            tsf_info["antispy"] = self.get_tsf_info("as")
            tsf_info["vulnerability"] = self.get_tsf_info("vp")
            tsf_info["url"] = self.get_tsf_info("url")
            tsf_info["wildfire"] = self.get_tsf_info("wf")
            tsf_info["fileblocking"] = self.get_tsf_info("fb")
            tsf_info["update_sched"] = self.get_tsf_info("update-schedule")
            tsf_info["secprof"] = self.get_tsf_info("secprof")
            tsf_info["data_filtering"] = self.get_tsf_info("df")
            tsf_info["data_objects"] = self.get_tsf_info("dfo")
            tsf_info["mgmtinfo"] = self.get_tsf_info("mgmtinfofw")
            tsf_info["dos"] = self.get_tsf_info("dos")
            tsf_info["ike_crypto"] = self.get_tsf_info("ike-crypto")
            tsf_info["ipsec_crypto"] = self.get_tsf_info("ipsec-crypto")
            tsf_info["ike_gw"] = self.get_tsf_info("ike-gw")
            tsf_info["ipsec_vpn"] = self.get_tsf_info("ipsec-vpn")
            tsf_info["interfaces"] = self.get_tsf_info("interfaces")
            tsf_info["zones"] = self.get_tsf_info("zones")
            tsf_info["templates"] = ""
            tsf_info["devicegroups"] = ""
            tsf_info["logforwarding"] = self.get_tsf_info("logforwarding")
            tsf_info["snmpv2m"] = self.get_tsf_info("snmpv2m")
            tsf_info["snmpv2s"] = self.get_tsf_info("snmpv2s")
            tsf_info["snmpv3"] = self.get_tsf_info("snmpv3")
            tsf_info["logintsettings"] = self.get_tsf_info("logintsettings")
            tsf_info["gp_portals"] = self.get_tsf_info("gp_portals")
            tsf_info["gp_gateways"] = self.get_tsf_info("gp_gateways")
            tsf_info["hip"] = self.get_tsf_info("hip")
            tsf_info["groups"] = self.get_tsf_info("groups")
            tsf_info["userid"] = self.get_tsf_info("userid")
        else:
            tsf_info["hapriority"] = self.get_tsf_ha_panorama_info()
            tsf_info["mgmtinfo"] = self.get_tsf_info("mgmtinfopn")
            tsf_info["templates"] = self.get_tsf_info("templates")
            tsf_info["devicegroups"] = self.get_tsf_info("devicegroups")
            tsf_info["admins"] = self.get_tsf_info("adminspn")
            tsf_info["logforwarding"] = ""
            tsf_info["vsys"] = ""
            tsf_info["antivirus"] = ""
            tsf_info["antispy"] = ""
            tsf_info["vulnerability"] = ""
            tsf_info["url"] = ""
            tsf_info["wildfire"] = ""
            tsf_info["fileblocking"] = ""
            tsf_info["update_sched"] = ""
            tsf_info["secprof"] = ""
            tsf_info["data_filtering"] = ""
            tsf_info["data_objects"] = ""
            tsf_info["dos"] = ""
            tsf_info["ike_crypto"] = ""
            tsf_info["ipsec_vpn"] = ""
            tsf_info["ike_gw"] = ""
            tsf_info["ipsec_crypto"] = ""
            tsf_info["interfaces"] = ""
            tsf_info["zones"] = ""
            tsf_info["logintsettings"] = ""
            tsf_info["snmpv2s"] = self.get_tsf_info("snmpv2sp")
            tsf_info["snmpv2m"] = self.get_tsf_info("snmpv2mp")
            tsf_info["snmpv3"] = self.get_tsf_info("snmpv3p")
            tsf_info["gp_portals"] = ""
            tsf_info["gp_gateways"] = ""
            tsf_info["hip"] = ""
            tsf_info["groups"] = ""
            tsf_info["userid"] = ""

        return tsf_info

    def cli_output_check(self, start, end):
        """Function to get output of various CLI commands from TSF.

        The output has to be parsed and formatted seperately.
        """
        my_tsf_file = glob.glob(self.tmp_path + "tmp/cli/techsupport_*_*_*.txt")
        tsf_file = str(my_tsf_file[0])
        logger.debug("Starting cli_output_check() on : %s", tsf_file)
        logger.debug("TSF File: %s", tsf_file)

        try:
            match = False
            match_string = str()
            with open(tsf_file) as file:
                for line in file:
                    if line != "\n":
                        # logger.debug("Checking line: %s", line.rstrip())
                        if re.match(start, line):
                            match = True
                        if re.match(end, line):
                            match = False
                        if match:
                            # logger.debug("Adding line to match_string: %s", line.rstrip())
                            match_string = (
                                match_string + line
                            )  # line.rstrip() # remove this strip so the text wouldnt be a giant blob
                            # logger.debug("The match_string is %s", match_string)
        except Exception as e:
            print("broken: %s", e)

        return match_string

    def get_tsf_licenses(self, isPanorama):
        """Function to get License info from TSF for Firewall and Panorama."""

        if isPanorama:
            license_info = self.cli_output_check(
                "> request license info", "> show counter global"
            )
        else:
            license_info = self.cli_output_check(
                "> request license info", "> show system setting logging"
            )
        license_info = license_info.splitlines()
        licenses = ""
        i = 0
        for line in license_info:
            if "Feature" in line:
                if i == 0:
                    licenses = line.split("Feature: ", 1)[1]
                    i = i + 1
                else:
                    licenses = licenses + ", " + line.split("Feature: ", 1)[1]
            else:
                continue
        licenses = licenses + "."
        return licenses

    def get_tsf_info(self, which_info):
        """Get various info from TSF file."""
        # logger.debug("Starting get_tsf_info with tmp_path: %s", self.tmp_path)
        filename = "dummy"

        if (
            which_info == "mgmtinfopn"
            or which_info == "templates"
            or which_info == "devicegroups"
            or which_info == "adminspn"
            or which_info == "hapriority"
        ):
            filename = (
                self.tmp_path + "opt/pancfg/mgmt/saved-configs/running-config.xml"
            )
            # logger.debug("Setting XML filename: %s", filename)
        elif (
            which_info == "snmpv2mp"
            or which_info == "snmpv2sp"
            or which_info == "snmpv3p"
        ):
            filename = (
                self.tmp_path + "opt/pancfg/mgmt/saved-configs/running-config.xml"
            )
            # logger.debug("Setting XML filename: %s", filename)
        else:
            filename = (
                self.tmp_path
                + "opt/pancfg/mgmt/saved-configs/.merged-running-config.xml"
            )
            # logger.debug("Setting XML filename: %s", filename)

        my_xml_handler = PanXMLHandler(filename)
        # logger.debug("Import XML Tree from: %s", filename)
        my_xml_handler.set_conf_root()

        if my_xml_handler.config_root is not None:
            if which_info == "av":
                dict_list = my_xml_handler.get_av()
            elif which_info == "as":
                dict_list = my_xml_handler.get_as()
            elif which_info == "vp":
                dict_list = my_xml_handler.get_vp()
            elif which_info == "wf":
                dict_list = my_xml_handler.get_wf()
            elif which_info == "fb":
                dict_list = my_xml_handler.get_fb()
            elif which_info == "df":
                dict_list = my_xml_handler.get_df()
            elif which_info == "dfo":
                dict_list = my_xml_handler.get_dfo()
            elif which_info == "url":
                dict_list = my_xml_handler.get_url()
            elif which_info == "mgmtinfofw":
                dict_list = my_xml_handler.get_mgmtinfo("Firewall")
            elif which_info == "update-schedule":
                dict_list = my_xml_handler.get_update_sched()
            elif which_info == "secprof":
                dict_list = my_xml_handler.get_secprof()
            elif which_info == "dos":
                dict_list = my_xml_handler.get_dos()
            elif which_info == "ike-crypto":
                dict_list = my_xml_handler.get_ike_crypto()
            elif which_info == "ipsec-crypto":
                dict_list = my_xml_handler.get_ipsec_crypto()
            elif which_info == "ike-gw":
                dict_list = my_xml_handler.get_ike_gw()
            elif which_info == "ipsec-vpn":
                dict_list = my_xml_handler.get_ipsec_vpn()
            elif which_info == "vsys":
                dict_list = my_xml_handler.get_vsys_vr()
            elif which_info == "interfaces":
                dict_list = my_xml_handler.get_interfaces()
            elif which_info == "zones":
                dict_list = my_xml_handler.get_zones()
            elif which_info == "logforwarding":
                dict_list = my_xml_handler.get_logforwarding()
            elif which_info == "templates":
                dict_list = my_xml_handler.get_templates()
            elif which_info == "devicegroups":
                dict_list = my_xml_handler.get_devicegroups()
            elif which_info == "snmpv2m":
                dict_list = my_xml_handler.get_snmpv2_manager()
            elif which_info == "snmpv2s":
                dict_list = my_xml_handler.get_snmpv2_system()
            elif which_info == "snmpv3":
                dict_list = my_xml_handler.get_snmpv3()
            elif which_info == "snmpv2mp":
                dict_list = my_xml_handler.get_snmpv2_manager()
            elif which_info == "snmpv2sp":
                dict_list = my_xml_handler.get_snmpv2_system()
            elif which_info == "snmpv3p":
                dict_list = my_xml_handler.get_snmpv3()
            elif which_info == "logintsettings":
                dict_list = my_xml_handler.get_logintsettings()
            elif which_info == "gp_portals":
                dict_list = my_xml_handler.get_gp_portals()
            elif which_info == "gp_gateways":
                dict_list = my_xml_handler.get_gp_gateways()
            elif which_info == "hip":
                dict_list = my_xml_handler.get_hip()
            elif which_info == "admins":
                dict_list = my_xml_handler.get_admins()
            elif which_info == "adminspn":
                dict_list = my_xml_handler.get_admins()
            elif which_info == "groups":
                dict_list = my_xml_handler.get_groups()
            elif which_info == "userid":
                dict_list = my_xml_handler.get_userid()
            else:
                dict_list = my_xml_handler.get_mgmtinfo("Panorama")
                temp_dict = my_xml_handler.get_mgmtinfo("Panorama")
                for key, value in temp_dict.items():
                    logger.info("MGMT info: %s:%s", key, value)
            return dict_list
        else:
            return None

    def get_tsf_ha_panorama_info(self):
        hapriority = "HA is not enabled"
        ha = self.cli_output_check(
            "> show high-availability all",
            "> show high-availability state-synchronization",
        )
        for line in ha.split("\n"):
            if "Priority:" in line:
                hapriority = re.search("Priority: (.*)", ha).group(1)
                return hapriority
        return hapriority

    def get_tsf_ha_info(self):
        """ """
        logger.debug("Starting get_tsf_ha_info()")
        config_path = (
            self.tmp_path
            + "tmp/"
            + self.date_string
            + "/opt/pancfg/mgmt/saved-configs/.merged-running-config.xml"
        )
        sdb_path = self.tmp_path + "tmp/" + self.date_string + "/tmp/cli/logs/sdb.txt"
        ha = self.cli_output_check(
            "> show high-availability all",
            "> show high-availability state-synchronization",
        )
        for line in ha.split("\n"):
            if "HA not enabled" == line:
                return {"hapeername": None}
        hamode = "None"
        hamode = re.search("Mode: (.*)", ha).group(1)
        conf = open(config_path)
        tree = et.parse(conf)
        config_root = tree.getroot()
        hainfo = {}
        ha1a = config_root.find(".//high-availability/interface/ha1/ip-address")
        ha1b = config_root.find(".//high-availability/interface/ha1-backup/ip-address")
        ha2a = config_root.find(".//high-availability/interface/ha2/ip-address")
        ha2b = config_root.find(".//high-availability/interface/ha2-backup/ip-address")
        heartbeat = config_root.find(
            ".//high-availability/group/election-option/heartbeat-backup"
        )
        if ha1a:
            ha1a = ha1a.text
        if ha1b:
            ha1b = ha1b.text
        if ha2a:
            ha2a = ha2a.text
        if ha2b:
            ha2b = ha2b.text
        if heartbeat:
            heartbeat = heartbeat.text
            if heartbeat == "yes":
                heartbeat = "Enabled"
            else:
                heartbeat = "Disabled"
        else:
            heartbeat = "Disabled"
        hainfo["ha1a"] = ha1a
        hainfo["ha1b"] = ha1b
        hainfo["ha2a"] = ha2a
        hainfo["ha2b"] = ha2b
        hainfo["hamode"] = hamode
        with open(sdb_path, encoding="ISO-8859-1") as sdb_file:
            sdb = sdb_file.read()
            hapeername = re.search("peer.cfg.hostname: (.*)", sdb)
            if hapeername:
                hapeername = hapeername.group(1)
            ha_peer_info = re.search("ha.app.peer.info: (.*)", sdb)
        if hainfo["hamode"] != "Active-Passive":
            hapeername = None
        peerserial = ""
        peerha1a = ""
        peerha1b = ""
        peerha2a = ""
        peerha2b = ""
        peermgmtip = ""
        peermgmtipv6 = ""
        if ha_peer_info:
            ha_peer_info = ha_peer_info.group(1)
            peerserial = re.search("'serial-number': (.*?), '", ha_peer_info).group(1)
            peerha1a = re.search("'ha1-ip': (.*?), '", ha_peer_info).group(1)
            peerha1b = re.search("'ha1-backup-ip': (.*?), 'ha", ha_peer_info).group(1)
            peerha2a = re.search("'ha2-ip': (.*?), '", ha_peer_info).group(1)
            peerha2b = re.search("'ha2-backup-ip': (.*?), '", ha_peer_info).group(1)
            peermgmtip = re.search("'mgmt-ip': (.*?), '", ha_peer_info).group(1)
            peermgmtipv6 = re.search("'mgmt-ipv6': (.*?), '", ha_peer_info).group(1)
        hainfo["hapeername"] = hapeername
        hainfo["peerserial"] = peerserial
        hainfo["peerha1a"] = peerha1a
        hainfo["peerha1b"] = peerha1b
        hainfo["peerha2a"] = peerha2a
        hainfo["peerha2b"] = peerha2b
        hainfo["peermgmtip"] = peermgmtip
        hainfo["peermgmtipv6"] = peermgmtipv6
        hainfo["heartbeat"] = heartbeat
        # print(hainfo)
        return hainfo

    def get_tsf_ha_otherinfo(self):
        """Method."""
        logger.debug("Starting get_tsf_ha_otherinfo().")

        ha = self.cli_output_check(
            "> show high-availability all",
            "> show high-availability state-synchronization",
        )
        for line in ha.split("\n"):
            if "HA not enabled" == line:
                return {}
        haotherinfo = {}
        passivelink_state = re.search("Passive Link State: (.*)", ha)

        if passivelink_state:
            passivelink_state = passivelink_state.group(1)
        mfhdtime = re.search("Monitor Fail Hold Down Interval: (.*)", ha)

        if mfhdtime:
            mfhdtime = mfhdtime.group(1)
        priority = re.search("Priority: (.*)", ha)

        if priority:
            priority = priority.group(1)
        preemptive = re.search("Preemptive: (.*)", ha).group(1)
        linkmonitoring = re.search(
            "Link Monitoring Information:\n(.*)", ha, re.MULTILINE
        ).group(1)
        pathmonitoring = re.search(
            "Path Monitoring Information:\n(.*)", ha, re.MULTILINE
        ).group(1)
        backup = re.search(
            "HA1 Backup Control Link Information:\n(.*)", ha, re.MULTILINE
        )

        if backup is None:
            backup = re.search(
                "HA2 Backup Data Link Information:\n(.*)", ha, re.MULTILINE
            )
            if backup is None:
                backup = "Disabled"
            else:
                backup = "Enabled"
        else:
            backup = "Enabled"

        if linkmonitoring == "    Enabled: yes":
            linkmonitoring = "Enabled"
        else:
            linkmonitoring = "Disabled"

        if pathmonitoring == "    Enabled: yes":
            pathmonitoring = "Enabled"
        else:
            pathmonitoring = "Disabled"

        pht = re.search("Promotion Hold Interval: (.*)", ha).group(1)
        hi = re.search("Heartbeat Ping Interval: (.*)", ha).group(1)

        if pht == "500 ms" and hi == "1000 ms":
            hatimer = "Aggressive"
        elif pht == "2000 ms" and hi == "2000 ms":
            hatimer = "Recommended"
        else:
            hatimer = "Custom"
        haotherinfo["passivelink_state"] = passivelink_state
        haotherinfo["mfhdtime"] = mfhdtime
        haotherinfo["priority"] = priority
        haotherinfo["preemptive"] = preemptive
        haotherinfo["hatimer"] = hatimer
        haotherinfo["backup"] = backup
        haotherinfo["linkmonitoring"] = linkmonitoring
        haotherinfo["pathmonitoring"] = pathmonitoring

        return haotherinfo

    def get_hapeername(self, fw):
        """Get the name of the HA peer as it appears to the PAN device."""
        logger.debug("Starting get_hapeername.")
        peername = ""
        if fw.hapeername:
            peername = "\n" + fw.hapeername
        return peername


"""
__author__     = 'Franklin Diaz'
__copyright__  = '© 2021 Palo Alto Networks, Inc. All rights reserved.'
__license__    = 'https://www.paloaltonetworks.com/legal/script-software-license-1-0.pdf'
__version__    = '0.1'
__email__      = 'fdiaz@paloaltonetworks.com'
"""
