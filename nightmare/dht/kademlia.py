"""
Classes and methods for the Kademlia DHT protocol.
"""

class ContactInfo(object):
    """Class that holds the contact information for a node in the Kademlia
    network. Instances of this class are stored in the k-buckets.
    """

    def __init__(self, ip, port, node_id, last_seen=None):
        """init for a node in a k-bucket.
        ip is the
        """
        self.ip = ip
        self.port = port
        self.node_id = node_id
        self.last_seen = last_seen
