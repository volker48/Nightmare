'''
Created on Dec 13, 2011

@author: marcusmccurdy
'''
from twisted.internet import reactor
from twisted.spread.pb import PBServerFactory
from dht.kademliaproto import Remote_Kademlia, Kademlia

if __name__ == '__main__':
    remote = Remote_Kademlia(Kademlia())
    reactor.listenTCP(8789, PBServerFactory(remote))
    reactor.run()