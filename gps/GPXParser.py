# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 08:45:49 2014

@author: johnnort
"""
from xml.dom import minidom
import pandas, os

class GPXParser:
  def __init__(self, filename):
    self.tracks = {}
    self.filename = filename        
    self.outfile = self.filename.split('.')[0]+".csv"    
    try:
      doc = minidom.parse(filename)
      doc.normalize()
    except:
      return # handle this later
    gpx = doc.documentElement
    for node in gpx.getElementsByTagName('trk'):
      self.parseTrack(node)

  def parseTrack(self, trk):
    name = trk.getElementsByTagName('name')[0].firstChild.data
    if not name in self.tracks:
      self.tracks[name] = {}
    for trkseg in trk.getElementsByTagName('trkseg'):
      for trkpt in trkseg.getElementsByTagName('trkpt'):
        lat = float(trkpt.getAttribute('lat'))
        lon = float(trkpt.getAttribute('lon'))
        ele = float(trkpt.getElementsByTagName('ele')[0].firstChild.data)
        rfc3339 = trkpt.getElementsByTagName('time')[0].firstChild.data
        self.tracks[name][rfc3339]={'lat':lat,'lon':lon,'ele':ele}

  def getTrack(self, name):
    times = self.tracks[name].keys()
    points = [self.tracks[name][time] for time in times.sort()]
    return [(point['lat'],point['lon']) for point in points]
    
  def getTracks(self):
      return self.tracks
    
  def tracks_to_csv(self, out):
        df = pandas.DataFrame.from_dict(self.tracks[self.tracks.keys()[0]], orient='index')       
        for node in self.tracks.keys()[1:]:
            df = df.append(pandas.DataFrame.from_dict(self.tracks[node],orient='index'))
        if out == "":
            out = self.outfile
        df.to_csv(out, index_label = 'time')
        print "The GPS device belonging to participant %s recorded %s tracks." % (self.filename.split('\\')[-1].split('_')[0], str(len(df)))       
        return df
