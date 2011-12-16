'''
Created on Dec 13, 2011

@author: Marcus McCurdy <marcus.mccurdy@gmail.com>
'''
from twisted.spread import pb
from twisted.internet import reactor
from twisted.python import util

if __name__ == '__main__':
    factory = pb.PBClientFactory()
    reactor.connectTCP("localhost", 8789, factory)
    d = factory.getRootObject()
    d.addCallback(lambda object: object.callRemote("find_node", "1234567"))
    d.addBoth(lambda _: reactor.stop())
    reactor.run()