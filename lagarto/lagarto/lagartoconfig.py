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
__date__ ="$Jan 25, 2012 20:44:00 AM$"
#########################################################################

from lagartoresources import LagartoException

import xml.etree.ElementTree as xml


class XmlLagarto(object):
    """
    Lagarto configuration class
    """

    def _read(self):
        """
        Read configuration file
        """        
        # Parse XML file
        tree = xml.parse(self.file_name)
        if tree is None:
            return
        # Get the root node
        root = tree.getroot()
        # Read process name
        procname = root.find("procname")
        if procname is not None:
            self.procname = procname.text.replace(" ", "_")
        # Enter comms section
        comms = root.find("comms")
        if comms is not None:
            # Read IP address
            address = comms.find("address")
            if address is not None:
                self.address = address.text
            # Read MQTT server address
            mqttserver = comms.find("mqttserver")
            if mqttserver is not None:
                self.mqttserver = mqttserver.text
            # Read MQTT port
            mqttport = comms.find("mqttport")
            if mqttport is not None:
                self.mqttport = mqttport.text
            # Publish condition
            publish = comms.find("publish")
            if publish is not None:
                self.publish = publish.text
            # Read http port
            httpport = comms.find("httpport")        
            if httpport is not None:
                self.httpport = int(httpport.text)


    def save(self):
        """
        Save current configuration file in disk
        """
        try:
            f = open(self.file_name, 'w')
            f.write("<?xml version=\"1.0\"?>\n")
            f.write("<lagarto>\n")
            f.write("\t<procname>" + self.procname + "</procname>\n")
            f.write("\t<comms>\n")
            if self.address is not None:
                f.write("\t\t<address>" + self.address + "</address>\n")
            if self.mqttserver is not None:
                f.write("\t\t<mqttserver>" + self.mqttserver + "</mqttserver>\n")
            if self.mqttport is not None:
                f.write("\t\t<mqttport>" + self.mqttport + "</mqttport>\n")
            if self.publish is not None:
                f.write("\t\t<publish>" + self.publish + "</publish>\n")
            if self.httpport is not None:
                f.write("\t\t<httpport>" + str(self.httpport) + "</httpport>\n")
            f.write("\t</comms>\n")
            f.write("</lagarto>\n")
            f.close()
        except:
            raise LagartoException("Unable to save " + self.file_name) 
        
        
    def __init__(self, file_name="lagarto.xml"):
        """
        Class constructor
        
        @param filename: path to the configuration file
        """       
        ## Name/path of the current configuration file
        self.file_name = file_name
        
        ## Process name
        self.procname = None
                
        ## MQTT server address
        self.mqttserver = "localhost"
        
        ## MQTT port
        self.mqttport = 1883
        
        ## Publish condition. Publish on event by default
        self.publish = "event"
        
        ## HTTP server port
        self.httpport = None
        
        ## Local IP address
        self.address = None
               
        ## PUSh address
        self.push_address = "tcp://*:5001"

        ## PULL address
        self.pull_address = "tcp://localhost:5001"

        # Read XML file
        self._read()
