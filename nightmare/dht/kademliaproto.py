'''
Created on Dec 12, 2011

@author: Marcus McCurdy <marcus.mccurdy@gmail.com>
'''

from twisted.internet.protocol import Factory, Protocol
from twisted.spread import pb

class KademliaProtocol(Protocol):
    
    def dataReceived(self, data):
        pass

        
class KademliaFactory(Factory):

    protocol = KademliaProtocol
    
    def __init__(self, kademlia):
        self.kademlia = kademlia


class Remote_Kademlia(pb.Root):
    
    def __init__(self, kademlia):
        self.kademlia = kademlia
        
    def remote_find_node(self, requestor_info, node_id):
        self.kademlia.find_node(requestor_info, node_id)
    
    def remote_find_value(self, requestor_info, key):
        self.kademlia.find_value(requestor_info, key)
    
    def remote_ping(self, requestor_info):
        self.kademlia.ping(requestor_info)
    
    def remote_store(self, requestor_info, key, value):
        self.kademlia.store(requestor_info, key, value)