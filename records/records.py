#!/usr/bin/env python

import pandas as pd
import requests
import json

class Records:
    def __init__(self, genusKey=None, year=None):
        
        # store input params
        self.genusKey = genusKey
        self.year = year
        
        # will be used to store output results
        self.df = None
        self.json = None
        
    def get_single_batch(self, offset=0, limit=20):
        "returns JSON result for a small batch query"
        res = requests.get(
        url="https://api.gbif.org/v1/occurrence/search/",
        params={
            "genusKey": self.genusKey,
            "year": self.year,
            "offset": offset,
            "limit": limit,
            "hasCoordinate": "true",
            "country": "US",
            }
        )
        return res.json()
        
    def get_all_records(self):
        "stores result for all records to self.json and self.df"
        # for storing results
        alldata = []
    
        # continue until we call 'break'
        offset = 0
        while 1:
        
            # get JSON data for a batch 
            self.json = self.get_single_batch(offset, 300)
        
            # increment counter by 300 (the max limit)
            offset += 300
        
            # add this batch of data to the growing list
            alldata.extend(self.json["results"])
        
            # stop when end of record is reached
            if self.json["endOfRecords"]:
                print(f'Done. Found {len(alldata)} records')
                break
            
            # print a dot on each rep to show progress
            print('.', end='')
        
        #store the result as self.df 
        self.df = pd.json_normalize(alldata)
        return self.df