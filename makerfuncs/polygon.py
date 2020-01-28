# https://wiki.openstreetmap.org/wiki/Osmosis/Polygon_Filter_File_Python_Parsing
import pyclipper, re
from pprint import pprint
from geojson import Polygon, Feature, FeatureCollection





def parse_poly(o):
	fp = open('./poly/' + o.state.data_id + '.poly', "r")
	lines = fp.readlines()

	in_ring = False
	coords = []
	
	for (index, line) in enumerate(lines):
		if index == 0:
			# first line is junk.
			continue
		
		elif index == 1:
			# second line is the first polygon ring.
			coords.append([[], []])
			ring = coords[-1][0]
			in_ring = True
		
		elif in_ring and line.strip() == 'END':
			# we are at the end of a ring, perhaps with more to come.
			in_ring = False
	
		elif in_ring:
			# we are in a ring and picking up new coordinates.
			ring.append(map(float, line.split()))
	
		elif not in_ring and line.strip() == 'END':
			# we are at the end of the whole polygon.
			break
	
		elif not in_ring and line.startswith('!'):
			# we are at the start of a polygon part hole.
			coords[-1][1].append([])
			ring = coords[-1][1][-1]
			in_ring = True
	
		elif not in_ring:
			# we are at the start of a polygon part.
			coords.append([[], []])
			ring = coords[-1][0]
			in_ring = True

	pco = pyclipper.PyclipperOffset()


	print("len coords =",len(coords))
	
	path = []
	for polygon in coords:
		if len(polygon[0]) == 0:
			continue

		path = []
		for points in polygon:
			for point in points:
				coord = list(point)
				print("coord", coord[0], coord[1])
				coord = (int(coord[0]*100000), int(coord[1]*100000))
				print("coord", coord[0], coord[1])
				path.append( coord )

		print(path)
		print("--------------")
		

		# FIXME


	# path = ((171, 495), (171, 497), (175, 497), (175, 495), (171, 495))
	# path = ((180, 200), (260, 200), (260, 150), (180, 150))

	print("path", path)
	# http://www.angusj.com/delphi/clipper/documentation/Docs/Units/ClipperLib/Classes/ClipperOffset/Methods/AddPath.htm
	pco.AddPath(path, pyclipper.JT_MITER, pyclipper.ET_CLOSEDPOLYGON)

			
	solution = pco.Execute(2.0)		#0.84 cca 1 m
	solution = solution[0]

	print("solution", solution)

	solution.append(solution[0])
	print("solution", solution)

	i = 0
	for point in solution:
		solution[i] = (point[0]/100000, point[1]/100000)
		i += 1

	print("solution", solution)
	test = Polygon([solution])


	my_feature = Feature(geometry=test)
	feature_collection = FeatureCollection([my_feature])

	print()
	print(feature_collection)




def load(o):
	# Pokud existuje *.poly nactu ho
	# if not os.path.isfile('./polygons/' + o.state.data_id + '.poly'):
	return