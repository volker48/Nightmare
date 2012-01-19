'''
Created on Dec 12, 2011

@author: Marcus McCurdy <marcus.mccurdy@gmail.com>
'''
from twisted.spread import pb
from twisted.application import service
from twisted.internet import defer
from nightmare.dht import kademlia


class PerspectiveKademliaFromService(pb.Root):
    
    def __init__(self, service):
        self.service = service
        
    def remote_find_node(self, requestor_info, node_id):
        self.service.find_node(requestor_info, node_id)
    
    def remote_find_value(self, requestor_info, key):
        self.service.find_value(requestor_info, key)
    
    def remote_ping(self, requestor_info):
        self.service.ping(requestor_info)
    
    def remote_store(self, requestor_info, key, value):
        self.service.store(requestor_info, key, value)
        
        
class KademliaService(service.Service):
    
    def __init__(self, kdem):
        self.kdem = kdem
    
    def find_node(self, requestor_info, node_id):
        return defer.succeed(self.kdem.find_node(requestor_info, node_id))
    
    def find_value(self, requestor_info, key):
        return defer.succeed(self.kdem.find_value(requestor_info, key))
    
    def ping(self, requestor_info):
        return defer.succeed(self.kdem.ping(requestor_info))
    
    def store(self, requestor_info, key, value):
        return defer.succeed(self.kdem.store(requestor_info, key, value))
    
    def startService(self):
        service.Service.startService(self)
        
    def stopService(self):
        service.Service.stopService(self)