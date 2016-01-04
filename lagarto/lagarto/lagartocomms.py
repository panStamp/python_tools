#########################################################################
#
# Copyright (c) 2012 Daniel Berenguer <dberenguer@usapiens.com>
#
# This file is part of the lagarto project.
#
# lagarto  is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# lagarto is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with panLoader; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA
#
#########################################################################
__author__="Daniel Berenguer"
__date__  ="$Jan 26, 2012$"
#########################################################################

from lagartoconfig import XmlLagarto
from lagartohttp import LagartoHttpServer
from lagartomqtt import LagartoMqttClient
from lagartoresources import LagartoException, LagartoMessage

import httplib
import threading
import json
import socket
import os
import time


class LagartoProcess(object):
    """
    Geenric Lagarto process class
    """
    def get_status(self, endpoints):
        """
        Return network status as a list of endpoints in JSON format
        Method to be overriden by subclass
        
        @param endpoints: list of endpoints being queried
        
        @return list of endpoints in JSON format
        """
        print "get_status needs to be overriden"
        return None


    def set_status(self, endpoints):
        """
        Set endpoint status
        Method to be overriden by subclass
        
        @param endpoints: list of endpoints in JSON format
        
        @return list of endpoints being controlled, with new values
        """
        print "set_status needs to be overriden"
        return None


    def http_command_received(self, command, params):
        """
        Process command sent from HTTP server. Method to be overrided by data server.
        Method to be overriden by subclass
        
        @param command: command string
        @param params: dictionary of parameters
        
        @return True if command successfukky processed by server.
        Return False otherwise
        """
        print "http_command_received needs to be overriden"
        return False
    

    def _get_local_ip_address(self):
        """
        Get local IP address
        
        @return local IP address
        """
        ipaddr = socket.gethostbyname(socket.gethostname())
        if ipaddr.startswith("127.0"):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("1.1.1.1", 8000))
                ipaddr = s.getsockname()[0]
                s.close()
            except:
                pass
 
        return ipaddr


    def publish_status(self, status_data=None, endp=None):
        """
        Publish network status (collection of endpoint data)
        
        @param status_data network status to be transmitted
        @param endp Endpoint data
        """
        self.mqtt_client.publish_status(status_data, endp)
        

    def stop(self):
        """
        Stop HTTP server
        """
        self.http_server.stop()


    def __init__(self, working_dir):
        '''
        Constructor
        
        @param working_dir: Working directory
        '''
        cfg_path = os.path.join(working_dir, "config", "lagarto.xml")
        # Read configuration file       
        self.config = XmlLagarto(cfg_path)
        
        ## Local IP address
        address = self._get_local_ip_address()
        # Save IP address in config file
        if self.config.address != address:
            self.config.address = address
            self.config.save()

        # MQTT Client
        self.mqtt_client = LagartoMqttClient(self, self.config)
        
        # HTTP server
        self.http_server = LagartoHttpServer(self, self.config, working_dir)
        self.http_server.start()
