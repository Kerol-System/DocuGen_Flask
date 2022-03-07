from tsf_handler import PanTSFHandler


class PrismaAccess(PanTSFHandler):
    """Subclass for a Panorama device with Prisma Access"""
    def __init__(self, tsf_info):
        super().__init__("/Users/satwiksatat/Downloads/","/Users/satwiksatat/Downloads/", "/")
        self.tsf_info = tsf_info
        self.csp = self.get_csp_info()
        self.multi_tenancy = False
        self.plugin_version = self.csp['version']
        self.prisma_templates = self.csp['prisma-templates']
        self.prisma_dg = self.csp['prisma-dg']
        self.service_setup = self.csp['service-setup']  # Break out to parse further
        self.mobile_gp = self.csp['mobile-users']  # Break out to parse further
        self.mobile_explicit_proxy = self.csp['mobile-users-explicit-proxy']  # Break out to parse further
        self.remote_networks = self.csp['remote-networks']  # Break out to parse further
        self.service_connection = self.csp['service-connection']  # Break out to parse further
        self.traffic_steering = self.csp['traffic-steering']

    def get_csp_info(self) -> dict:
        """Retrieves the contents of the cloud-services plugin from the
        config XML file for further further processing

        NOTE: csp_all is the entirety of //plugin/cloud-services in an
        ordered dictionary. To extend csp_info, simply add a statement to
        parse a different area of csp_all. Further processing of this info
        is done in other functions

        Returns:
            dict: Contents of  //plugin/cloud-services from the config XML
            as a dictionary
        """
        csp_all = (
                self.tsf_info
                ['running']['config']['devices']['entry']
                ['plugins'].get('cloud_services'))
        csp_info = dict()
        if csp_all is not None:  # In case a device is mis-typed
            csp_info['version'] = str(csp_all.get('@version'))
            csp_info['service-setup'] = csp_all.get('service-connection')
            if 'service-connection' in csp_all:
                csp_info['service-connection'] = (
                    csp_all['service-connection'].get('onboarding'))
                csp_info['prisma-dg'] = (
                    csp_all['service-connection'].get('template-stack'))
                csp_info['prisma-templates'] = (
                    csp_all['service-connection'].get('device-group'))
            else:
                csp_info['service-connection'] = None
                csp_info['prisma-dg'] = None
                csp_info['prisma-templates'] = None
            csp_info['mobile-users-explicit-proxy'] = (
                csp_all.get('mobile-users-explicit-proxy'))
            csp_info['mobile-users'] = csp_all.get('mobile-users')
            csp_info['remote-networks'] = csp_all.get('remote-networks')
            csp_info['traffic-steering'] = list()
            if 'traffic-steering' in csp_all:
                for e in csp_all.get('traffic-steering'):
                    csp_info['traffic-steering'].append(e)
        print(csp_all)
        return csp_info
    
    
