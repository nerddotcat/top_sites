#!/usr/bin/env python

import requests
import argparse
import sys


def loadSiteList(fileName):
  """Returns list of domains from given file.
    
    Assumes that the file is a list of each site separated by a newline.
    
    Args:
      fileName (str): Path to the file we want to get sites from.
      
    Returns:
      list of strings: List of sites we want to visit.
  """
  fp = open(fileName,'r')
  #get sites and throw out blank lines
  siteList = [ x for x in fp.read().split() if len(x) > 0]
  fp.close()
  return siteList

def visitSite(site, verbose=False):
  """Returns dictionary with site information
    
    Attempts to connect to the given website and returns a dictionary.
    
    Args:
      site (str): Web address to visit, should not contain 'http://'.
      verbose (boolean): If True, will print if a site was successfully visited.
      
    Returns:
      dictionary: Dictionary with attributes we want to use.
  """
  fullUrl = "http://{}".format(site)
  siteData = {'url': fullUrl, 'site': site}
  try:
    siteResp = requests.get(fullUrl)
    
    siteData['ok'] = siteResp.ok
    siteData['html'] = siteResp.text
    siteData['sizekb'] = int(len(siteData['html'])/1000)
    siteData['time'] = siteResp.elapsed.total_seconds()
    
    if verbose:
      print("[+] Visited {} {}kb {}s".format(site, siteData['sizekb'], siteData['time']) )
  
  #consider handling other types of exceptions
  except Exception as e:
    siteData['ok'] = False
    if verbose:
      print("[-] Failed to load {}".format(site) )
  
  return siteData


def getMedian(values,attribute):
  """Returns median value from values list, with the given attribute
    
    Args:
      values (list of dictionaries): Assumed that this is sorted based on attribute
      attribute (str): name of attribute from dictionary defined from visitSite function
      
    Returns:
      int/float: Median value for given attribute
  """
  median = -1
  if len(values) % 2 == 0:
    #if even amount of values, take average of two middle values
    index = int(len(values)/2)
    median = (values[index][attribute]+values[index-1][attribute])/2.0
  else:
    #else odd, grab middle value
    index = int(len(values)/2)
    median = values[index][attribute]
  return median

def main():
  """Main function for script
     
     Calls functions to gather site information, processes, and prints data.
  """
  #parse command line arguments
  parser = argparse.ArgumentParser()
  parser.add_argument("-v", help="show more verbose output", action='store_true')
  parser.add_argument("path", help="path to file that contains a list of sites")
  args = parser.parse_args()
  #load the list of sites
  sites = loadSiteList(args.path)
  
  if args.v:
    print("[+] Loaded a list of {} sites".format(len(sites)))
  
  
  siteResp = []
  badResp = []
  #gather site information
  for site in sites:
    response = visitSite(site,args.v)
    if response['ok']:
      siteResp.append(response)
    else:
      badResp.append(response)
    
  if args.v:
    print("[+] Visited {} sites".format(len(siteResp)))
    if len(badResp):
      print("[-] Failed to visit {} sites".format(len(badResp)))
  
  # we're just going to exit if less than 5 sites were visited
  if len(siteResp) < 5:
    print("Did not successfully visit at least 5 sites, exiting...")
    sys.exit()
  
  #process and print information
  timeSort = sorted(siteResp, key=lambda x: x['time'])
  sizeSort = sorted(siteResp, key=lambda x: x['sizekb'])
  
  print("Fastest 5 Sites:")
  for index in range(5):
    site = timeSort[index]
    print("{} {}kb {}s".format(site['site'], site['sizekb'], site['time']))
  
  print("")#for newline
  
  print("Slowest 5 Sites:")
  for index in range(1,6):
    site = timeSort[-index]
    print("{} {}kb {}s".format(site['site'], site['sizekb'], site['time']))
  
  print("")#for newline
  
  #print median size
  print("Median Homepage Size: {}kb".format( int(getMedian(sizeSort,'sizekb')) ))
  
  #print median download time
  print("Median Homepage Download Time: {}s".format( getMedian(timeSort,'time') ))
  
  


if __name__ == '__main__':
  main()
