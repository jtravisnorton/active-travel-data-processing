# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 08:45:49 2014

@author: johnnort
"""
from xml.dom import minidom
import pandas
import datetime
class gpx_to_csv:
  def __init__(self, filename):
    self.tracks = {}
    self.filename = filename        
    self.outfile = self.filename.split('.')[0]+".csv"    
    try:
      doc = minidom.parse(filename)
      doc.normalize()
    except:
      return # handle this properly later
    gpx = doc.documentElement
    seg = 0    
    for node in gpx.getElementsByTagName('trk'):
      self.parseTrack(node, seg)
      seg += 1
  def parseTrack(self, trk, seg):
    name = trk.getElementsByTagName('name')[0].firstChild.data
    if not name in self.tracks:
      self.tracks[name] = {}
    for trkseg in trk.getElementsByTagName('trkseg'):
      for trkpt in trkseg.getElementsByTagName('trkpt'):
        lat = float(trkpt.getAttribute('lat'))
        lon = float(trkpt.getAttribute('lon'))
        ele = float(trkpt.getElementsByTagName('ele')[0].firstChild.data)
        rfc3339 = trkpt.getElementsByTagName('time')[0].firstChild.data
        time = datetime.datetime.strptime(rfc3339, '%Y-%m-%dT%H:%M:%SZ')
        self.tracks[name][time]={'lat':lat,'lon':lon,'ele':ele,'seg':seg}
  def getTrack(self, name):
    times = self.tracks[name].keys()
    points = [self.tracks[name][time] for time in times.sort()]
    return [(point['lat'],point['lon']) for point in points]
    
  def getTracks(self):
      return self.tracks
    
  def tracks_to_csv(self, out = ""):
        df = pandas.DataFrame.from_dict(self.tracks[self.tracks.keys()[0]], orient='index')       
        for node in self.tracks.keys()[1:]:
            df = df.append(pandas.DataFrame.from_dict(self.tracks[node],orient='index'))
        if out == "":
            out = self.outfile
        #df['ParticipantID'] = self.filename.split('\\')[-1].split('_')[0]
        #df['phase'] = self.filename.split('\\')[-1].split('_')[1]
        df.to_csv(out, index_label = 'time')
        """Plot tracks on a map"""        
        x = df.lon.tolist()
        y = df.lat.tolist()        
        m = Basemap(llcrnrlon=min(x), llcrnrlat=min(y), urcrnrlon=max(x), urcrnrlat=max(y), 
                    projection='tmerc', resolution='h', lon_0=-78.58333333333333, lat_0=40.0)
        x, y = m(x,y)
        plot.title("Plot of %s tracks for participant %s." % (str(len(df)), self.filename.split('\\')[-1].split('_')[0]))      
        #m.fillcontinents(color='#cc9966',lake_color='#99ffff')
        #m.drawcounties(linewidth = 1, color='black')
        #m.drawmapboundary(fill_color='#99ffff')
        m.scatter(x,y,1,marker='o',color='green')        
        return df
