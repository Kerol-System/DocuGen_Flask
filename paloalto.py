"""The SwiftDoc Project."""

import logging
import logging.config

logging.config.fileConfig(
    "logging.conf",
    defaults={"logfilename": "SwiftDoc.log"},
    disable_existing_loggers=False,
)
logger = logging.getLogger(__name__)


"""
class PaloBaseClass(ABC):
    def __init__(self, value):
        self.value = value
        super().__init__()

    @abstractmethod
"""


class PaloPanorama:
    """Class representing a Panorama entry."""
    panorama_models = ["Panorama", "M-100", "M-500", "M-200", "M-600"]
    mgmtinfo = {}
    model = ""
    panos = ""
    licenses = ""
    admins = []
    opmode = ""  # log collector or panorama?
    hapriority = "HA not enabled"
    hainfo = {}
    hapeername = ""
    haotherinfo = {}
    templates = []
    templates_prisma = []
    devicegroups = []
    snmpv2_manager = []
    snmpv2_system = []
    snmpv3 = []

    def __init__(self, hostname, serial):
        """Make a Panorama."""
        self.hostname = hostname
        self.serial = serial


class PaloFirewall:
    """Class representing a firewall entry."""

    mgmtinfo = {}
    model = ""
    multivsys = ""
    panos = ""
    licenses = ""
    admins = []
    vsys = []
    hainfo = {}
    hapeername = ""
    haotherinfo = {}
    logintsettings = {}
    interfaces = {}
    antivirus = []
    antispy = []
    vulnerability = []
    url = []
    wildfire = []
    fileblocking = []
    update_sched = []
    secprof = []
    data_filtering = []
    data_objects = []
    dos = []
    ike_crypto = []
    ipsec_crypto = []
    ike_gw = []
    ipsec_vpn = []
    interfaces = []
    zones = []
    logforwarding = []
    snmpv2_manager = []
    snmpv2_system = []
    snmpv3 = []
    gp_portals = []
    gp_gateways = []
    hip = []
    groups = []
    userid = []

    def __init__(self, hostname, serial):
        """Make a firewall."""
        self.hostname = hostname
        self.serial = serial


"""
__author__     = 'Franklin Diaz'
__copyright__  = '© 2021 Palo Alto Networks, Inc. All rights reserved.'
__license__    = 'https://www.paloaltonetworks.com/legal/script-software-license-1-0.pdf'
__version__    = '0.1'
__email__      = 'fdiaz@paloaltonetworks.com'
"""
