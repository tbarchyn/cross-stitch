#!/usr/bin/env python

import sys, os
import argparse
import scipy.ndimage
import scipy.misc
import scipy.cluster
import numpy
import matplotlib
matplotlib.use('WXAgg')
import matplotlib.figure
import matplotlib.backends
import matplotlib.backends.backend_wxagg
#import matplotlib.pyplot as plt
import wx

class CrossStitch:

    def __init__(self):
        self.img = numpy.zeros(3)

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
        fig = matplotlib.pyplot.figure()
        imgplot = matplotlib.pyplot.imshow(self.img)
        imgplot.set_interpolation('nearest')
        matplotlib.pyplot.grid()
        matplotlib.pyplot.savefig(filename)

    def image(self):
        return self.img

class MainScreen(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(MainScreen, self).__init__(*args, **kwargs)
        self.cs = CrossStitch()
        self.InitUI()
        self.contentNotSaved = False

    def InitUI(self):

        self.InitMenu()
        #self.InitToolbar()
        self.InitPreview()

        self.SetSize((600, 600))
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
        qtool = toolbar.AddLabelTool(wx.ID_EXIT, 'Quit',
                wx.Bitmap('textit.png'))
        self.Bind(wx.EVT_TOOL, self.OnQuit, qtool)

        toolbar.Realize()

    def InitPreview(self):
        self.figure = matplotlib.figure.Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = matplotlib.backends.backend_wxagg.FigureCanvasWxAgg(self,
                -1, self.figure)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

    def DrawPreview(self):
        self.axes.grid(True)
        self.axes.imshow(self.cs.image(), interpolation='nearest')
        self.canvas.draw()

    def OnQuit(self, event):
        self.Close()

    def OnOpen(self, event):
        if self.contentNotSaved:
            if wx.MessageBox('Current image is not saved! Proceed?',
                    'Please confirm', wx.ICON_QUESTION | wx.YES_NO, self) == \
                    wx.NO:
                        return
        
        self.dirname = ''
        openFileDialog = wx.FileDialog(self, 'Open image file', self.dirname,
                '', 'JEPG files (*.jpg)|*.jpg',
                wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_OK:
            self.filename = openFileDialog.GetFilename()
            self.dirname = openFileDialog.GetDirectory()
            self.cs.read_image(openFileDialog.GetPath())
            self.DrawPreview()
        openFileDialog.Destroy()

    def OnSave(self, event):
        self.cs.save_image("fisker-pattern.png")
        self.contentNotSaved = False

    def OnDownSample(self, event):
        self.cs.down_sample(80)
        self.contentNotSaved = True
        self.DrawPreview()

    def OnLimitColors(self, event):
        self.cs.limit_colors(16)
        self.contentNotSaved = True
        self.DrawPreview()




def main():
    app = wx.App()
    MainScreen(None, title='Cross Stitch')
    app.MainLoop()

if __name__ == '__main__':
    main()
