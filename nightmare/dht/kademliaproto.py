'''
Created on Dec 12, 2011

@author: Marcus McCurdy <marcus.mccurdy@gmail.com>
'''
from twisted.spread import pb
from twisted.application import service
from twisted.internet import defer
from zope.interface import Interface, implements
from twisted.python import components

class IKademliaService(Interface):
    
    def find_node(requestor_info, node_id):
        """
        Returns the k closest nodes to node_id that his node knows
        """
    def find_value(requestor_info, key):
        """
        Returns value assigned key if this node previously received
        a store request for key and value or the k closest nodes
        to the key that this node knows about
        """
        
    def ping(requestor_info):
        """
        Used to determine if this node is still online
        """
        
    def store(requestor_info, key, value):
        """
        Instructors this node to store value at key
        """

class IPerspectiveKademlia(Interface):
    
    def remote_find_node(requestor_info, node_id):
        """
        Returns the k closest nodes to node_id that his node knows
        """
    def remote_find_value(requestor_info, key):
        """
        Returns value assigned key if this node previously received
        a store request for key and value or the k closest nodes
        to the key that this node knows about
        """
        
    def remote_ping(requestor_info):
        """
        Used to determine if this node is still online
        """
        
    def remote_store(requestor_info, key, value):
        """
        Instructors this node to store value at key
        """

class PerspectiveKademliaFromService(pb.Root):
    implements(IPerspectiveKademlia)
    
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
        
components.registerAdapter(PerspectiveKademliaFromService, 
                           IKademliaService, 
                           IPerspectiveKademlia)
        
class KademliaService(service.Service):
    
    implements(IKademliaService)
    
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