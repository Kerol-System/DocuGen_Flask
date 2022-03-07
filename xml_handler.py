"""The SwiftDoc Project."""

import logging
import logging.config

import defusedxml.ElementTree as et

logging.config.fileConfig(
    "logging.conf",
    defaults={"logfilename": "SwiftDoc.log"},
    disable_existing_loggers=False,
)
logger = logging.getLogger(__name__)


class PanXMLHandler:
    """Methods for XML."""

    config_root = ""

    def __init__(self, config_file):
        self.config_file = config_file

    def set_conf_root(self):
        """[summary]"""
        conf = open(self.config_file)
        tree = et.parse(conf)
        self.config_root = tree.getroot()
        # logger.debug("Config root set to: %s", et.tostring(self.config_root, encoding='utf8').decode('utf8'))

    def get_userid(self):
        """ """
        logger.debug("Start PanXMLHandler.get_userid()")

        userid_dict = {}
        userid_dict_list = []
        source = ""
        type = ""
        ip_address = ""
        port = ""
        interface = ""
        # Captive Portal
        for agent in self.config_root.findall(".//captive-portal"):
            source = "Captive Portal"
            if agent.find("./mode"):
                if agent.find("./redirect-host"):
                    ip_address = agent.find("./redirect-host").text
                    type = "Redirect"
                else:
                    type = "Transparent"
                port = "N/A"
                interface = "Default (MGMT)"
                userid_dict["source"] = source
                userid_dict["type"] = type
                userid_dict["ip_address"] = ip_address
                userid_dict["port"] = port
                userid_dict["interface"] = interface
                userid_dict_list.append(dict(userid_dict))
        # Server Monitoring
        for agent in self.config_root.findall(
                ".//user-id-collector/server-monitor/entry"
        ):
            source = "Server Monitoring"
            if agent.find("./active-directory/host"):
                type = "Active Directory"
                ip_address = agent.find("./active-directory/host").text
                port = "N/A"
                interface = "Default (MGMT)"
                userid_dict["source"] = source
                userid_dict["type"] = type
                userid_dict["ip_address"] = ip_address
                userid_dict["port"] = port
                userid_dict["interface"] = interface
                userid_dict_list.append(dict(userid_dict))
        # TS Agent
        for agent in self.config_root.findall(".//ts-agent/entry"):
            source = "Terminal Service Agent"
            if agent.find("./ip-list/member"):
                type = "Terminal Service Agent"
                ip_address = agent.find("./ip-list/member").text
                port = agent.find("./port").text
                type = agent.find("./host").text
                interface = "Default (MGMT)"
                userid_dict["source"] = source
                userid_dict["type"] = type
                userid_dict["ip_address"] = ip_address
                userid_dict["port"] = port
                userid_dict["interface"] = interface
                userid_dict_list.append(dict(userid_dict))
        for agent in self.config_root.findall(".//user-id-agent/entry"):
            if agent.find("./disabled"):
                if agent.find("./disabled").text == "no":
                    type = "User-ID Agent"
                    source = ""
                    ip_address = agent.find("./host-port/host").text
                    port = agent.find("./host-port/port").text
                    for entry in self.config_root.findall(".//route/service/entry"):
                        if entry.attrib["name"] == "uid-agent":
                            interface = entry.find("./source/interface").text
                    if interface == "":
                        interface = "Default (MGMT)"
                    userid_dict["source"] = source
                    userid_dict["type"] = type
                    userid_dict["ip_address"] = ip_address
                    userid_dict["port"] = port
                    userid_dict["interface"] = interface
                    userid_dict_list.append(dict(userid_dict))

        logger.debug("End PanXMLHandler.get_userid()")
        return userid_dict_list

    def get_groups(self):
        """ """
        group_dict = {}
        group_dict_list = []
        for group_mapping in self.config_root.findall(".//group-mapping/entry"):
            profile = group_mapping.find("./server-profile")
            if profile:
                profile = profile.text
            domain = group_mapping.find("./domain")
            if domain:
                domain = domain.text
            group = group_mapping.find("./group-object/member")
            if group:
                group = group.text
            user = group_mapping.find("./user-object/member")
            if user:
                user = user.text
            uname = group_mapping.find("./user-name/member")
            gname = group_mapping.find("./group-name/member")
            attributes = ""
            if uname:
                attributes = uname.text + "\n"
            if gname:
                attributes = attributes + gname.text
            include_list = ""
            for il in group_mapping.findall("./group-include-list/member"):
                include_list = include_list + il.text + "\n"
            group_dict["profile"] = profile
            group_dict["domain"] = domain
            group_dict["group"] = group
            group_dict["user"] = user
            group_dict["attributes"] = attributes
            group_dict["include_list"] = include_list
            group_dict_list.append(dict(group_dict))
        return group_dict_list

    def get_snmpv2_manager(self):
        """ """
        global version, manager_ip, manager_name, manager_community
        snmpv2_dict = {}
        snmpv2_dict_list = []
        manager_ip = ""
        manager_name = ""
        manager_community = ""
        for snmpv2p in self.config_root.findall(
                ".//shared/log-settings/snmptrap/entry"
        ):
            profile_name = snmpv2p.attrib["name"]
            version = snmpv2p.find("./version/").tag
            manager_community = snmpv2p.find("./version//server/entry/community")
            if manager_community:
                manager_community = manager_community.text
            else:
                manager_community = ""
            manager_name = snmpv2p.find("./version//server/entry")
            if manager_name:
                manager_name = manager_name.attrib["name"]
            else:
                manager_name = ""
            manager_ip = snmpv2p.find("./version//server/entry/manager")
            if manager_ip:
                manager_ip = manager_ip.text
            else:
                manager_ip = ""
            snmpv2_dict["profile_name"] = profile_name
            snmpv2_dict["manager_ip"] = manager_ip
            snmpv2_dict["manager_name"] = manager_name
            snmpv2_dict["manager_community"] = manager_community
            snmpv2_dict_list.append(dict(snmpv2_dict))
        return snmpv2_dict_list

    def get_snmpv2_system(self):
        """ """
        snmpv2_dict = {}
        snmpv2_dict_list = []
        version = self.config_root.find(
            ".//system/snmp-setting/access-setting/version/"
        )
        if version:
            version = version.tag
        else:
            return snmpv2_dict_list
        if version == "v3":
            return snmpv2_dict_list
        snmpv2_dict["version"] = version
        location = self.config_root.find(".//system/snmp-setting/snmp-system/location")
        if location:
            location = location.text
        else:
            location = ""
        snmpv2_dict["location"] = location
        contact = self.config_root.find(".//system/snmp-setting/snmp-system/contact")
        if contact:
            contact = contact.text
        else:
            contact = ""
        snmpv2_dict["contact"] = contact
        community = self.config_root.find(
            ".//system/snmp-setting/access-setting/version/v2c/snmp-community-string"
        )
        if community:
            community = community.text
        else:
            community = "Public"
        snmpv2_dict["settings_community"] = community
        snmpv2_dict_list.append(dict(snmpv2_dict))
        return snmpv2_dict_list

    def get_gp_portals(self):
        """ """
        gpp_dict = {}
        gpp_dict_list = []

        for portal in self.config_root.findall(
                ".//global-protect/global-protect-portal/entry"
        ):
            interface = portal.find("./portal-config/local-address/interface")
            if interface:
                interface = interface.text
            address_ipv4 = portal.find("./portal-config/local-address/ip/ipv4")
            if address_ipv4:
                address_ipv4 = address_ipv4.text
            address_ipv6 = portal.find("./portal-config/local-address/ip/ipv6")
            if address_ipv6:
                address_ipv6 = address_ipv6.text
                address = address_ipv4 + "\n" + address_ipv6
            else:
                address = address_ipv4
            auth_profile = portal.find(
                "./portal-config/client-auth/entry/authentication-profile"
            )
            if auth_profile:
                auth_profile = auth_profile.text
            agent_profiles = ""
            os = portal.find("./client-config/configs//os")
            if os:
                for os in os.findall("./member"):
                    agent_profiles = agent_profiles + os.text + "\n"
            else:
                agent_profiles = "Any"
            gateways = ""
            for gateway in portal.findall(
                    "./client-config/configs//gateways/internal/list/entry"
            ):
                gateways = gateways + gateway.attrib["name"] + "\n"
            for gateway in portal.findall(
                    "./client-config/configs//gateways/external/list/entry"
            ):
                gateways = gateways + gateway.attrib["name"] + "\n"

            gpp_dict["interface"] = interface
            gpp_dict["auth_profile"] = auth_profile
            gpp_dict["address"] = address
            gpp_dict["agent_profiles"] = agent_profiles
            gpp_dict["gateways"] = gateways
        gpp_dict_list.append(dict(gpp_dict))
        return gpp_dict_list

    def get_gp_gateways(self):
        """ """
        gpg_dict = {}
        gpg_dict_list = []

        for gateway in self.config_root.findall(
                ".//global-protect/global-protect-gateway/entry"
        ):
            interface = ""
            dhcp_pool = ""
            address = ""
            gateway_name = gateway.attrib["name"]
            tunnel_mode = gateway.find("./tunnel-mode")
            if tunnel_mode:
                tunnel_mode = tunnel_mode.text

            if tunnel_mode == "yes":
                for gw in self.config_root.findall(
                        ".//tunnel/global-protect-gateway/entry"
                ):
                    if gateway_name + "-N" == gw.attrib["name"]:
                        address_ipv4 = gw.find(".//local-address/ip/ipv4")
                        if address_ipv4:
                            address_ipv4 = address_ipv4.text
                        address_ipv6 = gw.find(".//local-address/ip/ipv6")
                        if address_ipv6:
                            address_ipv6 = address_ipv6.text
                            address = str(address_ipv4) + "\n" + str(address_ipv6)
                        else:
                            address = address_ipv4
                        interface = gw.find(".//local-address/interface")
                        if interface:
                            interface = interface.text
                        for pool in gw.findall(".//ip-pool/member"):
                            dhcp_pool = dhcp_pool + pool.text + "\n"
            else:
                address_ipv4 = gateway.find(".//local-address/ip/ipv4")
                if address_ipv4:
                    address_ipv4 = address_ipv4.text
                address_ipv6 = gateway.find(".//local-address/ip/ipv6")
                if address_ipv6:
                    address_ipv6 = address_ipv6.text
                    address = str(address_ipv4) + "\n" + str(address_ipv6)
                else:
                    address = address_ipv4
                interface = gateway.find(".//local-address/interface")
                if interface:
                    interface = interface.text
                for pool in gateway.findall(".//ip-pool/member"):
                    dhcp_pool = dhcp_pool + pool.text + "\n"

            auth_profile = gateway.find(".//client-auth/entry/authentication-profile")
            if auth_profile:
                auth_profile = auth_profile.text
            agent_profiles = ""
            os = gateway.find("./remote-user-tunnel-configs/configs//os")
            if os:
                for os in os.findall("./member"):
                    agent_profiles = agent_profiles + os.text + "\n"
            else:
                agent_profiles = "Any"

            gpg_dict["interface"] = interface
            gpg_dict["auth_profile"] = auth_profile
            gpg_dict["address"] = address
            gpg_dict["agent_profiles"] = agent_profiles
            gpg_dict["dhcp_pool"] = dhcp_pool
            gpg_dict["tunnel_mode"] = tunnel_mode
            gpg_dict_list.append(dict(gpg_dict))
        return gpg_dict_list

    def get_logintsettings(self):
        """ """
        logintsettings = {}
        for interface in self.config_root.findall(
                ".//network/interface/ethernet//entry"
        ):
            logint = interface.find("./log-card")
            if logint:
                logcard = interface.attrib["name"]
                ip = logint.find("./ip-address")
                if ip:
                    ip = ip.text
                mask = logint.find("./netmask")
                if mask:
                    mask = mask.text
                gw = logint.find("./default-gateway")
                if gw:
                    gw = gw.text
                ipv6 = logint.find("./ipv6-address")
                if ipv6:
                    ipv6 = ipv6.text
                else:
                    ipv6 = "Not Used"
                speed = logint.find("./speed")
                if speed:
                    speed = speed.text
                else:
                    speed = "Auto"
                mtu = logint.find("./mtu")
                if mtu:
                    mtu = mtu.text
                else:
                    mtu = "Default"
                logintsettings["logcard"] = logcard
                logintsettings["ip"] = ip
                logintsettings["mask"] = mask
                logintsettings["gw"] = gw
                logintsettings["ipv6"] = ipv6
                logintsettings["speed"] = speed
                logintsettings["mtu"] = mtu
        return logintsettings

    def get_snmpv3(self):
        """ """
        snmpv3_dict = {}
        snmpv3_dict_list = []
        for view in self.config_root.findall(
                ".//system/snmp-setting/access-setting/version/v3/views/entry"
        ):
            snmpv3_dict["name"] = view.attrib["name"]
            for entry in view.findall("./view/entry"):
                snmpv3_dict["view"] = entry.attrib["name"]
                snmpv3_oid = entry.find("./oid")
                if snmpv3_oid is not None:
                    snmpv3_dict["oid"] = snmpv3_oid.text
                else:
                    snmpv3_dict["oid"] = "Not Configured"
                snmpv3_mask = entry.find("./mask")
                if snmpv3_mask is not None:
                    snmpv3_dict["mask"] = snmpv3_mask.text
                else:
                    snmpv3_dict["mask"] = "Not Configured"
                snmpv3_option = entry.find("./option")
                if snmpv3_option is not None:
                    snmpv3_dict["option"] = snmpv3_option.text
                else:
                    snmpv3_dict["option"] = "Not Configured"
        for user in self.config_root.findall(
                ".//system/snmp-setting/access-setting/version/v3/users/entry"
        ):
            snmpv3_dict["users"] = user.attrib["name"]
            for view in user.findall("./view"):
                snmpv3_dict["user_view"] = view.text
        if snmpv3_dict != {}:
            snmpv3_dict_list.append(dict(snmpv3_dict))
        return snmpv3_dict_list

    def get_logforwarding(self):
        """ """
        lf_dict = {}
        lf_dict_list = []

        for lfp in self.config_root.findall(
                ".//devices//vsys//log-settings/profiles//match-list/entry"
        ):
            snmp = ""
            syslog = ""
            email = ""
            lf_dict["profile_name"] = lfp.attrib["name"]
            lf_dict["log_type"] = lfp.find("./log-type").text
            lf_dict["panorama"] = lfp.find("./send-to-panorama").text
            if lfp.find("./send-snmptrap/member"):
                snmp = snmp + lfp.find("./send-snmptrap/member").text + "\n"
            if lfp.find("./send-syslog/member"):
                syslog = syslog + lfp.find("./send-syslog/member").text + "\n"
            if lfp.find("./send-email/member"):
                email = email + lfp.find("./send-email/member").text + "\n"
            lf_dict["snmp"] = snmp
            lf_dict["email"] = email
            lf_dict["syslog"] = syslog
            lf_dict_list.append(dict(lf_dict))
        return lf_dict_list

    def get_templates(self):
        """ """
        templates_dict = {}
        templates_dict_list = []

        for template in self.config_root.findall(".//devices/entry/template/entry"):
            if template.find("./id"):
                continue
            templates_dict["template_name"] = template.attrib["name"]
            templates_dict["stack_name"] = ""
            templates_dict["members"] = ""
            templates_dict_list.append(dict(templates_dict))

        templates_dict = {}
        for template_stack in self.config_root.findall(
                ".//devices/entry/template-stack/entry"
        ):
            if template_stack.find("./id"):
                continue
            members = ""
            templates_dict["template_name"] = ""
            templates_dict["stack_name"] = template_stack.attrib["name"]
            for template in template_stack.findall(".//templates/member"):
                members = members + template.text + "\n"
            templates_dict["members"] = members
            templates_dict_list.append(dict(templates_dict))
        return templates_dict_list

    def get_templates_for_prisma(self):
        global temp1, temp2
        temp1 = []
        temp2 = []
        prismatemplates_dict = {}
        templates_prisma_dict_list = []

        for template in self.config_root.findall(".//devices/entry/template/entry"):
            if template.find("./id"):
                continue
            # prismatemplates_dict["template_name"] = template.attrib["name"]
            # templates_dict_list.append(dict(prismatemplates_dict))
            temp1.append(template.attrib["name"])

        for template_stack in self.config_root.findall(
                ".//devices/entry/template-stack/entry"
        ):
            if template_stack.find("./id"):
                continue
            # prismatemplates_dict["stack_name"] = template_stack.attrib["name"]
            # templates_dict_list.append(dict(prismatemplates_dict))
            temp2.append(template_stack.attrib["name"])

        if len(temp1) == len(temp2):
            for i in range(len(temp1)):
                prismatemplates_dict["template_name"] = temp1[i]
                prismatemplates_dict["stack_name"] = temp2[i]
                templates_prisma_dict_list.append(dict(prismatemplates_dict))
        else:
            print("Error while matching template name and stack name")
        return templates_prisma_dict_list

    def get_devicegroups(self):

        """ """
        devicegroups_dict = {}
        devicegroups_dict_list = []
        devicegroups_dict["tier1"] = "Shared"
        devicegroups_dict["tier2"] = ""
        devicegroups_dict["tier3"] = ""
        devicegroups_dict["tier4"] = ""
        devicegroups_dict["master"] = ""
        devicegroups_dict_list.append(dict(devicegroups_dict))
        for devicegroup in self.config_root.findall(
                ".//readonly/devices/entry/device-group/entry"
        ):
            if devicegroup.find("./parent-dg") is None:
                devicegroups_dict = {}
                tier2 = devicegroup.attrib["name"]
                devicegroups_dict["tier1"] = ""
                devicegroups_dict["tier2"] = tier2
                devicegroups_dict["tier3"] = ""
                devicegroups_dict["tier4"] = ""
                for dg in self.config_root.findall(
                        ".//devices/entry/device-group/entry"
                ):
                    if dg.find("./id"):
                        continue
                    if tier2 == dg.attrib["name"]:
                        master = dg.find("./master-device/device")
                        if master:
                            master = master.text
                        else:
                            master = ""
                        devicegroups_dict["master"] = master
                devicegroups_dict_list.append(dict(devicegroups_dict))
                for devicegroup in self.config_root.findall(
                        ".//readonly/devices/entry/device-group/entry"
                ):
                    if (
                            devicegroup.find("./parent-dg")
                            and devicegroup.find("./parent-dg").text == tier2
                    ):
                        devicegroups_dict = {}
                        tier3 = devicegroup.attrib["name"]
                        devicegroups_dict["tier1"] = ""
                        devicegroups_dict["tier2"] = ""
                        devicegroups_dict["tier3"] = tier3
                        devicegroups_dict["tier4"] = ""
                        for dg in self.config_root.findall(
                                ".//devices/entry/device-group/entry"
                        ):
                            if dg.find("./id"):
                                continue
                            if tier3 == dg.attrib["name"]:
                                master = dg.find("./master-device/device")
                                if master:
                                    master = master.text
                                else:
                                    master = ""
                                devicegroups_dict["master"] = master
                        devicegroups_dict_list.append(dict(devicegroups_dict))
                        for devicegroup in self.config_root.findall(
                                ".//readonly/devices/entry/device-group/entry"
                        ):
                            if (
                                    devicegroup.find("./parent-dg")
                                    and devicegroup.find("./parent-dg").text == tier3
                            ):
                                devicegroups_dict = {}
                                tier4 = devicegroup.attrib["name"]
                                devicegroups_dict["tier1"] = ""
                                devicegroups_dict["tier2"] = ""
                                devicegroups_dict["tier3"] = ""
                                devicegroups_dict["tier4"] = tier4
                                for dg in self.config_root.findall(
                                        ".//devices/entry/device-group/entry"
                                ):
                                    if dg.find("./id"):
                                        continue
                                    if tier4 == dg.attrib["name"]:
                                        master = dg.find("./master-device/device")
                                        if master:
                                            master = master.text
                                        else:
                                            master = ""
                                        devicegroups_dict["master"] = master
                                devicegroups_dict_list.append(dict(devicegroups_dict))
        return devicegroups_dict_list

    def get_av(self):
        """Get Anti Virus info"""

        av_dict = {}
        av_dict_list = []
        for elem in self.config_root.findall(".//profiles/virus/entry"):
            av_decoders = ""
            av_actions = ""
            av_wf_actions = ""
            av_prof_name = elem.attrib["name"]
            for child in elem.findall(".//decoder/entry"):
                av_decoders = av_decoders + child.attrib["name"] + "\n"
                for grand_child in child:
                    if grand_child.tag == "action":
                        av_actions = av_actions + grand_child.text + "\n"
                    elif grand_child.tag == "wildfire-action":
                        av_wf_actions = av_wf_actions + grand_child.text + "\n"

            av_dict["av_profile_name"] = av_prof_name
            av_dict["av_decoders"] = av_decoders
            av_dict["av_actions"] = av_actions
            av_dict["av_wf_actions"] = av_wf_actions
            av_dict_list.append(dict(av_dict))
        return av_dict_list

    def get_ike_crypto(self):
        """Function to get ike crypto profile details"""

        ike_crypto_dict = {}
        ike_crypto_dict_list = []
        for elem in self.config_root.findall(
                ".//ike/crypto-profiles/ike-crypto-profiles/entry"
        ):
            dhgroup = ""
            authentication = ""
            encryption = ""
            v2multiple = elem.find("./authentication-multiple")
            ike_crypto_dict["ikeprofilename"] = elem.attrib["name"]
            for child in elem.findall("./dh-group/member"):
                dhgroup = dhgroup + child.text + " "
            for child in elem.findall("./hash/member"):
                authentication = authentication + child.text + " "
            for child in elem.findall("./encryption/member"):
                encryption = encryption + child.text + " "
            ike_crypto_dict["dhgroup"] = dhgroup
            ike_crypto_dict["authentication"] = authentication
            ike_crypto_dict["encryption"] = encryption
            if elem.find("./lifetime/") is not None:
                ike_crypto_dict["keylifetime"] = (
                        elem.find("./lifetime/").text + " " + elem.find("./lifetime/").tag
                )
            else:
                ike_crypto_dict["keylifetime"] = "Not Used"
            if v2multiple:
                v2multiple = v2multiple.text
            else:
                v2multiple = "0"
            ike_crypto_dict["v2authentication"] = v2multiple
            ike_crypto_dict_list.append(dict(ike_crypto_dict))
        return ike_crypto_dict_list

    def get_ipsec_crypto(self):
        """Function to get ipsec crypto profile details"""
        ipsec_crypto_dict = {}
        ipsec_crypto_dict_list = []
        for elem in self.config_root.findall(
                ".//ike/crypto-profiles/ipsec-crypto-profiles/entry"
        ):
            dhgroup = ""
            authentication = ""
            encryption = ""
            ipsec_crypto_dict["profilename"] = elem.attrib["name"]
            protocol = elem.find("./").tag
            ipsec_crypto_dict["protocol"] = protocol
            dhgroup = elem.find(".//dh-group").text
            for child in elem.findall(".//authentication/member"):
                authentication = authentication + child.text + " "
            if protocol == "esp":
                for child in elem.findall(".//encryption/member"):
                    encryption = encryption + child.text + " "
            ipsec_crypto_dict["dhgroup"] = dhgroup
            ipsec_crypto_dict["authentication"] = authentication
            ipsec_crypto_dict["encryption"] = encryption
            ipsec_crypto_dict["lifetime"] = (
                    elem.find("./lifetime/").text + " " + elem.find("./lifetime/").tag
            )
            if elem.find("./lifesize/"):
                ipsec_crypto_dict["lifesize"] = (
                        elem.find("./lifesize/").text + " " + elem.find("./lifesize/").tag
                )
            else:
                ipsec_crypto_dict["lifesize"] = "Not Used"
            ipsec_crypto_dict_list.append(dict(ipsec_crypto_dict))
        return ipsec_crypto_dict_list

    def get_ike_gw(self):
        """Function to get IKE gateway details"""

        ike_gw_dict = {}
        ike_gw_dict_list = []
        for elem in self.config_root.findall(".//ike/gateway/entry"):
            ike_gw_dict["ike_gw"] = elem.attrib["name"]
            authentication = elem.find("./authentication/").tag
            ike_gw_dict["authentication"] = authentication
            # protocol = ""
            for child in elem.findall("./protocol/"):
                if child.tag == "version":
                    ikeversion = elem.find("./protocol/version").text
                else:
                    ikeversion = "ikev1"
            ike_gw_dict["ike_version"] = ikeversion
            local_interface = elem.find(".//local-address/interface")
            if local_interface is not None:
                ike_gw_dict["address_type"] = local_interface.tag
                ike_gw_dict["interface"] = local_interface.text
            else:
                ike_gw_dict["address_type"] = ""
            local_ip = elem.find(".//local-address/ip")
            if local_ip is not None:
                ike_gw_dict["local_address"] = local_ip.text
            else:
                ike_gw_dict["local_address"] = ""
            peer_address = elem.find("./peer-address/")
            if peer_address is not None:
                ike_gw_dict["peer_address_type"] = peer_address.tag
                ike_gw_dict["peer_address"] = peer_address.text
            else:
                ike_gw_dict["peer_address_type"] = ""
                ike_gw_dict["peer_address"] = ""
            peer_id = elem.find("./peer-id/id")
            if peer_id is not None:
                ike_gw_dict["peer_id"] = peer_id.text
            else:
                ike_gw_dict["peer_id"] = ""
            local_id = elem.find("./local-id/id")
            if local_id is not None:
                ike_gw_dict["local_id"] = local_id.text
            else:
                ike_gw_dict["local_id"] = ""
            ike_crypto = elem.find(".//protocol//ike-crypto-profile")
            if ike_crypto is None:
                ike_gw_dict["crypto_profile"] = "default"
            else:
                ike_gw_dict["crypto_profile"] = ike_crypto.text
            ike_gw_dict_list.append(dict(ike_gw_dict))
        return ike_gw_dict_list

    def get_ipsec_vpn(self):
        """Function to get IPSEC VPN details"""
        ipsec_vpn_dict = {}
        ipsec_vpn_dict_list = []
        for elem in self.config_root.findall(".//tunnel/ipsec/entry"):
            proxy_id = ""
            ipsec_vpn_dict["tunnel_name"] = elem.attrib["name"]
            ipsec_vpn_dict["type"] = elem.find("./").tag
            ipsec_vpn_dict["ike_gw"] = elem.find(".//ike-gateway/entry").attrib["name"]
            if elem.find(".//ipsec-crypto-profile") is not None:
                ipsec_vpn_dict["ipsec_crypto"] = elem.find(
                    ".//ipsec-crypto-profile"
                ).text
            else:
                ipsec_vpn_dict["ipsec_crypto"] = "default"
            ipsec_vpn_dict["tunnel_interface"] = elem.find(".//tunnel-interface").text
            if elem.find(".//tunnel-monitor/enable") is not None:
                ipsec_vpn_dict["options"] = (
                        "Tunnel Monitoring Enabled = "
                        + elem.find(".//tunnel-monitor/enable").text
                )
            else:
                ipsec_vpn_dict["options"] = "Tunnel Monitoring Not Enabled"
            for child in elem.findall(".//proxy-id//entry"):
                proxy_id_local = ""
                proxy_id_remote = ""
                if child.find("./").tag == "local" or "remote":
                    proxy_id_local = child.find(".//local")
                    proxy_id_local = (
                        proxy_id_local.text
                        if proxy_id_local is not None
                        else "Not Configured"
                    )
                    proxy_id_remote = child.find(".//remote")
                    proxy_id_remote = (
                        proxy_id_remote.text
                        if proxy_id_remote is not None
                        else "Not Configured"
                    )
                    proxy_id = (
                            proxy_id
                            + child.attrib["name"]
                            + " (Local: "
                            + proxy_id_local
                            + ", Remote: "
                            + proxy_id_remote
                            + ")\n"
                    )
            ipsec_vpn_dict["proxy_id"] = proxy_id
            ip_type = elem.find(".//ipv6")
            if ip_type:
                ip_type = ip_type.text
            if ip_type or ip_type != "yes":
                ip_type = "IPv4"
            else:
                ip_type = "IPv6"
            ipsec_vpn_dict["address_type"] = ip_type
            ipsec_vpn_dict_list.append(dict(ipsec_vpn_dict))
        return ipsec_vpn_dict_list

    def get_dos(self):
        """Get DoS profile Info"""

        dos_dict = {}
        dos_dict_list = []
        for elem in self.config_root.findall(".//profiles/dos-protection/entry"):
            dos_dict["dos_rule_name"] = elem.attrib["name"]
            dos_dict["dos_type"] = elem.find("./type").text
            dos_dict["dos_syn"] = elem.find("./flood/tcp-syn/enable").text
            dos_dict["dos_udp"] = elem.find("./flood/udp/enable").text
            dos_dict["dos_icmp"] = elem.find("./flood/icmp/enable").text
            dos_dict["dos_icmp6"] = elem.find("./flood/icmpv6/enable").text
            dos_dict["dos_flood"] = elem.find("./flood/other-ip/enable").text
            dos_dict["dos_rps"] = elem.find("./resource/sessions/enabled").text
            dos_dict_list.append(dict(dos_dict))
        return dos_dict_list

    def get_vsys_vr(self):
        """Get VSYS Info. VSYS ID != part of Config and VSYS_name is
        not part of running output. Hence, not getting VSYS ID, except
        when multivsys is off and hence VSYS ID is 1."""
        vsys_dict = {}
        vsys_dict_list = []
        for vsys in self.config_root.findall(".//vsys/entry"):
            interfaces = ""
            protocols = ""
            vrs = ""
            vri = ""
            vsys_dict["vsys_name"] = vsys.attrib["name"]
            if not vsys.findall("./import/network/virtual-router/member"):
                for vr2 in self.config_root.findall(".//network/virtual-router/entry"):
                    bgp = ""
                    ospf = ""
                    ospf3 = ""
                    rip = ""
                    vri = vri + vr2.attrib["name"]
                    for interface in vr2.findall("./interface/member"):
                        interfaces = interfaces + interface.text + "\n"
                        vri = vri + "\n"
                    interfaces = interfaces + "\n"
                    vri = vri + "\n"
                    vrs = vrs + vr2.attrib["name"] + "\n"
                    bgp = vr2.find("./protocol/bgp/enable")
                    static = "Static"
                    if bgp:
                        bgp = "\nBGP: " + bgp.text
                    else:
                        bgp = "\nBGP: no"
                    vrs = vrs + "\n"
                    ospf = vr2.find("./protocol/ospf/enable")
                    if ospf:
                        ospf = "\nOSPF: " + ospf.text
                    else:
                        ospf = "\nOSPF: no"
                    vrs = vrs + "\n"
                    ospf3 = vr2.find("./protocol/ospf/enable")
                    if ospf3:
                        ospf3 = "\nOSPF3: " + ospf3.text
                    else:
                        ospf3 = "\nOSPF3: no"
                    vrs = vrs + "\n"
                    rip = vr2.find("./protocol/rip/enable")
                    if rip:
                        rip = "\nRIP: " + rip.text + "\n\n"
                    else:
                        rip = "\nRIP: no" + "\n\n"
                    vrs = vrs + "\n\n"
                    protocols = protocols + static + bgp + ospf + ospf3 + rip
            else:
                for vr1 in vsys.findall("./import/network/virtual-router/member"):
                    for vr2 in self.config_root.findall(
                            ".//network/virtual-router/entry"
                    ):
                        bgp = ""
                        ospf = ""
                        ospf3 = ""
                        rip = ""
                        if vr1.text == vr2.attrib["name"]:
                            vri = vri + vr1.text
                            for interface in vr2.findall("./interface/member"):
                                interfaces = interfaces + interface.text + "\n"
                                vri = vri + "\n"
                            interfaces = interfaces + "\n"
                            vri = vri + "\n"

                            vrs = vrs + vr1.text + "\n"
                            bgp = vr2.find("./protocol/bgp/enable")
                            static = "Static"
                            if bgp:
                                bgp = "\nBGP: " + bgp.text
                            else:
                                bgp = "\nBGP: no"
                            vrs = vrs + "\n"
                            ospf = vr2.find("./protocol/ospf/enable")
                            if ospf:
                                ospf = "\nOSPF: " + ospf.text
                            else:
                                ospf = "\nOSPF: no"
                            vrs = vrs + "\n"
                            ospf3 = vr2.find("./protocol/ospf/enable")
                            if ospf3:
                                ospf3 = "\nOSPF3: " + ospf3.text
                            else:
                                ospf3 = "\nOSPF3: no"
                            vrs = vrs + "\n"
                            rip = vr2.find("./protocol/rip/enable")
                            if rip:
                                rip = "\nRIP: " + rip.text + "\n\n"
                            else:
                                rip = "\nRIP: no" + "\n\n"
                            vrs = vrs + "\n\n"
                            protocols = protocols + static + bgp + ospf + ospf3 + rip

            vsys_dict["interfaces"] = interfaces
            vsys_dict["vr_name_p"] = vrs
            vsys_dict["vr_name_i"] = vri
            vsys_dict["protocols"] = protocols
            vsys_dict_list.append(dict(vsys_dict))
        return vsys_dict_list

    def get_zones(self):
        """Get Zone info."""
        zones_dict = {}
        zones_dict_list = []
        for vsys in self.config_root.findall(".//vsys/entry"):
            for zone in vsys.findall("./zone/entry"):
                zones_dict["vsys_name"] = vsys.attrib["name"]
                zones_dict["zone_name"] = zone.attrib["name"]
                if zone.find("./network/"):
                    zones_dict["zone_type"] = zone.find("./network/").tag
                else:
                    zones_dict["zone_type"] = "None"
                zone_protection = zone.find(".//network/zone-protection-profile")
                user_id = zone.find(".//enable-user-identification")
                if zone_protection:
                    zone_protection = zone_protection.text
                else:
                    zone_protection = "No"
                if user_id:
                    user_id = user_id.text
                else:
                    user_id = "No"
                zones_dict["user_id"] = user_id
                zones_dict["zone_protection"] = zone_protection
                zones_dict_list.append(dict(zones_dict))
        return zones_dict_list

    def get_admins(self):
        """Get Admin info."""
        logger.debug("Starting get_admins()")
        admins_dict = {}
        admins_dict_list = []
        for admin in self.config_root.findall(".//mgt-config/users/entry"):
            admin_name = admin.attrib["name"]
            logger.debug("Found admin name: %s", admin_name)
            auth_profile = admin.find("./authentication-profile")
            if auth_profile:
                auth_profile = auth_profile.text
            else:
                auth_profile = ""

            my_pass_profile = admin.find("./password-profile")
            if my_pass_profile:
                my_pass_profile = my_pass_profile.text
            else:
                my_pass_profile = ""  # False Positive [B105:hardcoded_password_string] Possible hardcoded password: ''

            admin_role = admin.find("./permissions/role-based/")
            if admin_role:
                role_profile = admin_role.find("./profile")
                access_domain = admin_role.find("./dg-template-profiles/entry")
                admin_role = admin_role.tag
                if access_domain:
                    role_profile = access_domain.find("./profile")
                    access_domain = access_domain.attrib["name"]
                if role_profile:
                    role_profile = role_profile.text
                else:
                    role_profile = ""
            else:
                admin_role = ""
                role_profile = ""
                access_domain = ""

            admins_dict["admin_name"] = admin_name
            admins_dict["admin_role"] = admin_role
            admins_dict["role_profile"] = role_profile
            admins_dict["auth_profile"] = auth_profile
            admins_dict["pass_profile"] = my_pass_profile
            admins_dict["access_domain"] = access_domain
            admins_dict_list.append(dict(admins_dict))
        return admins_dict_list

    def get_dfo(self):
        """Get Data Filtering Objects Info."""

        dfo_dict = {}
        dfo_dict_list = []
        for elem in self.config_root.findall(".//profiles/data-objects/entry"):
            profile_name = elem.attrib["name"]
            pattern_type = ""
            dfo_name = ""
            file_types = ""
            pattern = ""
            pattern_type = elem.find("./pattern-type/").tag
            find1 = "./pattern-type/" + str(pattern_type) + "/pattern/entry"
            find2 = "./file-type/member"
            find3 = "./regex"
            for child in elem.findall(find1):
                dfo_name = dfo_name + child.attrib["name"]
                for grand_child in child.findall(find2):
                    file_types = file_types + grand_child.text + "\n"
                    dfo_name = dfo_name + "\n"
                for grand_child in child.findall(find3):
                    pattern = pattern + grand_child.text + "\n"
            dfo_dict["profile_name"] = profile_name
            dfo_dict["pattern_type"] = pattern_type
            dfo_dict["dfo_name"] = dfo_name
            dfo_dict["file_types"] = file_types
            dfo_dict["pattern"] = pattern
            dfo_dict_list.append(dict(dfo_dict))
        return dfo_dict_list

    def get_as(self):
        """Get Anti-Spyware Info."""

        as_dict = {}
        as_dict_list = []
        for elem in self.config_root.findall(".//profiles/spyware/entry"):
            as_prof_name = elem.attrib["name"]
            as_severity = ""
            as_action = ""
            as_dns_sinkhole = ""
            for child in elem.findall(".//rules/entry"):
                for grand_child in child.findall(".//severity//member"):
                    as_severity = as_severity + grand_child.text + " "
                as_severity = as_severity + "\n"
                as_action = as_action + child.find(".//action//").tag + "\n"
            as_dns_sinkhole = elem.find(".//botnet-domains//lists//entry")
            if as_dns_sinkhole:
                as_dns_sinkhole = (
                        "Server: "
                        + as_dns_sinkhole.attrib["name"]
                        + "\n Action: "
                        + elem.find(".//botnet-domains//lists//entry//action//").tag
                )
            as_dict["as_profile_name"] = as_prof_name
            as_dict["as_severity"] = as_severity
            as_dict["as_actions"] = as_action
            as_dict["as_dnssink"] = as_dns_sinkhole
            as_dict_list.append(dict(as_dict))
        return as_dict_list

    def get_vp(self):
        """Get Vulnerability Protection Info."""

        vp_dict = {}
        vp_dict_list = []
        for elem in self.config_root.findall(".//profiles/vulnerability/entry"):
            vp_prof_name = elem.attrib["name"]
            vp_severity = ""
            vp_action = ""
            vp_rules = ""
            for child in elem.findall(".//rules/entry"):
                vp_rules = vp_rules + child.attrib["name"] + "\n"
                for grand_child in child.findall(".//severity//member"):
                    vp_severity = vp_severity + grand_child.text + " "
                vp_severity = vp_severity + "\n"
                vp_action = vp_action + child.find(".//action//").tag + "\n"
            vp_dict["vp_profile_name"] = vp_prof_name
            vp_dict["vp_severity"] = vp_severity
            vp_dict["vp_actions"] = vp_action
            vp_dict["vp_rules"] = vp_rules
            vp_dict_list.append(dict(vp_dict))
        return vp_dict_list

    def get_url(self):
        """Get URL filtering Info."""

        url_dict = {}
        url_dict_list = []
        for elem in self.config_root.findall(".//profiles/url-filtering/entry"):
            block = ""
            alert = ""
            allow = ""
            continu = ""
            override = ""
            credential = ""
            url_prof_name = elem.attrib["name"]
            for child in elem.findall("./alert/member"):
                alert = alert + child.text + "\n"
            for child in elem.findall("./allow/member"):
                allow = allow + child.text + "\n"
            for child in elem.findall("./block/member"):
                block = block + child.text + "\n"
            for child in elem.findall("./continue/member"):
                continu = continu + child.text + "\n"
            for child in elem.findall("./override/member"):
                override = override + child.text + "\n"

            for child in elem.findall("./credential-enforcement/mode/"):
                credential = child.tag

            if allow == "":
                allow = "All Other Categories"

            url_dict["url_prof_name"] = url_prof_name
            url_dict["alert"] = alert
            url_dict["allow"] = allow
            url_dict["block"] = block
            url_dict["continue"] = continu
            url_dict["credential"] = credential
            url_dict["override"] = override
            url_dict_list.append(dict(url_dict))
        return url_dict_list

    def get_wf(self):
        """Get Wildfire Info."""

        wf_dict = {}
        wf_dict_list = []
        for elem in self.config_root.findall(".//profiles/wildfire-analysis/entry"):
            wf_dict["wf_prof_name"] = elem.attrib["name"]
            for entry in elem.findall("./rules/entry"):
                filetype = ""
                applications = ""
                analysis = elem.find("./rules/entry/analysis").text
                direction = elem.find("./rules/entry/direction").text
                for child in elem.findall("./rules/entry/file-type/member"):
                    filetype = filetype + child.text + "\n"
                for child in elem.findall("./rules/entry/application/member"):
                    applications = applications + child.text + "\n"

                wf_dict["wf_filetypes"] = filetype
                wf_dict["wf_applications"] = applications
                wf_dict["wf_direction"] = direction
                wf_dict["wf_analysis"] = analysis
                wf_dict_list.append(dict(wf_dict))
        return wf_dict_list

    def get_fb(self):
        """Get File Blocking Info."""

        fb_dict = {}
        fb_dict_list = []
        for elem in self.config_root.findall(
                ".//profiles//file-blocking//entry//rules/entry"
        ):
            fb_rule_name = elem.attrib["name"]
            filetype = ""
            applications = ""
            action = elem.find("./action").text
            direction = elem.find("./direction").text
            for child in elem.findall("./file-type/member"):
                filetype = filetype + child.text + "\n"
            for child in elem.findall("./application/member"):
                applications = applications + child.text + "\n"

            fb_dict["fb_rule_name"] = fb_rule_name
            fb_dict["fb_filetypes"] = filetype
            fb_dict["fb_applications"] = applications
            fb_dict["fb_direction"] = direction
            fb_dict["fb_action"] = action
            fb_dict_list.append(dict(fb_dict))
        return fb_dict_list

    def get_hip(self):
        """Get File Blocking Info."""
        hip_dict = {}
        hip_dict_list = []
        for elem in self.config_root.findall(".//profiles//hip-profiles/entry"):
            name = elem.attrib["name"]
            parameters = elem.find("./match")
            if parameters:
                parameters = parameters.text
            hip_dict["name"] = name
            hip_dict["parameters"] = parameters
            hip_dict_list.append(dict(hip_dict))
        return hip_dict_list

    def get_interfaces(self):
        """Get interfaces Info.

        interfaces ID != part of Config and interfaces_name is
        not part of running output. Hence, not getting interfaces ID, except
        when multiinterfaces is off and hence interfaces ID is 1.
        """
        interfaces_dict = {}
        interfaces_dict_list = []
        ae_eth = self.config_root.findall(
            ".//network/interface/aggregate-ethernet/entry"
        )
        eth = self.config_root.findall(".//network/interface/ethernet/entry")
        interfaces = []
        for interface in ae_eth:
            interfaces.append(interface)
        for interface in eth:
            interfaces.append(interface)

        for elem in interfaces:
            type = elem.findall("./")
            if type:
                for int_type in type:
                    if (
                            int_type.tag == "comment"
                            or int_type.tag == "link-state"
                            or int_type.tag == "link-speed"
                            or int_type.tag == "link-duplex"
                    ):
                        continue
                    else:
                        interface_type = int_type.tag
            else:
                continue
            if (
                    interface_type == "ha"
                    or interface_type == "log-card"
                    or interface_type == "aggregate-group"
            ):
                continue
            interface = elem.attrib["name"]

            mgtprof = elem.find(".//interface-management-profile")
            if mgtprof:
                mgtprof = mgtprof.text

            ip = ""
            for child in elem.findall(".//ip/entry"):
                ip = ip + child.attrib["name"] + "\n"
            child = elem.find(".//dhcp-client")
            if child:
                ip = "DHCP Client\n"

            for vsys in self.config_root.findall(".//vsys/entry"):
                for this_interface in vsys.findall("./import/network/interface/member"):
                    if this_interface.text == interface:
                        interfaces_dict["vsys_name"] = vsys.attrib["name"]

            vr_name = ""
            for vr in self.config_root.findall(".//network/virtual-router/entry"):
                for this_interface in vr.findall("./interface/member"):
                    if this_interface.text == interface:
                        vr_name = vr.attrib["name"]

            interfaces_dict["zone"] = ""
            for zone in self.config_root.findall(".//vsys/entry/zone/entry"):
                for this_interface in zone.findall(".//member"):
                    if this_interface.text == interface:
                        interfaces_dict["zone"] = zone.attrib["name"]

            interfaces_dict["vlan"] = ""

            for vlan in self.config_root.findall(".//network/vlan/entry"):
                for this_interface in vlan.findall(".//interface/member"):
                    if this_interface.text == interface:
                        interfaces_dict["vlan"] = vlan.attrib["name"]

            interfaces_dict["vr_name"] = vr_name
            interfaces_dict["interface"] = interface
            interfaces_dict["type"] = interface_type
            interfaces_dict["mgtprof"] = mgtprof
            interfaces_dict["ip"] = ip
            interfaces_dict_list.append(dict(interfaces_dict))
        return interfaces_dict_list

    def get_df(self):
        """Get Data Filtering Info."""

        df_dict = {}
        df_dict_list = []
        for elem in self.config_root.findall(
                ".//profiles//data-filtering//entry//rules/entry"
        ):
            df_rule_name = elem.attrib["name"]
            filetype = ""
            applications = ""
            alert = elem.find("./alert-threshold").text
            block = elem.find("./block-threshold").text
            pattern = elem.find("./data-object").text
            direction = elem.find("./direction").text
            for child in elem.findall("./file-type/member"):
                filetype = filetype + child.text + "\n"
            for child in elem.findall("./application/member"):
                applications = applications + child.text + "\n"

            df_dict["df_rule_name"] = df_rule_name
            df_dict["df_filetypes"] = filetype
            df_dict["df_applications"] = applications
            df_dict["df_direction"] = direction
            df_dict["df_alert"] = alert
            df_dict["df_block"] = block
            df_dict["df_patterns"] = pattern
            df_dict_list.append(dict(df_dict))
        return df_dict_list

    def get_mgmtinfo(self, model):
        """Get management Interface Info from Panorama and Firewalls."""
        logger.debug("Starting get_mgmtinfo() for model: %s", model)
        mgmtinfo_dict = {}

        if model != "Panorama":
            system_type = self.config_root.find(".//system/type/")
            if system_type:
                system_type = system_type.tag
            else:
                system_type = "static"
        else:
            system_type = "static"

        ip = self.config_root.find(".//system/ip-address")

        if ip is not None:
            ip = ip.text
        else:
            ip = "Not Configured"

        mask = self.config_root.find(".//system/netmask")

        if mask is not None:
            mask = mask.text
        else:
            ip = "Not Configured"

        gw = self.config_root.find(".//system/default-gateway")

        if gw is not None:
            gw = gw.text
        else:
            ip = "Not Configured"

        ipv6 = self.config_root.find(".//system/ipv6-address")

        if ipv6 is not None:
            ipv6 = ipv6.text
        else:
            ipv6 = "Not Used"

        speed = self.config_root.find(".//system/speed-duplex")

        if speed is None:
            speed = "Default"
        else:
            speed = speed.text

        mtu = self.config_root.find(".//system/mtu")

        if mtu is None:
            mtu = "Default"
        else:
            mtu = mtu.text

        services = ""
        services_list = self.config_root.findall(".//system/service/")
        for service in services_list:
            if service.tag == "disable-http" and service.text == "no":
                services = services + " HTTP"
            elif service.tag == "disable-telnet" and service.text == "no":
                services = services + " Telnet"
            elif service.tag == "disable-icmp" and service.text == "no":
                services = services + " ICMP"
            elif service.tag == "disable-ssh" and service.text == "no":
                services = services + " SSH"
            elif service.tag == "disable-https" and service.text == "no":
                services = services + " HTTPS"
        if self.config_root.find(".//system/service/disable-https") is None:
            services = services + " HTTPS"
        if self.config_root.find(".//system/service/disable-ssh") is None:
            services = services + " SSH"
        if self.config_root.find(".//system/service/disable-icmp") is None:
            services = services + " ICMP"

        permitted_ips = ""
        for ipadd in self.config_root.findall(".//system/permitted-ip/entry"):
            if ipadd:
                permitted_ips = permitted_ips + ipadd.attrib["name"] + "\n"

        if system_type == "dhcp-client":
            ip = "Assigned by DHCP"

        if permitted_ips == "":
            permitted_ips = "Not Configured"

        mgmtinfo_dict["ip"] = ip
        mgmtinfo_dict["mask"] = mask
        mgmtinfo_dict["gw"] = gw
        mgmtinfo_dict["ipv6"] = ipv6
        mgmtinfo_dict["speed"] = speed
        mgmtinfo_dict["mtu"] = mtu
        mgmtinfo_dict["services"] = services
        mgmtinfo_dict["permitted_ips"] = permitted_ips

        for key, value in mgmtinfo_dict.items():
            logger.info("Processing device: %s:%s", key, value)

        return mgmtinfo_dict

    def get_update_sched(self):
        """Get Dynamic Update Schedule."""

        update_sched_dict = {}
        update_sched_list = []
        for elem in self.config_root.findall(".//system//update-schedule/"):
            update_type = ""
            recurrence = ""
            time = ""
            action = ""
            threshold = ""

            update_type = elem.tag
            recurrence = elem.find(".//recurring/")
            if recurrence:
                if recurrence.tag != "sync-to-peer":
                    recurrence = recurrence.tag
            time = elem.find(".//at")
            if time:
                time = time.text
            action = elem.find(".//action")
            if action:
                action = action.text
            threshold = elem.find(".//threshold")
            if threshold:
                threshold = elem.find(".//threshold").text
            update_sched_dict["type"] = update_type
            update_sched_dict["recurrence"] = recurrence
            update_sched_dict["time"] = time
            update_sched_dict["action"] = action
            update_sched_dict["threshold"] = threshold
            update_sched_list.append(dict(update_sched_dict))
        return update_sched_list

    def get_secprof(self):
        """Get Security Profile Groups Info."""

        secprof_dict = {}
        secprof_dict_list = []
        for elem in self.config_root.findall(".//profile-group//entry"):
            group_name = elem.attrib["name"]
            av = elem.find("./virus/member")
            if av:
                av = av.text
            a_s = elem.find("./spyware/member")
            if a_s:
                a_s = a_s.text
            vp = elem.find("./vulnerability/member")
            if vp:
                vp = vp.text
            fb = elem.find("./file-blocking/member")
            if fb:
                fb = fb.text
            wf = elem.find("./wildfire-analysis/member")
            if wf:
                wf = wf.text
            df = elem.find("./data-filtering/member")
            if df:
                df = df.text
            url = elem.find("./url-filtering/member")
            if url:
                url = url.text

            secprof_dict["group_name"] = group_name
            secprof_dict["av"] = av
            secprof_dict["as"] = a_s
            secprof_dict["vp"] = vp
            secprof_dict["fb"] = fb
            secprof_dict["wf"] = wf
            secprof_dict["df"] = df
            secprof_dict["url"] = url
            secprof_dict_list.append(dict(secprof_dict))
        return secprof_dict_list
