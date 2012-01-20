from twisted.application import service, internet
from dht.kademliaproto import KademliaService, IPerspectiveKademlia
from dht.kademlia import Kademlia
from twisted.spread import pb

application = service.Application('nightmare')
service = KademliaService(Kademlia())
internet.TCPServer(56789, pb.PBServerFactory(IPerspectiveKademlia(service))).setServiceParent(application)
