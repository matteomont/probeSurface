#!/usr/bin/env python

import os
import shutil
import sys

import numpy
import re

args = sys.argv

# default values
probeLineDictName = 'probeSurfaceDict'
probesDict = 'probesDict'


#filename = './system/' + probeLineDictName
filename = probeLineDictName
myfile = open(filename,'r')
probeLineDict = myfile.readlines()
myfile.close()

#filenameW = './system/' + probesDict
filenameW = probesDict
mywfile = open(filenameW,'w')

entryFields = '\n'
entryOutput = '\n'

doTheFields = False

for line in probeLineDict:

	# points
	if line.startswith('start'):
		startCoordsF = map(float,re.findall(r"[-+]?\d*\.\d+|\d+",line))
		startCoords = numpy.array(startCoordsF)
	if line.startswith('end'):
		endCoordsF = map(float,re.findall(r"[-+]?\d*\.\d+|\d+",line))
		endCoords = numpy.array(endCoordsF)
	if line.startswith('nPoints_y'):
		nPointsy = map(int,re.findall("\d+",line))[0]
	if line.startswith('nPoints_z'):
		nPointsz = map(int,re.findall("\d+",line))[0]

# generate points
probeLocationsData = '\n'
incrVecy = (endCoords[1] - startCoords[1])/(nPointsy-1)
incrVecz = (endCoords[2] - startCoords[2])/(nPointsz-1)

for j in range(0,nPointsy):
	for i in range(0,nPointsz):
		tmpPointy = startCoords[1] + j*incrVecy
		tmpPointz = startCoords[2] + i*incrVecz
		probeLocationsData += '\t( ' + startCoords[0].astype('|S6') + ' '
		probeLocationsData += tmpPointy.astype('|S6') + ' '
		probeLocationsData += tmpPointz.astype('|S6') + ' )\n'


# strings
headerOF  = '/*--------------------------------*- C++ -*----------------------------------*\\\n'
headerOF += '| =========                 |                                                 |\n'
headerOF += '| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |\n'
headerOF += '|  \\    /   O peration     | Version:  2.1.x                                 |\n'
headerOF += '|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |\n'
headerOF += '|    \\/     M anipulation  |                                                 |\n'
headerOF += '\*---------------------------------------------------------------------------*/\n'
headerOF += 'FoamFile\n'
headerOF += '{\n'
headerOF += '\tversion\t\t2.0;\n'
headerOF += '\tformat\t\tascii;\n'
headerOF += '\tclass\t\tdictionary;\n'
headerOF += '\tobject\t\tprobesDict;\n'
headerOF += '}\n'
headerOF += '// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n'


probeLocationsStart  = 'probes\n'
probeLocationsStart += '\t{\n'
probeLocationsStart += '\t\ttype probes;\n'
probeLocationsStart += '\t\tfunctionObjectLibs ("libsampling.so");\n'
probeLocationsStart += '\nfields\n'
probeLocationsStart += '(\n'
probeLocationsStart += '\tp\n'
probeLocationsStart += '\tU\n'
probeLocationsStart += ');\n'
probeLocationsStart += '\noutputControl\ttimeStep;\n'
probeLocationsStart += '\n// Locations to be probed.\n'
probeLocationsStart += 'probeLocations\n'
probeLocationsStart += '(\n'

probeLocationsEnd = ');\n}\n'

finish = '\n// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n'


# write probesDict

mywfile.write(headerOF)

mywfile.write(entryFields)

mywfile.write(entryOutput)

mywfile.write(probeLocationsStart)

mywfile.write(probeLocationsData)

mywfile.write(probeLocationsEnd)

mywfile.write(finish)

mywfile.close()


