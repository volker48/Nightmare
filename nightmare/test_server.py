'''
Created on Dec 13, 2011

@author: Marcus McCurdy <marcus.mccurdy@gmail.com>
'''
from twisted.internet import reactor
from twisted.spread.pb import PBServerFactory
from dht.kademliaproto import PerspectiveKademliaFromService, Kademlia

if __name__ == '__main__':
    remote = PerspectiveKademliaFromService(Kademlia())
    reactor.listenTCP(8789, PBServerFactory(remote))
    reactor.run()