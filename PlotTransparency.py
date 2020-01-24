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

Parser.add_argument('-p',
                    action = 'store_true',
                    dest = 'isFigOut',
                    help = 'Figure file is created')

args = Parser.parse_args()

FileIN = args.FileIN
isFigOut = args.isFigOut

if(len(FileIN) <= 0):
    print 'please select input file with option -i'
    sys.exit()
    pass

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
    
    pass

#canvas
c1 = ROOT.TCanvas('c1', 'Transparency', 0, 0, 1200, 900)

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetTitleFont(132, '')
ROOT.gStyle.SetTitleFont(132, 'XYZ')
ROOT.gStyle.SetLabelFont(132, '')
ROOT.gStyle.SetLabelFont(132, 'XYZ')

c1.SetFillColor(0)
c1.SetGridx()
c1.SetGridy()

MinWave = 350.0 #nm
MaxWave = 600.0
MinTrans = 0.0 #%, relative transparency
MaxTrans = 100.0

gTransArray = []

for i in range(len(FileIN)):

    gTrans = ROOT.TGraph(len(TransArray[i][0]),
                         numpy.array(TransArray[i][0]),
                         numpy.array(TransArray[i][1]))

    gTrans.SetTitle('')
    gTrans.GetXaxis().SetTitle('Wavelength [nm]')
    gTrans.GetXaxis().SetTitleFont(132)
    gTrans.GetXaxis().SetLabelFont(132)
    gTrans.GetXaxis().SetLimits(MinWave, MaxWave)
    gTrans.GetYaxis().SetTitle('Transparency [%]')
    gTrans.GetYaxis().SetTitleFont(132)
    gTrans.GetYaxis().SetTitleOffset(1.2)
    gTrans.GetYaxis().SetLabelFont(132)
    gTrans.SetMinimum(MinTrans)
    gTrans.SetMaximum(MaxTrans)
    
    gTrans.SetLineColor(i + 2)
    gTrans.SetLineWidth(3)
    gTrans.SetMarkerStyle(8)
    gTrans.SetMarkerSize(.8)
    gTrans.SetMarkerColor(i + 2)
    
    gTransArray.append(gTrans)

    pass

gTransArray[0].Draw('apl')

for i in range(1, len(gTransArray)):
    gTransArray[i].Draw('plsame')
    pass

c1.Update()
