'''
Created on Dec 11, 2011

@author: Marcus McCurdy <marcus.mccurdy@gmail.com>
'''
import unittest
from datetime import datetime as dt
from nightmare.dht import kademlia
from nightmare.dht.kademlia import ContactInfo

class Test(unittest.TestCase):

    
    
    def test_kbuckets(self):
        kbucket = kademlia.KBucket(kademlia.generate_id())
        self.assertTrue(len(kbucket.buckets) == 160)
        for bucket in kbucket.buckets:
            self.assertFalse(bucket)
            
    def test_store_node(self):
        node = kademlia.ContactInfo('192.168.1.1', 56789, '2', dt.now())
        kbucket = kademlia.KBucket('3')
        kbucket.store_node(node)
        self.assertTrue(len(kbucket.buckets[0]) == 1)
        node50 = kademlia.ContactInfo('192.168.1.2', 56789, '32', dt.now())
        kbucket.store_node(node50)
        self.assertEqual(len(kbucket.buckets[5]), 1)
        
    def test_contact_info_comparisons(self):
        start = dt.now()
        id1 = kademlia.generate_id()
        id2 = kademlia.generate_id()
        id3 = kademlia.generate_id()
        c1 = kademlia.ContactInfo('192.168.176.1', 56789, id1, start)
        c2 = kademlia.ContactInfo('192.168.176.3', 56789, id2, dt.now())
        c3 = kademlia.ContactInfo('192.168.176.4', 56555, id3, dt.now())
        c11 = kademlia.ContactInfo('192.168.176.1', 56789, id1, start)
        self.assertFalse(c1 == c2)
        self.assertTrue(c1 != c2)
        self.assertTrue(c1 < c2)
        self.assertTrue(c2 > c1)
        self.assertTrue(c1 == c11)
        self.assertTrue(c11 >= c1)
        self.assertTrue(c11 <= c1)
        self.assertTrue(c3 > c1)
        
    def test_kademlia_init(self):
        kdem = kademlia.Kademlia()
        print('id: %s' % kdem.node_id)
        
    def test_find_node(self):
        nodes = []
        for x in xrange(1, 30):
            nodes.append(kademlia.ContactInfo('192.168.1.%d' % x, 56789, '%d' %x))
        
        node_under_test = kademlia.Kademlia()
        for node in nodes:
            node_under_test.ping(node)
        some_id = kademlia.generate_id()
        k_nodes = node_under_test.find_node(kademlia.ContactInfo('192.168.176.12', 56789, kademlia.generate_id()), some_id)
        self.assertEqual(node_under_test.kbuckets.k, len(k_nodes), 'Invalid number of nodes returned')
        
    def test_store(self):
        node = kademlia.Kademlia(db_filename='test.db')
        requestor = ContactInfo('192.168.11.1', 56789, kademlia.generate_id())
        key = 'foo'
        val = 'bar'
        node.store(requestor, key, val)
        found_value = node.find_value(requestor, key)
        self.assertEqual(val, found_value)
 
if __name__ == "__main__":
    unittest.main()

