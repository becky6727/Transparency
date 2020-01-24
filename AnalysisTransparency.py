import os, sys, time
import numpy
import ROOT
import argparse

#options
Parser = argparse.ArgumentParser(description = 'options')

Parser.add_argument('-i',
                    dest = 'FileIN',
                    #default = None,
                    nargs = '+',
                    type = str,
                    help = 'input file')

Parser.add_argument('-wl',
                    dest = 'WL',
                    default = '450.0',
                    type = float,
                    help = 'Wavelength where you want to get the value of transparency')

args = Parser.parse_args()

FileIN = args.FileIN
WL = args.WL

if(len(FileIN) <= 0):
    print 'please select input file with option -i'
    sys.exit()
    pass

#variable for transparency data
TransArray = [[] for i in range(len(FileIN))]

isData = False

XArray = []
YArray = []

for i in range(len(FileIN)):

    #initialize
    isData = False
    XArray = []
    YArray = []
    
    for Line in open(FileIN[i]):

        #strip \n and split at \t or \s
        Line = Line.rstrip()
        Line = Line.split()

        #skip header
        if(len(Line) > 2):
            continue

        #skip blank lines
        if(len(Line) <= 0):
            continue

        #data starts after [nm, %T]
        if(Line[0] == 'nm'):
            isData = True
            continue
        
        if(isData):
            XArray.append(float(Line[0]))
            YArray.append(float(Line[1]))
            pass
        
        pass

    XArray.reverse()
    YArray.reverse()
    
    TransArray[i].append(XArray)
    TransArray[i].append(YArray)

    
    #convert array type
    TransArray[i] = numpy.array(TransArray[i])

    print '%s: Transparency = %2.2f %% at wavelength = %3.2f nm' %(FileIN[i],
                                                                   numpy.interp(WL, TransArray[i][0], TransArray[i][1]),
                                                                   WL)

    #calc attenuation length
    T = (numpy.interp(WL, TransArray[i][0], TransArray[i][1]))/100.0
    Lambda = -90.0/numpy.log(T)
    
    print '%s: Att. length = %2.2f mm at wavelength = %3.2f nm' %(FileIN[i], Lambda, WL)
    
    pass
