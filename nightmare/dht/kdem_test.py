'''
Created on Dec 11, 2011

@author: Marcus McCurdy
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
        
 
if __name__ == "__main__":
    unittest.main()