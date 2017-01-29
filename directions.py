
class routePoint(object):
    def __init__(self, inLat, inLon, inEle=None, inStart=False, inEnd=False):
        self.lat = inLat
        self.lon = inLon
        self.ele = inEle
        self.start = inStart
        self.end = inEnd

    def display(self):
        print("\n" + repr(self.lat) + "\t" + repr(self.lon) + "\t" + repr(self.ele) + "\t" + repr(self.start) + " " + repr(self.end))


def routeInfo(startpnt, endpnt, key, mode='driving', plot=False, plotfile='mymap.html'):
    import googlemaps
    import json
    import polyline
    client = googlemaps.Client(key)
    dirResult = client.directions(startpnt, endpnt, mode, waypoints=None, alternatives=False, avoid=None, language=None, units=None, region=None, departure_time=None, arrival_time=None, optimize_waypoints=True, transit_mode=None, transit_routing_preference=None, traffic_model=None)


    #print json.dumps(dirResult, indent=4, sort_keys=True)

    routePoints = [];

    points = []
    #latitudes1 = []
    #longitudes1 = []
    samples = 0;

    for item in dirResult[0]['legs'][0]['steps']:
        code = str(item['polyline']['points'])
        poly = polyline.decode(code)
        for coord in poly:
            tmpPoint = routePoint(coord[0], coord[1])
            if (samples == 0):
                tmpPoint.start = True
            routePoints.append(tmpPoint)
            samples = samples + 1
            points.append(coord)
            #latitudes1.append(coord[0])
        	#longitudes1.append(coord[1])

    #print routePoints

    eleResult = client.elevation_along_path(points, samples)
    #elevation = []
    #for point in eleResult:
    for i in range(0, samples):
        #elevation.append(point['elevation'])
        routePoints[i].ele = eleResult[i]['elevation']
        if (i == samples-1):
            routePoints[i].end = True



    #for point in routePoints:
    #    point.display()


    if plot:
        import gmplot
        gmap = gmplot.GoogleMapPlotter(47.6682253, -122.3195193, 16)
        gmap.plot(latitudes1, longitudes1, 'cornflowerblue', edge_width=10)
        gmap.scatter(latitudes1, longitudes1, 'r', marker=True)
        gmap.draw(plotfile)

    return routePoints


startpnt = '5336 8th Ave NE, Seattle, WA 98105'
endpnt = 'Space Needle , Seattle, WA 98105'

mode = 'driving'

key = 0


route = routeInfo(startpnt, endpnt, key)

import texttable as tt
tab = tt.Texttable()
x = [[]] # The empty row will have the header
for point in route:
    x.append([point.lat,point.lon,point.ele,point.start,point.end])
tab.add_rows(x)
tab.set_cols_align(['r','r','r','r','r'])
tab.header(['Latitude', 'Longitude', 'Elevation','Start','End'])
print tab.draw()
