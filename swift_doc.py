"""The SwiftDoc Project."""

import datetime
import logging
import logging.config
import os
from docxtpl import DocxTemplate

logging.config.fileConfig(
    "logging.conf",
    defaults={"logfilename": "SwiftDoc.log"},
    disable_existing_loggers=False,
)
logger = logging.getLogger(__name__)

message = "Not Configured"


class SwiftDoc:
    """Things for preparing logs, connecting to devices, etc."""

    MonthYear = datetime.datetime.now().strftime(
        "%B %Y"
    )  # To print Month Year on the title page
    now = datetime.datetime.now()  # this time is used for start of execution
    pan_hosts = []  # list will get populated from main.py
    my_separator = "/"  # default to Linux/Mac

    if os.name != "posix":
        my_separator = "\\"

    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + my_separator + 'flask-swiftdoc-1.0'
    message = "Not Configured"
    temp = ['1']
    t1Info = []
    t2Info = []
    t3Info = []
    t4Info = []
    t5Info = []
    t6Info = []
    t7Info = []
    t8Info = []
    t9Info = []
    t10Info = []
    t11Info = []
    t12Info = []
    t13Info = []
    t14Info = []
    t15Info = []
    t16Info = []
    t17Info = []
    t18Info = []
    t19Info = []
    t20Info = []
    t21Info = []
    t23Info = []
    t24Info = []
    t25Info = []
    t26Info = []
    t27Info = []
    t28Info = []
    t29Info = []
    t30Info = []
    t31Info = []
    t32Info = []
    t33Info = []
    t34Info = []
    t35Info = []
    t36Info = []
    t37Info = []
    t38Info = []
    t39Info = []
    t40Info = []
    t41Info = []
    t42Info = []
    t43Info = []
    t44Info = []
    t18Count = 0
    t18UsedIKE = []
    t19Count = 0
    t19UsedIPSec = []
    t55Info = []

    def __init__(self, date_string, input_path, output_path, report_name, template1, info):
        """Make a SwiftDoc."""
        self.date_string = date_string
        self.input_path = input_path  # an empty string, we get this from helpers.py
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
            t4_dictionary = {
                "t4serial": panorama.serial if self.check_panorama_model(panorama) else message,
                "t4devicename": panorama.hostname if self.check_panorama_model(panorama) else message,
                "t4model": panorama.model if self.check_panorama_model(panorama) else message,
            }
            self.t4Info.append(dict(t4_dictionary))

    def t5_info(self):
        """Populate the values for Table 5 - Panorama Licenses.

        Panorama: yes
        FW: no
        """
        logger.debug("Running %s", self.func_name())

        for panorama in self.pan_hosts:
            t5_dictionary = {
                "t5devicename": panorama.hostname if self.check_panorama_model(panorama) else message,
                "t5licenses": panorama.licenses if self.check_panorama_model(panorama) else message,
                "t5role": panorama.opmode if self.check_panorama_model(panorama) else message,
            }
            self.t5Info.append(dict(t5_dictionary))

    def t6_info(self):
        """Populate the values for Table 6 - Panorama PAN-OS Versions.
        Panorama: yes
        FW: no
        """
        logger.debug("Running %s", self.func_name())

        for panorama in self.pan_hosts:
            t6_dictionary = {
                "t6devicename": panorama.hostname if self.check_panorama_model(panorama) else message,
                "t6panos": panorama.panos if self.check_panorama_model(panorama) else message,
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
            for entry in fw.admins:
                t7_dictionary["t7devicename"] = fw.hostname + fw.hapeername if fw.admins is not None else message
                t7_dictionary["t7adminname"] = entry["admin_name"] if fw.admins is not None else message
                t7_dictionary["t7adminrole"] = entry["admin_role"] if fw.admins is not None else message
                t7_dictionary["t7authprofile"] = entry["auth_profile"] if fw.admins is not None else message
                t7_dictionary["t7passprofile"] = entry["pass_profile"] if fw.admins is not None else message
                t7_dictionary["t7roleprof"] = entry["role_profile"] if fw.admins is not None else message
                t7_dictionary["t7accessdomain"] = entry["access_domain"] if fw.admins is not None else message
                self.t7Info.append(dict(t7_dictionary))

    def t8_info(self):
        """# Populate the values for Table 8 - VSYS."""
        logger.debug("Running %s", self.func_name())
        for fw in self.pan_hosts:
            t8_dictionary = {}
            if not self.check_panorama_model(fw) and fw.multivsys is not None:
                t8_dictionary = {"t8devicename": fw.hostname + fw.hapeername}
                if fw.multivsys == "off":
                    t8_dictionary["t8vsysid"] = "1"
                else:
                    t8_dictionary["t8vsysid"] = ""
                if fw.vsys is not None:
                    for entry in fw.vsys:
                        t8_dictionary["t8vsysname"] = entry["vsys_name"]
                        t8_dictionary["t8interfaces"] = entry["interfaces"]
                        t8_dictionary["t8vr"] = entry["vr_name_i"]
                        self.t8Info.append(dict(t8_dictionary))
            else:
                t8_dictionary["t8devicename"] = message
                t8_dictionary["t8vsysid"] = message
                t8_dictionary["t8vsysname"] = message
                t8_dictionary["t8interfaces"] = message
                t8_dictionary["t8vr"] = message
                self.t8Info.append(dict(t8_dictionary))

    def t9_info(self):
        """# Populate the values for Table 9 - Virtual Router."""
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            t9_dictionary = {}
            if not self.check_panorama_model(fw) and fw.vsys is not None:
                t9_dictionary = {"t9devicename": fw.hostname + fw.hapeername}
                for entry in fw.vsys:
                    t9_dictionary["t9vsysname"] = entry["vsys_name"]
                    t9_dictionary["t9vr"] = entry["vr_name_p"]
                    t9_dictionary["t9protocols"] = entry["protocols"]
                    self.t9Info.append(dict(t9_dictionary))
            else:
                t9_dictionary["t9devicename"] = message
                t9_dictionary["t9vsysname"] = message
                t9_dictionary["t9vr"] = message
                t9_dictionary["t9protocols"] = message
                self.t9Info.append(dict(t9_dictionary))

    def t10_info(self):
        """# Populate the values for Table 10 – HA Firewall Deployment."""
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            t10_dictionary = {"t10devicename": fw.hostname if not self.check_panorama_model(fw) else message}
            hainfo = fw.hainfo
            # if hainfo != {'hapeername':None}:
            t10_dictionary["t10hamode"] = hainfo["hamode"] if hainfo != {} and hainfo != {
                "hapeername": None} else message
            t10_dictionary["t10ha1a"] = hainfo["ha1a"] if hainfo != {} and hainfo != {"hapeername": None} else message
            t10_dictionary["t10ha1b"] = hainfo["ha1b"] if hainfo != {} and hainfo != {"hapeername": None} else message
            t10_dictionary["t10ha2a"] = hainfo["ha2a"] if hainfo != {} and hainfo != {"hapeername": None} else message
            t10_dictionary["t10ha2b"] = hainfo["ha2b"] if hainfo != {} and hainfo != {"hapeername": None} else message
            self.t10Info.append(dict(t10_dictionary))

    def t11_info(self):
        """# Populate the values for Table 11 – Standardized HA Settings."""
        logger.debug("Running %s", self.func_name())
        t11_dictionary = {}
        haotherinfo = ""
        for fw in self.pan_hosts:
            # if not self.check_panorama_model(fw):
            t11_dictionary["t11devicename"] = fw.hostname + fw.hapeername if not self.check_panorama_model(
                fw) and fw.haotherinfo != {} else message
            t11_dictionary["t11passivelinkstate"] = fw.haotherinfo[
                "passivelink_state"
            ] if not self.check_panorama_model(fw) and fw.haotherinfo != {} else message
            t11_dictionary["t11mfhdtime"] = haotherinfo["mfhdtime"] if not self.check_panorama_model(
                fw) and fw.haotherinfo != {} else message
            t11_dictionary["t11priority"] = haotherinfo["priority"] if not self.check_panorama_model(
                fw) and fw.haotherinfo != {} else message
            t11_dictionary["t11preemptive"] = haotherinfo["preemptive"] if not self.check_panorama_model(
                fw) and fw.haotherinfo != {} else message
            if "heartbeat" in fw.haotherinfo:
                t11_dictionary["t11heartbeat"] = haotherinfo["heartbeat"] if not self.check_panorama_model(
                    fw) and fw.haotherinfo != {} else message
            else:
                t11_dictionary["t11heartbeat"] = "None" if not self.check_panorama_model(
                    fw) and fw.haotherinfo != {} else message
            t11_dictionary["t11hatimer"] = haotherinfo["hatimer"] if not self.check_panorama_model(
                fw) and fw.haotherinfo != {} else message
            t11_dictionary["t11backup"] = haotherinfo["backup"] if not self.check_panorama_model(
                fw) and fw.haotherinfo != {} else message
            t11_dictionary["t11linkmonitoring"] = haotherinfo["linkmonitoring"] if not self.check_panorama_model(
                fw) and fw.haotherinfo != {} else message
            t11_dictionary["t11pathmonitoring"] = haotherinfo["pathmonitoring"] if not self.check_panorama_model(
                fw) and fw.haotherinfo != {} else message
            self.t11Info.append(dict(t11_dictionary))

    def t12_info(self):
        """# Populate the values for Table 12 – Operational Interface Settings."""
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            t12_dictionary = {}
            if not self.check_panorama_model(fw) and fw.vsys is not None:
                for entry in fw.interfaces:
                    t12_dictionary["t12devicename"] = fw.hostname + fw.hapeername
                    t12_dictionary["t12interfacename"] = entry["interface"]
                    t12_dictionary["t12type"] = entry["type"]
                    if entry["mgtprof"] is None:
                        t12_dictionary["t12mgtprof"] = entry["mgtprof"]
                    else:
                        t12_dictionary["t12mgtprof"] = entry["mgtprof"].text
                    t12_dictionary["t12ip"] = entry["ip"]
                    if "vsys_name" in entry:
                        t12_dictionary["t12vsys"] = entry["vsys_name"]
                    else:
                        t12_dictionary["t12vsys"] = "None"
                    t12_dictionary["t12vr"] = entry["vr_name"]
                    t12_dictionary["t12zone"] = entry["zone"]
                    t12_dictionary["t12vlan"] = entry["vlan"]
                    self.t12Info.append(dict(t12_dictionary))
            else:
                t12_dictionary["t12devicename"] = message
                t12_dictionary["t12interfacename"] = message
                t12_dictionary["t12type"] = message
                t12_dictionary["t12mgtprof"] = message
                t12_dictionary["t12ip"] = message
                t12_dictionary["t12vsys"] = message
                t12_dictionary["t12vr"] = message
                t12_dictionary["t12zone"] = message
                t12_dictionary["t12vlan"] = message
                self.t12Info.append(dict(t12_dictionary))

    def t13_info(self):
        """# Populate the values for Table 13 - MGT Port Settings."""
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            # logger.debug("Including table 13 for %s, %s", fw.hostname, fw.mgmtinfo)
            t13_dictionary = {
                "t13devicename": fw.hostname if not self.check_panorama_model(fw) else message,
                "t13mgmtIP": fw.mgmtinfo["ip"] if not self.check_panorama_model(fw) else message,
                "t13mgmtnetmask": fw.mgmtinfo["mask"] if not self.check_panorama_model(fw) else message,
                "t13mgmtgateway": fw.mgmtinfo["gw"] if not self.check_panorama_model(fw) else message,
                "t13mgmtipv6": fw.mgmtinfo["ipv6"] if not self.check_panorama_model(fw) else message,
                "t13mgmtspeed": fw.mgmtinfo["speed"] if not self.check_panorama_model(fw) else message,
                "t13mgmtmtu": fw.mgmtinfo["mtu"] if not self.check_panorama_model(fw) else message,
                "t13mgmtservices": fw.mgmtinfo["services"] if not self.check_panorama_model(fw) else message,
                "t13mgmtpermittedips": fw.mgmtinfo["permitted_ips"] if not self.check_panorama_model(fw) else message,
            }
            self.t13Info.append(dict(t13_dictionary))

    def t14_info(self):
        """# Populate the values for Table 14 – Log Interface Settings."""
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            t14_dictionary = {}
            if not self.check_panorama_model(fw):
                if fw.logintsettings != {}:
                    t14_dictionary = {
                        "t14devicename": fw.hostname + fw.hapeername,
                        "t14interface": fw.logintsettings["logcard"],
                        "t14ip": fw.logintsettings["ip"],
                        "t14mask": fw.logintsettings["mask"],
                        "t14gw": fw.logintsettings["gw"],
                        "t14ipv6": fw.logintsettings["ipv6"],
                        "t14speed": fw.logintsettings["speed"],
                        "t14mtu": fw.logintsettings["mtu"],
                    }
                    self.t14Info.append(dict(t14_dictionary))
                else:
                    t14_dictionary = {
                        "t14devicename": message,
                        "t14interface": message,
                        "t14ip": message,
                        "t14mask": message,
                        "t14gw": message,
                        "t14ipv6": message,
                        "t14speed": message,
                        "t14mtu": message,
                    }
                    self.t14Info.append(dict(t14_dictionary))
            else:
                t14_dictionary = {
                    "t14devicename": message,
                    "t14interface": message,
                    "t14ip": message,
                    "t14mask": message,
                    "t14gw": message,
                    "t14ipv6": message,
                    "t14speed": message,
                    "t14mtu": message,
                }
                self.t14Info.append(dict(t14_dictionary))

    def t15_info(self):
        """# Populate the values for Table 15 - Zones."""
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            t15_dictionary = {}
            if not self.check_panorama_model(fw):
                for entry in fw.zones:
                    t15_dictionary["t15devicename"] = fw.hostname + fw.hapeername
                    t15_dictionary["t15zonename"] = entry["zone_name"]
                    t15_dictionary["t15zonetype"] = entry["zone_type"]
                    t15_dictionary["t15zoneprotection"] = entry["zone_protection"]
                    t15_dictionary["t15userid"] = entry["user_id"]
                    t15_dictionary["t15vsys"] = entry["vsys_name"]
                    self.t15Info.append(dict(t15_dictionary))
            else:
                t15_dictionary["t15devicename"] = message
                t15_dictionary["t15zonename"] = message
                t15_dictionary["t15zonetype"] = message
                t15_dictionary["t15zoneprotection"] = message
                t15_dictionary["t15userid"] = message
                t15_dictionary["t15vsys"] = message
                self.t15Info.append(dict(t15_dictionary))

    def t16_info(self):
        """Populate the values for Table 16 - IKE Profiles."""
        logger.debug("Running %s", self.func_name())
        t16_dictionary = {}
        ike_loop = 0
        for fw in self.pan_hosts:
            if not self.check_panorama_model(fw):
                if self.t18Count > 0:
                    for entry in self.t18UsedIKE:
                        for entry in fw.ike_crypto:
                            if (
                                    entry["ikeprofilename"]
                                    == self.t18UsedIKE[ike_loop]["ikeprofilename"]
                            ):
                                t16_dictionary["t16devicename"] = (
                                    fw.hostname + fw.hapeername if fw.ike_crypto else message
                                )
                                t16_dictionary["t16ikeprofilename"] = entry[
                                    "ikeprofilename"
                                ]
                                t16_dictionary["t16dhgroup"] = entry["dhgroup"]
                                t16_dictionary["t16authentication"] = entry[
                                    "authentication"
                                ]
                                t16_dictionary["t16encryption"] = entry["encryption"]
                                t16_dictionary["t16keylifetime"] = entry["keylifetime"]
                                t16_dictionary["t16ikev2authentication"] = entry[
                                    "v2authentication"
                                ]
                                self.t16Info.append(dict(t16_dictionary))
                                ike_loop += 1
                                if ike_loop == self.t18Count:
                                    break
                            else:
                                pass
                        break
                else:
                    t16_dictionary["t16devicename"] = message
                    t16_dictionary["t16ikeprofilename"] = message
                    t16_dictionary["t16dhgroup"] = message
                    t16_dictionary["t16authentication"] = message
                    t16_dictionary["t16encryption"] = message
                    t16_dictionary["t16keylifetime"] = message
                    t16_dictionary["t16ikev2authentication"] = message
                    self.t16Info.append(dict(t16_dictionary))
            else:
                t16_dictionary["t16devicename"] = message
                t16_dictionary["t16ikeprofilename"] = message
                t16_dictionary["t16dhgroup"] = message
                t16_dictionary["t16authentication"] = message
                t16_dictionary["t16encryption"] = message
                t16_dictionary["t16keylifetime"] = message
                t16_dictionary["t16ikev2authentication"] = message
                self.t16Info.append(dict(t16_dictionary))

    def t17_info(self):
        """# Populate the values for Table 17 – IPSec Profiles."""
        logger.debug("Running %s", self.func_name())
        t17_dictionary = {}
        ipsec_loop = 0
        for fw in self.pan_hosts:
            if not self.check_panorama_model(fw):
                t17_dictionary = {}
                if self.t19Count > 0:
                    for entry in self.t19UsedIPSec:
                        for entry in fw.ipsec_crypto:
                            if (
                                    entry["profilename"]
                                    == self.t19UsedIPSec[ipsec_loop]["t19ipseccrypto"]
                            ):
                                t17_dictionary["t17devicename"] = (
                                        fw.hostname + fw.hapeername
                                )
                                t17_dictionary["t17ipsecprofilename"] = entry[
                                    "profilename"
                                ]
                                t17_dictionary["t17dhgroup"] = entry["dhgroup"]
                                t17_dictionary["t17authentication"] = entry[
                                    "authentication"
                                ]
                                t17_dictionary["t17encryption"] = entry["encryption"]
                                t17_dictionary["t17ipsecprotocol"] = entry["protocol"]
                                t17_dictionary["t17lifetime"] = entry["lifetime"]
                                t17_dictionary["t17lifesize"] = entry["lifesize"]
                                self.t17Info.append(dict(t17_dictionary))
                                ipsec_loop += 1
                                if ipsec_loop == self.t19Count:
                                    break
                            else:
                                pass
                else:
                    t17_dictionary["t17devicename"] = message
                    t17_dictionary["t17ipsecprofilename"] = message
                    t17_dictionary["t17dhgroup"] = message
                    t17_dictionary["t17authentication"] = message
                    t17_dictionary["t17encryption"] = message
                    t17_dictionary["t17ipsecprotocol"] = message
                    t17_dictionary["t17lifetime"] = message
                    t17_dictionary["t17lifesize"] = message
                    self.t17Info.append(dict(t17_dictionary))
            else:
                t17_dictionary["t17devicename"] = message
                t17_dictionary["t17ipsecprofilename"] = message
                t17_dictionary["t17dhgroup"] = message
                t17_dictionary["t17authentication"] = message
                t17_dictionary["t17encryption"] = message
                t17_dictionary["t17ipsecprotocol"] = message
                t17_dictionary["t17lifetime"] = message
                t17_dictionary["t17lifesize"] = message
                self.t17Info.append(dict(t17_dictionary))

    def t18_info(self):
        """# Populate the values for Table 18 – IKE Gateway Configuration."""
        logger.debug("Running %s", self.func_name())
        t18_dictionary = {}
        t18TrackIKE = {}
        for fw in self.pan_hosts:
            if not self.check_panorama_model(fw):
                # t18Count = len(fw.ike_gw)
                if self.t18Count > 0:
                    for entry in fw.ike_gw:
                        t18_dictionary["t18devicename"] = fw.hostname + fw.hapeername
                        t18_dictionary["t18ikegwname"] = entry["ike_gw"]
                        t18_dictionary["t18ikeversion"] = entry["ike_version"]
                        t18_dictionary["t18addresstype"] = entry["address_type"]
                        if "interface" in entry:
                            t18_dictionary["t18interface"] = entry["interface"]
                        else:
                            t18_dictionary["t18interface"] = "None"
                        t18_dictionary["t18localaddress"] = entry["local_address"]
                        t18_dictionary["t18peeraddresstype"] = entry[
                            "peer_address_type"
                        ]
                        t18_dictionary["t18peeraddress"] = entry["peer_address"]
                        t18_dictionary["t18authentication"] = entry["authentication"]
                        t18_dictionary["t18localid"] = entry["local_id"]
                        t18_dictionary["t18peerid"] = entry["peer_id"]
                        t18_dictionary["t18ikecryptoprofile"] = entry["crypto_profile"]
                        t18TrackIKE["ikeprofilename"] = entry["crypto_profile"]
                        self.t18Info.append(dict(t18_dictionary))
                        self.t18UsedIKE.append(dict(t18TrackIKE))
                else:
                    t18_dictionary["t18devicename"] = message
                    t18_dictionary["t18ikegwname"] = message
                    t18_dictionary["t18ikeversion"] = message
                    t18_dictionary["t18addresstype"] = message
                    t18_dictionary["t18interface"] = message
                    t18_dictionary["t18localaddress"] = message
                    t18_dictionary["t18peeraddresstype"] = message
                    t18_dictionary["t18peeraddress"] = message
                    t18_dictionary["t18authentication"] = message
                    t18_dictionary["t18localid"] = message
                    t18_dictionary["t18peerid"] = message
                    t18_dictionary["t18ikecryptoprofile"] = message
                    t18_dictionary["ikeprofilename"] = message
                    self.t18Info.append(dict(t18_dictionary))
                    self.t18UsedIKE.append(dict(t18TrackIKE))
            else:
                t18_dictionary["t18devicename"] = message
                t18_dictionary["t18ikegwname"] = message
                t18_dictionary["t18ikeversion"] = message
                t18_dictionary["t18addresstype"] = message
                t18_dictionary["t18interface"] = message
                t18_dictionary["t18localaddress"] = message
                t18_dictionary["t18peeraddresstype"] = message
                t18_dictionary["t18peeraddress"] = message
                t18_dictionary["t18authentication"] = message
                t18_dictionary["t18localid"] = message
                t18_dictionary["t18peerid"] = message
                t18_dictionary["t18ikecryptoprofile"] = message
                t18_dictionary["ikeprofilename"] = message
                self.t18Info.append(dict(t18_dictionary))
                self.t18UsedIKE.append(dict(t18TrackIKE))

    def t19_info(self):
        """# Populate the values for Table 19 - IPSec Tunnel Configuration."""
        logger.debug("Running %s", self.func_name())
        t19_dictionary = {}
        t19TrackIPSec = {}
        for fw in self.pan_hosts:
            if not self.check_panorama_model(fw):
                self.t19Count = len(fw.ipsec_vpn)
                if self.t19Count > 0:
                    for entry in fw.ipsec_vpn:
                        t19_dictionary["t19devicename"] = fw.hostname + fw.hapeername
                        t19_dictionary["t19tunnelname"] = entry["tunnel_name"]
                        t19_dictionary["t19interface"] = entry["tunnel_interface"]
                        t19_dictionary["t19type"] = entry["type"]
                        t19_dictionary["t19addresstype"] = entry["address_type"]
                        t19_dictionary["t19ikegateway"] = entry["ike_gw"]
                        t19_dictionary["t19advancedoptions"] = entry["options"]
                        t19_dictionary["t19proxyids"] = entry["proxy_id"]
                        t19_dictionary["t19ipseccrypto"] = entry["ipsec_crypto"]
                        t19TrackIPSec["t19ipseccrypto"] = entry["ipsec_crypto"]
                        self.t19Info.append(dict(t19_dictionary))
                        self.t19UsedIPSec.append(dict(t19TrackIPSec))
                else:
                    t19_dictionary["t19devicename"] = message
                    t19_dictionary["t19tunnelname"] = message
                    t19_dictionary["t19interface"] = message
                    t19_dictionary["t19type"] = message
                    t19_dictionary["t19addresstype"] = message
                    t19_dictionary["t19ikegateway"] = message
                    t19_dictionary["t19advancedoptions"] = message
                    t19_dictionary["t19proxyids"] = message
                    t19_dictionary["t19ipseccrypto"] = message
                    t19TrackIPSec["t19ipseccrypto"] = message
                    self.t19Info.append(dict(t19_dictionary))
                    self.t19UsedIPSec.append(dict(t19TrackIPSec))
            else:
                t19_dictionary["t19devicename"] = message
                t19_dictionary["t19tunnelname"] = message
                t19_dictionary["t19interface"] = message
                t19_dictionary["t19type"] = message
                t19_dictionary["t19addresstype"] = message
                t19_dictionary["t19ikegateway"] = message
                t19_dictionary["t19advancedoptions"] = message
                t19_dictionary["t19proxyids"] = message
                t19_dictionary["t19ipseccrypto"] = message
                t19TrackIPSec["t19ipseccrypto"] = message
                self.t19Info.append(dict(t19_dictionary))
                self.t19UsedIPSec.append(dict(t19TrackIPSec))

    def t20_info(self):
        """# Populate the values for Table 20 – GlobalProtect Portal Information."""
        logger.debug("Running %s", self.func_name())
        t20_dictionary = {}
        for fw in self.pan_hosts:
            if not self.check_panorama_model(fw):
                for entry in fw.gp_portals:
                    if entry != {}:
                        t20_dictionary["t20devicename"] = fw.hostname + fw.hapeername
                        t20_dictionary["t20interface"] = entry["interface"].text
                        t20_dictionary["t20authprofile"] = entry["auth_profile"].text
                        t20_dictionary["t20ipaddress"] = entry["address"]
                        t20_dictionary["t20agentprofiles"] = entry["agent_profiles"]
                        t20_dictionary["t20gateways"] = entry["gateways"]
                        self.t20Info.append(dict(t20_dictionary))
                    else:
                        t20_dictionary["t20devicename"] = message
                        t20_dictionary["t20interface"] = message
                        t20_dictionary["t20authprofile"] = message
                        t20_dictionary["t20ipaddress"] = message
                        t20_dictionary["t20agentprofiles"] = message
                        t20_dictionary["t20gateways"] = message
                        self.t20Info.append(dict(t20_dictionary))
            else:
                t20_dictionary["t20devicename"] = message
                t20_dictionary["t20interface"] = message
                t20_dictionary["t20authprofile"] = message
                t20_dictionary["t20ipaddress"] = message
                t20_dictionary["t20agentprofiles"] = message
                t20_dictionary["t20gateways"] = message
                self.t20Info.append(dict(t20_dictionary))

    def t21_info(self):
        """# Populate the values for Table 21 – GlobalProtect Gateway Information.

        There is no way to distinguish between internal and external gateways
        just by looking at gateway part of configuration.
        If we look into portal part this can be achieved, however this might not
        always be reliable as Portal and Gateway might reside on different firewalls.
        Hence decided to put all gateways in table 20. Consultant will manually need to
        choose Internal Gateways and copy to Table 21.
        Alternatively, we can update table header to reflect Gateways instead of internal
        and External
        """
        logger.debug("Running %s", self.func_name())
        t21_dictionary = {}
        for fw in self.pan_hosts:
            if not self.check_panorama_model(fw):
                if fw.gp_gateways:
                    for entry in fw.gp_gateways:
                        if entry != {}:
                            t21_dictionary["t21devicename"] = fw.hostname + fw.hapeername
                            t21_dictionary["t21interface"] = entry["interface"]
                            t21_dictionary["t21authprofile"] = entry["auth_profile"].text
                            t21_dictionary["t21ipaddress"] = entry["address"]
                            t21_dictionary["t21agentprofiles"] = entry["agent_profiles"]
                            t21_dictionary["t21dhcppool"] = entry["dhcp_pool"]
                            t21_dictionary["t21tunnelmode"] = entry["tunnel_mode"].text
                            self.t21Info.append(dict(t21_dictionary))
                else:
                    t21_dictionary["t21devicename"] = message
                    t21_dictionary["t21interface"] = message
                    t21_dictionary["t21authprofile"] = message
                    t21_dictionary["t21ipaddress"] = message
                    t21_dictionary["t21agentprofiles"] = message
                    t21_dictionary["t21dhcppool"] = message
                    t21_dictionary["t21tunnelmode"] = message
                    self.t21Info.append(dict(t21_dictionary))
            else:
                t21_dictionary["t21devicename"] = message
                t21_dictionary["t21interface"] = message
                t21_dictionary["t21authprofile"] = message
                t21_dictionary["t21ipaddress"] = message
                t21_dictionary["t21agentprofiles"] = message
                t21_dictionary["t21dhcppool"] = message
                t21_dictionary["t21tunnelmode"] = message
                self.t21Info.append(dict(t21_dictionary))

    def t23_info(self):
        """# Populate the values for Table 23 – HIP Profile Information."""
        logger.debug("Running %s", self.func_name())
        t23_dictionary = {}
        for fw in self.pan_hosts:
            if not self.check_panorama_model(fw):
                if fw.hip:
                    for entry in fw.hip:
                        t23_dictionary["t23devicename"] = fw.hostname + fw.hapeername if entry != {} else message
                        t23_dictionary["t23name"] = entry["name"] if entry != {} else message
                        t23_dictionary["t23parameters"] = entry["parameters"] if entry != {} else message
                        self.t23Info.append(dict(t23_dictionary))
                else:
                    t23_dictionary["t23devicename"] = message
                    t23_dictionary["t23name"] = message
                    t23_dictionary["t23parameters"] = message
                    self.t23Info.append(dict(t23_dictionary))
            else:
                t23_dictionary["t23devicename"] = message
                t23_dictionary["t23name"] = message
                t23_dictionary["t23parameters"] = message
                self.t23Info.append(dict(t23_dictionary))

    def t24_info(self):
        """# Populate the values for Table 24 - Panorama MGT Port Settings

        # Pending Implementation of HA priority
        """
        logger.debug("Running %s", self.func_name())

        for panorama in self.pan_hosts:
            t24_dictionary = {
                "t24devicename": panorama.hostname if self.check_panorama_model(panorama) else message,
                "t24mgmtIP": panorama.mgmtinfo["ip"] if self.check_panorama_model(panorama) else message,
                "t24mgmtnetmask": panorama.mgmtinfo["mask"] if self.check_panorama_model(panorama) else message,
                "t24mgmtgateway": panorama.mgmtinfo["gw"] if self.check_panorama_model(panorama) else message,
                "t24mgmtipv6": panorama.mgmtinfo["ipv6"] if self.check_panorama_model(panorama) else message,
                "t24mgmtspeed": panorama.mgmtinfo["speed"] if self.check_panorama_model(panorama) else message,
                "t24mgmtmtu": panorama.mgmtinfo["mtu"] if self.check_panorama_model(panorama) else message,
                "t24mgmtservices": panorama.mgmtinfo["services"] if self.check_panorama_model(panorama) else message,
                "t24mgmtpermittedips": panorama.mgmtinfo["permitted_ips"] if self.check_panorama_model(
                    panorama) else message,
                "t24hapriority": panorama.hapriority if self.check_panorama_model(panorama) else message,
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
            else:
                t25_dictionary["t25devicename"] = message
                t25_dictionary["t25templatename"] = message
                t25_dictionary["t25stackname"] = message
                t25_dictionary["t25stackmembers"] = message
                self.t25Info.append(dict(t25_dictionary))

    def t55_info(self):
        t55_dictionary = {}
        for panorama in self.pan_hosts:
            if self.check_panorama_model(panorama):
                for entry in panorama.templates_prisma:
                    t55_dictionary["t55templatename"] = entry["template_name"]
                    t55_dictionary["t55stackname"] = entry["stack_name"]
                    self.t55Info.append(dict(t55_dictionary))
            else:
                t55_dictionary["t55templatename"] = message
                t55_dictionary["t55stackname"] = message
                self.t55Info.append(dict(t55_dictionary))

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
            else:
                t26_dictionary["t26devicename"] = message
                t26_dictionary["t26tier1"] = message
                t26_dictionary["t26tier2"] = message
                t26_dictionary["t26tier3"] = message
                t26_dictionary["t26tier4"] = message
                t26_dictionary["t26masterdevice"] = message
                self.t26Info.append(dict(t26_dictionary))

    def t27_info(self):
        """# Populate the values for Table 27 – Log Forwarding Profile."""
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            t27_dictionary = {}
            for entry in fw.logforwarding if fw.logforwarding else self.temp:
                t27_dictionary["t27devicename"] = fw.hostname + fw.hapeername if not self.check_panorama_model(
                    fw) and fw.logforwarding else message
                t27_dictionary["t27profilename"] = entry["profile_name"] if not self.check_panorama_model(
                    fw) and fw.logforwarding else message
                t27_dictionary["t27logtype"] = entry["log_type"] if not self.check_panorama_model(
                    fw) and fw.logforwarding else message
                t27_dictionary["t27panorama"] = entry["panorama"] if not self.check_panorama_model(
                    fw) and fw.logforwarding else message
                t27_dictionary["t27snmp"] = entry["snmp"] if not self.check_panorama_model(
                    fw) and fw.logforwarding else message
                t27_dictionary["t27email"] = entry["email"] if not self.check_panorama_model(
                    fw) and fw.logforwarding else message
                t27_dictionary["t27syslog"] = entry["syslog"] if not self.check_panorama_model(
                    fw) and fw.logforwarding else message
                self.t27Info.append(dict(t27_dictionary))

    def t28_info(self):
        """Populate the values for Table 28 – Antivirus Profile."""
        logger.debug("Running %s", self.func_name())
        for fw in self.pan_hosts:
            t28_dictionary = {}
            for entry in fw.antivirus if fw.antivirus else self.temp:
                t28_dictionary["t28devicename"] = fw.hostname + fw.hapeername if not self.check_panorama_model(
                    fw) else message
                t28_dictionary["t28avprofilename"] = entry["av_profile_name"] if not self.check_panorama_model(
                    fw) else message
                t28_dictionary["t28decoders"] = entry["av_decoders"] if not self.check_panorama_model(fw) else message
                t28_dictionary["t28actions"] = entry["av_actions"] if not self.check_panorama_model(fw) else message
                t28_dictionary["t28wfactions"] = entry["av_wf_actions"] if not self.check_panorama_model(
                    fw) else message
                self.t28Info.append(dict(t28_dictionary))

    def t29_info(self):
        """# Populate the values for Table 29 – Anti-spyware Profile."""
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            t29_dictionary = {}
            for entry in fw.antispy if fw.antispy else self.temp:
                t29_dictionary["t29devicename"] = fw.hostname + fw.hapeername if not self.check_panorama_model(
                    fw) else message
                t29_dictionary["t29asprofilename"] = entry["as_profile_name"] if not self.check_panorama_model(
                    fw) else message
                t29_dictionary["t29severity"] = entry["as_severity"] if not self.check_panorama_model(fw) else message
                t29_dictionary["t29actions"] = entry["as_actions"] if not self.check_panorama_model(fw) else message
                t29_dictionary["t29dnssink"] = entry["as_dnssink"] if not self.check_panorama_model(fw) else message
                self.t29Info.append(dict(t29_dictionary))

    def t30_info(self):
        """# Populate the values for Table 30 – Vulnerability Profiles."""
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            t30_dictionary = {}
            for entry in fw.vulnerability if fw.vulnerability else self.temp:
                t30_dictionary["t30devicename"] = fw.hostname + fw.hapeername if not self.check_panorama_model(
                    fw) else message
                t30_dictionary["t30vprofilename"] = entry["vp_profile_name"] if not self.check_panorama_model(
                    fw) else message
                t30_dictionary["t30severity"] = entry["vp_severity"] if not self.check_panorama_model(fw) else message
                t30_dictionary["t30action"] = entry["vp_actions"] if not self.check_panorama_model(fw) else message
                t30_dictionary["t30rulename"] = entry["vp_rules"] if not self.check_panorama_model(fw) else message
                self.t30Info.append(dict(t30_dictionary))

    def t31_info(self):
        """# Populate the values for Table 31 – URL Filtering Profiles."""
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            t31_dictionary = {}
            for entry in fw.url if fw.url else self.temp:
                t31_dictionary["t31devicename"] = fw.hostname + fw.hapeername if not self.check_panorama_model(
                    fw) else message
                t31_dictionary["t31profilename"] = entry["url_prof_name"] if not self.check_panorama_model(
                    fw) else message
                t31_dictionary["t31blocked"] = entry["block"] if not self.check_panorama_model(fw) else message
                t31_dictionary["t31allow"] = entry["allow"] if not self.check_panorama_model(fw) else message
                t31_dictionary["t31alert"] = entry["alert"] if not self.check_panorama_model(fw) else message
                t31_dictionary["t31continue"] = entry["continue"] if not self.check_panorama_model(fw) else message
                t31_dictionary["t31override"] = entry["override"] if not self.check_panorama_model(fw) else message
                t31_dictionary["t31credential"] = entry["credential"] if not self.check_panorama_model(fw) else message
                self.t31Info.append(dict(t31_dictionary))

    def t32_info(self):
        """# Populate the values for Table 32 – URL Filtering Profiles."""
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            t32_dictionary = {}
            for entry in fw.wildfire if fw.wildfire else self.temp:
                t32_dictionary["t32devicename"] = fw.hostname + fw.hapeername if not self.check_panorama_model(
                    fw) else message
                t32_dictionary["t32profilename"] = entry["wf_prof_name"] if not self.check_panorama_model(
                    fw) else message
                t32_dictionary["t32applications"] = entry["wf_applications"] if not self.check_panorama_model(
                    fw) else message
                t32_dictionary["t32filetypes"] = entry["wf_filetypes"] if not self.check_panorama_model(fw) else message
                t32_dictionary["t32direction"] = entry["wf_direction"] if not self.check_panorama_model(fw) else message
                t32_dictionary["t32analysis"] = entry["wf_analysis"] if not self.check_panorama_model(fw) else message
                self.t32Info.append(dict(t32_dictionary))

    def t33_info(self):
        """# Populate the values for Table 33 – File Blocking Profile Details."""
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            t33_dictionary = {}
            for entry in fw.fileblocking if fw.fileblocking else self.temp:
                t33_dictionary["t33devicename"] = fw.hostname + fw.hapeername if not self.check_panorama_model(
                    fw) else message
                t33_dictionary["t33rulename"] = entry["fb_rule_name"] if not self.check_panorama_model(fw) else message
                t33_dictionary["t33applications"] = entry["fb_applications"] if not self.check_panorama_model(
                    fw) else message
                t33_dictionary["t33filetypes"] = entry["fb_filetypes"] if not self.check_panorama_model(fw) else message
                t33_dictionary["t33direction"] = entry["fb_direction"] if not self.check_panorama_model(fw) else message
                t33_dictionary["t33action"] = entry["fb_action"] if not self.check_panorama_model(fw) else message
                self.t33Info.append(dict(t33_dictionary))

    def t34_info(self):
        """# Populate the values for Table 35 – Data Filtering Profile Details."""
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            t34_dictionary = {}
            for entry in fw.data_objects if fw.data_objects else self.temp:
                t34_dictionary["t34devicename"] = fw.hostname + fw.hapeername if not self.check_panorama_model(
                    fw) and fw.data_objects else message
                t34_dictionary["t34profilename"] = entry["profile_name"] if not self.check_panorama_model(
                    fw) and fw.data_objects else message
                t34_dictionary["t34patterntype"] = entry["pattern_type"] if not self.check_panorama_model(
                    fw) and fw.data_objects else message
                t34_dictionary["t34name"] = entry["dfo_name"] if not self.check_panorama_model(
                    fw) and fw.data_objects else message
                t34_dictionary["t34filetypes"] = entry["file_types"] if not self.check_panorama_model(
                    fw) and fw.data_objects else message
                t34_dictionary["t34pattern"] = entry["pattern"] if not self.check_panorama_model(
                    fw) and fw.data_objects else message
                self.t34Info.append(dict(t34_dictionary))

    def t35_info(self):
        """# Populate the values for Table 35 – Data Filtering Profile Details."""
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            t35_dictionary = {}
            for entry in fw.data_filtering if fw.data_filtering else self.temp:
                t35_dictionary["t35devicename"] = fw.hostname + fw.hapeername if not self.check_panorama_model(
                    fw) and fw.data_filtering else message
                t35_dictionary["t35rulename"] = entry["df_rule_name"] if not self.check_panorama_model(
                    fw) and fw.data_filtering else message
                t35_dictionary["t35apps"] = entry["df_applications"] if not self.check_panorama_model(
                    fw) and fw.data_filtering else message
                t35_dictionary["t35filetype"] = entry["df_filetypes"] if not self.check_panorama_model(
                    fw) and fw.data_filtering else message
                t35_dictionary["t35direction"] = entry["df_direction"] if not self.check_panorama_model(
                    fw) and fw.data_filtering else message
                t35_dictionary["t35alert"] = entry["df_alert"] if not self.check_panorama_model(
                    fw) and fw.data_filtering else message
                t35_dictionary["t35block"] = entry["df_block"] if not self.check_panorama_model(
                    fw) and fw.data_filtering else message
                t35_dictionary["t35patterns"] = entry["df_patterns"] if not self.check_panorama_model(
                    fw) and fw.data_filtering else message
                self.t35Info.append(dict(t35_dictionary))

    def t36_info(self):
        """# Populate the values for Table 35 – Data Filtering Profile Details."""
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            t36_dictionary = {}
            for entry in fw.dos if fw.dos else self.temp:
                t36_dictionary["t36devicename"] = fw.hostname + fw.hapeername if not self.check_panorama_model(
                    fw) and fw.dos else message
                t36_dictionary["t36profilename"] = entry["dos_rule_name"] if not self.check_panorama_model(
                    fw) and fw.dos else message
                t36_dictionary["t36type"] = entry["dos_type"] if not self.check_panorama_model(
                    fw) and fw.dos else message
                t36_dictionary["t36syn"] = entry["dos_syn"] if not self.check_panorama_model(fw) and fw.dos else message
                t36_dictionary["t36udp"] = entry["dos_udp"] if not self.check_panorama_model(fw) and fw.dos else message
                t36_dictionary["t36icmp"] = entry["dos_icmp"] if not self.check_panorama_model(
                    fw) and fw.dos else message
                t36_dictionary["t36icmp6"] = entry["dos_icmp6"] if not self.check_panorama_model(
                    fw) and fw.dos else message
                t36_dictionary["t36flood"] = entry["dos_flood"] if not self.check_panorama_model(
                    fw) and fw.dos else message
                t36_dictionary["t36rps"] = entry["dos_rps"] if not self.check_panorama_model(fw) and fw.dos else message
                self.t36Info.append(dict(t36_dictionary))

    def t37_info(self):
        """# Populate the values for Table 37 – Security Profile Group Details."""
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            t37_dictionary = {}
            for entry in fw.secprof if fw.secprof else self.temp:
                t37_dictionary["t37devicename"] = fw.hostname + fw.hapeername if not self.check_panorama_model(
                    fw) else message
                t37_dictionary["t37groupname"] = entry["group_name"] if not self.check_panorama_model(fw) else message
                t37_dictionary["t37av"] = entry["av"].text if not self.check_panorama_model(fw) else message
                t37_dictionary["t37as"] = entry["as"].text if not self.check_panorama_model(fw) else message
                t37_dictionary["t37vp"] = entry["vp"].text if not self.check_panorama_model(fw) else message
                t37_dictionary["t37fb"] = entry["fb"].text if not self.check_panorama_model(fw) else message
                t37_dictionary["t37df"] = entry["df"] if not self.check_panorama_model(fw) else message
                t37_dictionary["t37wf"] = entry["wf"].text if not self.check_panorama_model(fw) else message
                if entry == '1':
                    t37_dictionary["t37url"] = message
                elif entry["url"] is not None:
                    t37_dictionary["t37url"] = entry["url"].text if not self.check_panorama_model(fw) else message
                else:
                    t37_dictionary["t37url"] = entry["url"] if not self.check_panorama_model(fw) else message
                self.t37Info.append(dict(t37_dictionary))

    def t38_info(self):
        """# Populate the values for Table 38 – Dynamic Updates Schedule Details."""
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            t38_dictionary = {}
            for entry in fw.update_sched if fw.update_sched else self.temp:
                t38_dictionary["t38devicename"] = fw.hostname + fw.hapeername if not self.check_panorama_model(
                    fw) else message
                t38_dictionary["t38type"] = entry["type"] if not self.check_panorama_model(fw) else message
                if entry == '1':
                    t38_dictionary["t38recurrence"] = message
                elif type(entry["recurrence"]) == str:
                    t38_dictionary["t38recurrence"] = entry["recurrence"] if not self.check_panorama_model(
                        fw) else message
                else:
                    t38_dictionary["t38recurrence"] = entry["recurrence"].text if not self.check_panorama_model(
                        fw) else message
                if entry == '1':
                    t38_dictionary["t38time"] = message
                elif entry["time"] is None:
                    t38_dictionary["t38time"] = entry["time"] if not self.check_panorama_model(fw) else message
                else:
                    t38_dictionary["t38time"] = entry["time"].text if not self.check_panorama_model(fw) else message
                if entry == '1':
                    t38_dictionary["t38action"] = message
                elif entry["action"] is None:
                    t38_dictionary["t38action"] = entry["action"] if not self.check_panorama_model(fw) else message
                else:
                    t38_dictionary["t38action"] = entry["action"].text if not self.check_panorama_model(fw) else message
                if entry == '1':
                    t38_dictionary["t38threshold"] = message
                elif entry["threshold"] is None:
                    t38_dictionary["t38threshold"] = entry["threshold"] if not self.check_panorama_model(
                        fw) else message
                else:
                    t38_dictionary["t38threshold"] = entry["threshold"].text if not self.check_panorama_model(
                        fw) else message
                self.t38Info.append(dict(t38_dictionary))

    def t39_info(self):
        """# Populate the values for Table 39 – User-ID Source Details."""
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            t39_dictionary = {}
            for entry in fw.userid if fw.userid else self.temp:
                if entry != {}:
                    t39_dictionary["t39devicename"] = fw.hostname + fw.hapeername if not self.check_panorama_model(
                        fw) and fw.userid else message
                    t39_dictionary["t39source"] = entry["source"] if not self.check_panorama_model(
                        fw) and fw.userid else message
                    t39_dictionary["t39type"] = entry["type"] if not self.check_panorama_model(
                        fw) and fw.userid else message
                    t39_dictionary["t39ipaddress"] = entry["ip_address"] if not self.check_panorama_model(
                        fw) and fw.userid else message
                    t39_dictionary["t39port"] = entry["port"] if not self.check_panorama_model(
                        fw) and fw.userid else message
                    t39_dictionary["t39interface"] = entry["interface"] if not self.check_panorama_model(
                        fw) and fw.userid else message
                    self.t39Info.append(dict(t39_dictionary))

    def t40_info(self):
        """# Populate the values for Table 40 – Group Mapping Profile Details."""
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            t40_dictionary = {}
            for entry in fw.groups if fw.groups else self.temp:
                t40_dictionary["t40devicename"] = fw.hostname + fw.hapeername if not self.check_panorama_model(
                    fw) and fw.groups else message
                t40_dictionary["t40serverprofile"] = entry["profile"] if not self.check_panorama_model(
                    fw) and fw.groups else message
                t40_dictionary["t40domain"] = entry["domain"] if not self.check_panorama_model(
                    fw) and fw.groups else message
                t40_dictionary["t40group"] = entry["group"] if not self.check_panorama_model(
                    fw) and fw.groups else message
                t40_dictionary["t40user"] = entry["user"] if not self.check_panorama_model(
                    fw) and fw.groups else message
                t40_dictionary["t40attributes"] = entry["attributes"] if not self.check_panorama_model(
                    fw) and fw.groups else message
                t40_dictionary["t40includelist"] = entry["include_list"] if not self.check_panorama_model(
                    fw) and fw.groups else message
                self.t40Info.append(dict(t40_dictionary))

    def t41_info(self):
        """# Populate the values for Table 41 – SNMP Server Profile."""
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            if not self.check_panorama_model(fw):
                t41_dictionary = {}
                if fw.snmpv2_manager:
                    for entry in fw.snmpv2_manager:
                        t41_dictionary["t41devicename"] = fw.hostname + fw.hapeername
                        t41_dictionary["t41profilename"] = entry["profile_name"]
                        t41_dictionary["t41managername"] = entry["manager_name"]
                        t41_dictionary["t41managerip"] = entry["manager_ip"]
                        t41_dictionary["t41communitystring"] = entry["manager_community"]
                        self.t41Info.append(dict(t41_dictionary))
                else:
                    t41_dictionary["t41devicename"] = message
                    t41_dictionary["t41profilename"] = message
                    t41_dictionary["t41managername"] = message
                    t41_dictionary["t41managerip"] = message
                    t41_dictionary["t41communitystring"] = message
                    self.t41Info.append(dict(t41_dictionary))

        for panorama in self.pan_hosts:
            if self.check_panorama_model(panorama):
                t41_dictionary = {}
                if panorama.snmpv2_manager:
                    for entry in panorama.snmpv2_manager:
                        t41_dictionary["t41devicename"] = panorama.name
                        t41_dictionary["t41profilename"] = entry["profile_name"]
                        t41_dictionary["t41managername"] = entry["manager_name"]
                        t41_dictionary["t41managerip"] = entry["manager_ip"]
                        t41_dictionary["t41communitystring"] = entry["manager_community"]
                        self.t41Info.append(dict(t41_dictionary))
                else:
                    t41_dictionary["t41devicename"] = message
                    t41_dictionary["t41profilename"] = message
                    t41_dictionary["t41managername"] = message
                    t41_dictionary["t41managerip"] = message
                    t41_dictionary["t41communitystring"] = message
                    self.t41Info.append(dict(t41_dictionary))

    def t42_info(self):
        """Populate the values for Table 42 – SNMPv2 Settings."""
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            if not self.check_panorama_model(fw):
                t42_dictionary = {}
                for entry in fw.snmpv2_system if fw.snmpv2_system else self.temp:
                    t42_dictionary["t42devicename"] = fw.hostname + fw.hapeername if fw.snmpv2_system else message
                    t42_dictionary["t42location"] = entry["location"] if fw.snmpv2_system else message
                    t42_dictionary["t42contact"] = entry["contact"] if fw.snmpv2_system else message
                    t42_dictionary["t42version"] = entry["version"] if fw.snmpv2_system else message
                    t42_dictionary["t42community"] = entry["settings_community"] if fw.snmpv2_system else message
                    self.t42Info.append(dict(t42_dictionary))
        for panorama in self.pan_hosts:
            if self.check_panorama_model(panorama):
                t42_dictionary = {}
                for entry in panorama.snmpv2_system if panorama.snmpv2_system else self.temp:
                    t42_dictionary["t42devicename"] = panorama.name if panorama.snmpv2_system else message
                    t42_dictionary["t42location"] = entry["location"] if panorama.snmpv2_system else message
                    t42_dictionary["t42contact"] = entry["contact"] if panorama.snmpv2_system else message
                    t42_dictionary["t42version"] = entry["version"] if panorama.snmpv2_system else message
                    t42_dictionary["t42community"] = entry["settings_community"] if panorama.snmpv2_system else message
                    self.t42Info.append(dict(t42_dictionary))

    def t43_info(self):
        """# Populate the values for Table 43 – Views."""
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            if not self.check_panorama_model(fw):
                t43_dictionary = {}
                for entry in fw.snmpv3 if fw.snmpv3 else self.temp:
                    t43_dictionary["t43devicename"] = fw.hostname + fw.hapeername if fw.snmpv3 else message
                    t43_dictionary["t43name"] = entry["name"] if fw.snmpv3 else message
                    t43_dictionary["t43view"] = entry["view"] if fw.snmpv3 else message
                    t43_dictionary["t43oid"] = entry["oid"] if fw.snmpv3 else message
                    t43_dictionary["t43option"] = entry["option"] if fw.snmpv3 else message
                    t43_dictionary["t43mask"] = entry["mask"] if fw.snmpv3 else message
                    self.t43Info.append(dict(t43_dictionary))

        for panorama in self.pan_hosts:
            t43_dictionary = {}
            for entry in panorama.snmpv3 if panorama.snmpv3 else self.temp:
                if self.check_panorama_model(panorama):
                    t43_dictionary["t43devicename"] = panorama.name if panorama.snmpv3 else message
                    t43_dictionary["t43name"] = entry["name"] if panorama.snmpv3 else message
                    t43_dictionary["t43view"] = entry["view"] if panorama.snmpv3 else message
                    t43_dictionary["t43oid"] = entry["oid"] if panorama.snmpv3 else message
                    t43_dictionary["t43option"] = entry["option"] if panorama.snmpv3 else message
                    t43_dictionary["t43mask"] = entry["mask"] if panorama.snmpv3 else message
                    self.t43Info.append(dict(t43_dictionary))

    def t44_info(self):
        """# Populate the values for Table 44 – Users."""
        logger.debug("Running %s", self.func_name())

        for fw in self.pan_hosts:
            if not self.check_panorama_model(fw):
                t44_dictionary = {}
                for entry in fw.snmpv3 if fw.snmpv3 else self.temp:
                    t44_dictionary["t44devicename"] = fw.hostname + fw.hapeername if fw.snmpv3 else message
                    t44_dictionary["t44users"] = entry["users"] if fw.snmpv3 else message
                    t44_dictionary["t44view"] = entry["user_view"] if fw.snmpv3 else message
                    self.t44Info.append(dict(t44_dictionary))
        for panorama in self.pan_hosts:
            if self.check_panorama_model(panorama):
                t44_dictionary = {}
                for entry in panorama.snmpv3 if panorama.snmpv3 else self.temp:
                    t44_dictionary["t44devicename"] = panorama.name if panorama.snmpv3 else message
                    t44_dictionary["t44users"] = entry["users"] if panorama.snmpv3 else message
                    t44_dictionary["t44view"] = entry["user_view"] if panorama.snmpv3 else message
                    self.t44Info.append(dict(t44_dictionary))

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
            "t8": self.t8Info,
            "t9": self.t9Info,
            "t10": self.t10Info,
            "t11": self.t11Info,
            "t12": self.t12Info,
            "t13": self.t13Info,
            "t14": self.t14Info,
            "t15": self.t15Info,
            "t16": self.t16Info,
            "t17": self.t17Info,
            "t18": self.t18Info,
            "t19": self.t19Info,
            "t20": self.t20Info,
            "t21": self.t21Info,
            "t23": self.t23Info,
            "t24": self.t24Info,
            "t25": self.t25Info,
            "t26": self.t26Info,
            "t27": self.t27Info,
            "t28": self.t28Info,
            "t29": self.t29Info,
            "t30": self.t30Info,
            "t31": self.t31Info,
            "t32": self.t32Info,
            "t33": self.t33Info,
            "t34": self.t34Info,
            "t35": self.t35Info,
            "t36": self.t36Info,
            "t37": self.t37Info,
            "t38": self.t38Info,
            "t39": self.t39Info,
            "t40": self.t40Info,
            "t41": self.t41Info,
            "t42": self.t42Info,
            "t43": self.t43Info,
            "t44": self.t44Info,
            "t55": self.t55Info
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
        self.t8Info.clear()
        self.t9Info.clear()
        self.t10Info.clear()
        self.t11Info.clear()
        self.t12Info.clear()
        self.t13Info.clear()
        self.t14Info.clear()
        self.t15Info.clear()
        self.t16Info.clear()
        self.t17Info.clear()
        self.t18Info.clear()
        self.t19Info.clear()
        self.t20Info.clear()
        self.t21Info.clear()
        self.t23Info.clear()
        self.t24Info.clear()
        self.t25Info.clear()
        self.t26Info.clear()
        self.t27Info.clear()
        self.t28Info.clear()
        self.t29Info.clear()
        self.t30Info.clear()
        self.t31Info.clear()
        self.t32Info.clear()
        self.t33Info.clear()
        self.t34Info.clear()
        self.t35Info.clear()
        self.t36Info.clear()
        self.t37Info.clear()
        self.t38Info.clear()
        self.t39Info.clear()
        self.t40Info.clear()
        self.t41Info.clear()
        self.t42Info.clear()
        self.t43Info.clear()
        self.t44Info.clear()
        self.t18Count = 0
        self.t18UsedIKE.clear()
        self.t19Count = 0
        self.t19UsedIPSec.clear()
        self.t55Info.clear()

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
        self.t8_info()
        self.t9_info()
        self.t10_info()
        self.t11_info()
        self.t12_info()
        self.t13_info()  # needs working mgmtinfo (nested dict)
        self.t14_info()  # needs working mgmtinfo (nested dict)
        self.t15_info()
        self.t18_info()  # this one is out of order for a reason
        self.t19_info()  # this one is out of order for a reason
        self.t16_info()
        self.t17_info()
        self.t20_info()
        self.t21_info()
        self.t23_info()
        self.t24_info()
        self.t25_info()
        self.t26_info()
        self.t27_info()
        self.t28_info()
        self.t29_info()
        self.t30_info()
        self.t31_info()
        self.t32_info()
        self.t33_info()
        self.t34_info()
        self.t35_info()
        self.t36_info()
        self.t37_info()
        self.t38_info()
        self.t39_info()
        self.t40_info()
        self.t41_info()
        self.t42_info()
        self.t43_info()
        self.t55_info()
        self.t44_info()
        self.clean()

    def gen_doc(self):
        """Generate the document.

        # Write out the completed word document
        """
        logger.debug("Setting input template to: %s", self.doc_path)
        try:
            self.template.save(self.output_path)
        except Exception:
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
