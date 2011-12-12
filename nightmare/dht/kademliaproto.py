'''
Created on Dec 12, 2011

@author: Marcus McCurdy <marcus.mccurdy@gmail.com>
'''

from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory

class KademliaProtocol(Protocol):
    
    def dataReceived(self, data):
        Protocol.dataReceived(self, data)
        
class KademliaFactory(Factory):
    protocol = KademliaProtocol
    
    def __init__(self):
        pass
