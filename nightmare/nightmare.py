#!/usr/bin/env python

import dht.kademlia
import logging
import argparse

def main():
    parser = argparse.ArgumentParser(description="Nightmare PUB/SUB")
    parser.add_argument("--logfile", default="nightmare.log", 
                    help="The name of the log file (default: nightmare.log)")
    args = parser.parse_args()
    logging.basicConfig(filename=args.logfile,level=logging.DEBUG)
    logging.info("Staring Kademlia")
    contact = dht.kademlia.ContactInfo("192.168.176.2", 56789, 1234)
    print contact
    print repr(contact)

if __name__ == "__main__":
    main()
