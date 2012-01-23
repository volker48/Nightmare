"""
Classes and methods for the Kademlia DHT protocol.
"""
from datetime import datetime as dt
from uuid import uuid4
from hashlib import sha1
import sqlite3

class Node(object):
    """
    Class that holds the contact information for a node in the Kademlia
    network. Instances of this class are stored in the k-buckets.
    """

    def __init__(self, ip, port, node_id, last_seen=None):
        """
        init for a node in a k-bucket.
        """
        self.ip = ip
        self.port = port
        self.node_id = node_id
        self.last_seen = last_seen
        
    def __eq__(self, other):
        return self.node_id == other.node_id
    
    def __ne__(self, other):
        return self.node_id != other.node_id
    
    def __lt__(self, other):
        return self.last_seen < other.last_seen
    
    def __gt__(self, other):
        return self.last_seen > other.last_seen
    
    def __ge__(self, other):
        return self.last_seen >= other.last_seen

    def __le__(self, other):
        return self.last_seen <= other.last_seen
        
    def __str__(self):
        message = 'node<%s>@%s:%d last_seen: %s' 
        return message % (self.node_id, self.ip, self.port, self.last_seen)
    
    def __repr__(self):
        return str(self.__dict__)


class KBucket(object):
    """
    Class to handle k-buckets.
    """
    
    def __init__(self, node_id, k=20):
        """
        k --- The number of nodes to store in each KBucket defaults to 20
        """
        self.node_id = node_id
        self.k = k
        self.buckets = [list() for i in xrange(160)]
        
    def store_node(self, node):
        """
        @param node: The Node of the node to store in a k-bucket  
        """
        distance = long(self.node_id, 16) ^ long(node.node_id, 16)
        i = self._find_bucket_index(distance)
        to_update = [x for x in self.buckets[i] if x == node]
        if to_update:
            assert(len(to_update) == 1)
            to_update[0].last_seen = dt.now()
        else:                    
            if len(self.buckets[i]) < self.k:                    
                self.buckets[i].append(node) 
            else:
                #need to ping oldest node and if it doesn't respond replace it and if it does drop new contact
                pass                   
        self.buckets[i].sort() 
            
    def _find_bucket_index(self, distance):
        """
        Finds the index of the bucket a node at distance belongs in
        distance --- The integer XOR of the node's id with the node this KBucket belongs to
        """
        for i in xrange(160):
            lower_bound = 2**i
            upper_bound = 2**(i+1)
            if lower_bound <= distance < upper_bound:
                return i
        raise Exception("Did not find kbucket for distance %d" % distance)
    
    def find_k_closest(self, target_id):
        distances = []
        for bucket in self.buckets:
            for node in bucket:
                distance = long(target_id, 16) ^ long(node.node_id, 16)
                distances.append((node, distance))
        distances.sort(key=lambda x: x[1])        
        return [x[0] for x in distances][:self.k]
            
def generate_id():
    """Generates a random UUID and returns the SHA-1 hash of it.
    """
    random_uuid = uuid4()
    sha = sha1()
    sha.update(random_uuid.hex)
    return sha.hexdigest()

class SQLitePersistence(object):
    
    def __init__(self, db_filename):
        self.connection =  sqlite3.connect(db_filename)
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS hashtable (key TEXT PRIMARY KEY, value BLOB);")
        
        self.connection.commit()
        
    def store(self, key, value):
        self.cursor.execute("INSERT INTO hashtable VALUES (?, ?);", (key, value))    
        self.connection.commit()
        
    def retrieve(self, key):
        self.cursor.execute("SELECT value FROM hashtable WHERE key=?;", (key, ))
        r = self.cursor.fetchone()
        if r:
            return r[0]
        else:
            return None
        
class Kademlia(object):
    
    def __init__(self, persistance=SQLitePersistence, db_filename='nightmare.db', alpha=3):
        self.node_id = generate_id()
        self.kBuckets = KBucket(self.node_id)
        self.persist = persistance(db_filename)
        self.alpha = alpha
    
    def find_node(self, requester_info, target_id):
        """FIND NODE takes a 160-bit ID as an argument 
        The recipient of a the RPC returns <IPaddress,UDPport,NodeID> triples for the 
        k nodes it knows about closest to the target ID. These triples can come from 
        a single k-bucket, or they may come from multiple k-buckets if the closest 
        k-bucket is not full. In any case, the RPC recipient must return k items 
        (unless there are fewer than k nodes in all its k-buckets combined, in which 
        case it returns every node it knows about).
        """
        if requester_info:
            self.kBuckets.store_node(requester_info)
        return self.kBuckets.find_k_closest(target_id)
        
    def find_value(self, requester_info, key):
        self.kBuckets.store_node(requester_info)
        val = self.persist.retrieve(key)
        if val:
            return val
        return self.find_node(None, key)
    
    def ping(self, requester_info):
        self.kBuckets.store_node(requester_info)
        return self.node_id
        
    def store(self, requester_info, key, value):
        self.kBuckets.store_node(requester_info)
        self.persist.store(key, value)
        return 'SUCCESS'

    def node_lookup(self, key):
        nodes = []
        nodes.append(self.find_node(None, key))