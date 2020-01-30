from makerfuncs.State import State
from makerfuncs.states import STATES

USER_AREAS = {
	'OL': State(
		parent = 'CZ',
		name   = 'Olomouc',
		number = 8800,
		pois   = ['./pois/chs.osm.xml',],
		crop   = True
	),
}