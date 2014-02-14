#!/usr/bin/env python

import sys
import argparse
import scipy.ndimage
import scipy.misc
import scipy.cluster
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import wx

class CrossStitch:

    def __init__(self):
        pass

    def read_image(self, infile):
        try:
            self.img = scipy.ndimage.imread(infile)
        except IOError:
            sys.stderr.write('could not open input file "' + infile + '"\n')

    def down_sample(self, width):
        hw_ratio = float(self.img.shape[0])/self.img.shape[1]
        size = (int(round(hw_ratio*width)), width)
        self.img = scipy.misc.imresize(self.img, size)
        self.orig_img = self.img.copy()

    def limit_colors(self, ncolors):
        ar = self.img.reshape(scipy.product(self.img.shape[:2]),\
                self.img.shape[2])
        self.colors, dist = scipy.cluster.vq.kmeans(ar, ncolors)
        tmp = ar.copy()
        vecs, dist = scipy.cluster.vq.vq(ar, self.colors)
        for i, color in enumerate(self.colors):
            tmp[scipy.r_[scipy.where(vecs == i)],:] = color
        self.img = tmp.reshape(self.img.shape[0], self.img.shape[1], 3)

    def save_image(self, filename):
        fig = plt.figure()
        imgplot = plt.imshow(self.img)
        imgplot.set_interpolation('nearest')
        plt.grid()
        plt.savefig(filename)


class MainScreen(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(MainScreen, self).__init__(*args, **kwargs)
        self.InitUI()
        self.cs = CrossStitch()

    def InitUI(self):

        self.InitMenu()
        #self.InitToolbar()

        self.SetSize((600, 400))
        self.SetTitle('Main menu')
        self.Centre()
        self.Show(True)

    def InitMenu(self):

        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        fitem = fileMenu.Append(wx.ID_OPEN, 'Open', 'Open image')
        self.Bind(wx.EVT_MENU, self.OnOpen, fitem)
        fitem = fileMenu.Append(wx.ID_SAVE, 'Save', 'Save image')
        self.Bind(wx.EVT_MENU, self.OnSave, fitem)
        fileMenu.AppendSeparator()
        fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)
        menubar.Append(fileMenu, '&File')

        processingMenu = wx.Menu()
        fitem = processingMenu.Append(wx.ID_ANY, 'Down sample',
                'Down sample image')
        self.Bind(wx.EVT_MENU, self.OnDownSample, fitem)
        fitem = processingMenu.Append(wx.ID_ANY, 'Reduce number of colors',
                'Reduce number of colors in image')
        self.Bind(wx.EVT_MENU, self.OnLimitColors, fitem)

        menubar.Append(processingMenu, '&Image processing')


        self.SetMenuBar(menubar)

    def InitToolbar(self):

        toolbar = self.CreateToolBar()
        qtool = toolbar.AddLabelTool(wx.ID_EXIT, 'Quit', wx.Bitmap('textit.png'))
        self.Bind(wx.EVT_TOOL, self.OnQuit, qtool)

        toolbar.Realize()
        


    def OnQuit(self, e):
        self.Close()

    def OnOpen(self, e):
        self.cs.read_image("fiskeren.jpg")

    def OnSave(self, e):
        self.cs.save_image("fisker-pattern.png")

    def OnDownSample(self, e):
        self.cs.down_sample(80)

    def OnLimitColors(self, e):
        self.cs.limit_colors(16)




def main():
    app = wx.App()
    MainScreen(None, title='Cross Stitch')
    app.MainLoop()

if __name__ == '__main__':
    main()
