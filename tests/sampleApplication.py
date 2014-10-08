'''
Created on Oct 2, 2014

@author: preethib
'''
from jnpr.openclos.l3Clos import L3ClosMediation
from jnpr.openclos.ztp import ZtpServer
from jnpr.openclos.rest import RestServer
import jnpr.openclos.util
import os

installedDhcpConf = "/etc/dhcp/dhcpd.conf"

# OpenClos generated dhcpd.conf file path. It is usally located at 
# <OpenClos install dir>/jnpr/openclos/out/<pod name>/dhcpd.conf
generatedDhcpConf= "/home/regress/OpenClos-R1.0.dev1/jnpr/openclos/out/anotherPod/dhcpd.conf"


class sampleApplication:
    '''
    Sample Application for creating Layer-3 IP Fabric
    '''
    def createConfigFilesForDevices(self):
        '''
         create configuration for each leaf and spine in IP Fabric
         
        '''
        l3ClosMediation = L3ClosMediation()
        pods = l3ClosMediation.loadClosDefinition()
        l3ClosMediation.processFabric('anotherPod', pods['anotherPod'], reCreateFabric = True)

    def setupZTP(self):
        '''
        setup Zero Touch Provisioning
        generate DHCP config file and restart DHCP server with new dhcp configuration
        installs DHCP server
        '''
        ztpServer = ZtpServer()
        ztpServer.createPodSpecificDhcpConfFile('anotherPod')

        if jnpr.openclos.util.isPlatformUbuntu():
            os.system('sudo apt-get -y install isc-dhcp-server')
            os.system('sudo cp ' + generatedDhcpConf + ' ' + installedDhcpConf)
            os.system("/etc/init.d/isc-dhcp-server restart")

        elif jnpr.openclos.util.isPlatformCentos():
            os.system('yum -y install dhcp')
            os.system('sudo cp ' + generatedDhcpConf + ' ' + installedDhcpConf)
            os.system("/etc/rc.d/init.d/dhcpd restart")

    def startHTTPserverForZTPFileTransferProtocol(self):
        '''
        start HTTP server to serve as filetransfer mechanism for ZTP/DHCP process
        run HTTP server on port 80
        '''
        restServer = RestServer()
        restServer.initRest()
        restServer.start()

if __name__ == '__main__':
    app = sampleApplication()
    app.createConfigFilesForDevices()
    app.setupZTP()
    app.startHTTPserverForZTPFileTransferProtocol()
