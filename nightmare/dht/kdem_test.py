'''
Created on Dec 11, 2011

@author: Marcus McCurdy <marcus.mccurdy@gmail.com>
'''
import unittest
import kademlia
from datetime import datetime as dt

class Test(unittest.TestCase):


    def test_set_list(self):
        c1_time = dt.now()
        c1 = kademlia.ContactInfo('192.168.176.1', 56789, 1, c1_time)
        c2 = kademlia.ContactInfo('192.168.176.1', 56799, 2, dt.now())
        c3 = kademlia.ContactInfo('192.168.176.1', 9876, 3, dt.now())
        l = [c1, c2, c3]
        s = set(l)
        print(s)
        self.assertTrue(c1 in s)
        self.assertTrue(c1.last_seen == c1_time)
        l[1].last_seen = dt.now()
        print(s)
        print(l)
    
    def test_kbuckets(self):
        kbucket = kademlia.KBucket()
        self.assertTrue(len(kbucket.buckets) == 160)
        for bucket in kbucket.buckets:
            self.assertFalse(bucket)
            
    def test_store_node(self):
        node = kademlia.ContactInfo('192.168.1.1', 56789, 1, dt.now())
        kbucket = kademlia.KBucket()
        kbucket.store_node(node, 1)
        self.assertTrue(len(kbucket.buckets[0]) == 1)
        node50 = kademlia.ContactInfo('192.168.1.2', 56789, 30, dt.now())
        kbucket.store_node(node50, 50)
        self.assertEqual(len(kbucket.buckets[5]), 1)
        
    def test_contact_info_comparisons(self):
        start = dt.now()
        c1 = kademlia.ContactInfo('192.168.176.1', 56789, 1, start)
        c2 = kademlia.ContactInfo('192.168.176.3', 56789, 2, dt.now())
        c3 = kademlia.ContactInfo('192.168.176.4', 56555, 3, dt.now())
        c11 = kademlia.ContactInfo('192.168.176.1', 56789, 1, start)
        self.assertFalse(c1 == c2)
        self.assertTrue(c1 != c2)
        self.assertTrue(c1 < c2)
        self.assertTrue(c2 > c1)
        self.assertTrue(c1 == c11)
        self.assertTrue(c11 >= c1)
        self.assertTrue(c11 <= c1)
        self.assertTrue(c3 > c1)
 
if __name__ == "__main__":
    unittest.main()