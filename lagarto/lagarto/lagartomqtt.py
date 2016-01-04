#########################################################################
#
# Copyright (c) 2016 Daniel Berenguer <dberenguer@panstamp.com>
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
__author__="panStamp S.L.U."
__date__  ="$Jan 04, 2016$"
#########################################################################

from lagartoconfig import XmlLagarto
from lagartoresources import LagartoException, LagartoMessage

import paho.mqtt.client as mqtt
import threading
import json
import os
import time


class LagartoMqttClient(object):
    """
    MQTT client
    """

    def on_connect(self, client, userdata, flags, rc):
        """
        Callback function: connection completed
        """
        print("Connected to MQTT broker " + self.mqttserver + " on port " + str(self.mqttport))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(self.procname + "/simple/control/#")   # Simple control topic
        client.subscribe(self.procname + "/json/control/#" )    # JSON control topic        


    def on_message(self, client, userdata, msg):
        """
        Callback function: message published from server
        """
        print("Message received on topic " + msg.topic + " with QoS " + str(msg.qos) + " and payload " + msg.payload)

        topic = msg.tipic.split("/")
        if len(topic) >= 3:
          if topic[0] == self.procname:
              if topic[2] == "control":
                  status_data = []
                  if topic[1] == "simple":
                      if len(topic) == 5:
                          endpoint_data = {}
                          endpoint_data["location"] = topic[3]
                          endpoint_data["name"] = topic[4]
                          endpoint_data["value"] = msg.payload
                          status_data = [endpoint_data]
                  elif topic[1] == "json":
                      status_data = json.loads(msg.payload)["lagarto"]["status"]
                  
                  if len(status_data) > 0:    
                      status = data_server.set_status(status_data)
                      self.publish_status(status)


    def publish_status(self, status_data=None, endp=None):
        """
        Publish network status (collection of endpoint data)
        
        @param status_data network status to be transmitted
        @param endp Endpoint data
        """
        self.publish_lock.acquire()
        try:
            http_server = self.address + ":" + str(self.httpport)
            
            if endp is not None:
                status_data = [endp.dumps()]
                
            # Message in JSON format
            lagarto_msg = LagartoMessage(proc_name=self.procname, http_server=http_server, status=status_data)
            msg = json.dumps(lagarto_msg.dumps())
            topic = self.procname + "/json/status"    
            self.mqtt_client.publish(topic, payload=msg, qos=0, retain=False)
            
            # Message in simple format
            if status_data is not None:
                for endp_data in status_data:
                    topic = self.procname + "/simple/status/" + endp_data["location"] + "/" + endp_data["name"]
                    msg = endp_data["value"]
                    self.mqtt_client.publish(topic, payload=msg, qos=0, retain=False)
            
        finally:
            self.publish_lock.release()      


    def stop(self):
        """
        Stop MQTT client
        """
        self.mqtt_client.loop_stop()


    def __init__(self, data_server, config):
        '''
        Constructor
        
        @param working_dir: Working directory
        '''       
        ## Data server, probably the parent object
        self.data_server = data_server
        ## Process name
        self.procname = config.procname
        ## Own IP address
        self.address = config.address
        ## Own HTTP port
        self.httpport = config.httpport

        ## MQTT server
        self.mqttserver = config.mqttserver
        ## MQTT port
        self.mqttport = config.mqttport

        ## MQTT client
        self.mqtt_client = mqtt.Client()
       
        # Assign MQTT callbacks
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        
        # Connecto to MQTT broker
        self.mqtt_client.connect(config.mqttserver, int(config.mqttport), 60)
        
        # Run MQTT thread
        self.mqtt_client.loop_start()

        self.publish_lock = threading.Lock()
        
        # Heart beat transmission thread
        hbeat_process = PeriodicHeartBeat(self.publish_status)
        hbeat_process.start()


class PeriodicHeartBeat(threading.Thread):
    """
    Periodic transmission of Lagarto server heart beat
    """
    def run(self):
        """
        Start timer
        """
        while True:
            self.send_hbeat()
            time.sleep(60.0)
                      
    def __init__(self, send_hbeat):
        """
        Constructor
        
        @param send_hbeat: Heart beat transmission method
        """
        threading.Thread.__init__(self)
        # Configure thread as daemon
        self.daemon = True
        # Heart beat transmission method
        self.send_hbeat = send_hbeat
