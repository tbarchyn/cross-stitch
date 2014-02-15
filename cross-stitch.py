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
import matplotlib.pyplot
import wx

class CrossStitch:

    def __init__(self):
        self.img = numpy.zeros(3)

    def read_image(self, infile):
        try:
            self.img = scipy.ndimage.imread(infile)
        except IOError:
            sys.stderr.write('could not open input file "' + infile + '"\n')

        self.orig_img = self.img.copy()

    def down_sample(self, width):
        hw_ratio = float(self.img.shape[0])/self.img.shape[1]
        size = (int(round(hw_ratio*width)), width)
        self.img = scipy.misc.imresize(self.img, size)

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
        imgplot = matplotlib.pyplot.imshow(self.img, interpolation='nearest')
        matplotlib.pyplot.grid(True)
        matplotlib.pyplot.savefig(filename)

    def image(self):
        return self.img


def ask(parent=None, message=''):
    app = wx.App()
    dlg = wx.TextEntryDialog(parent, message)
    dlg.ShowModal()
    result = dlg.GetValue()
    dlg.Destroy()
    app.MainLoop()
    return result

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
        self.SetTitle('Cross Stitch')
        self.Centre()
        self.Show(True)

    def InitMenu(self):

        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        fitem = fileMenu.Append(wx.ID_OPEN, 'Open image', 'Open image')
        self.Bind(wx.EVT_MENU, self.OnOpen, fitem)
        fitem = fileMenu.Append(wx.ID_SAVE, 'Save image', 'Save image')
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

        helpMenu = wx.Menu()
        fitem = helpMenu.Append(wx.ID_ABOUT, 'About', 'About')
        self.Bind(wx.EVT_MENU, self.OnAbout, fitem)
        menubar.Append(helpMenu, '&Help')

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

        if self.contentNotSaved:
            if wx.MessageBox('Current image is not saved! Proceed?',
                    'Please confirm', wx.ICON_QUESTION | wx.YES_NO, self) == \
                    wx.NO:
                        return
        self.Close()

    def OnOpen(self, event):
        if self.contentNotSaved:
            if wx.MessageBox('Current image is not saved! Proceed?',
                    'Please confirm', wx.ICON_QUESTION | wx.YES_NO, self) == \
                    wx.NO:
                        return
        
        self.dirname = ''
        openFileDialog = wx.FileDialog(self, 'Open image file', self.dirname,
                '', 'Image files (*.jpg, *.jpeg, *.png, *.gif, *.bmp)|'
                + '*.jpg;*.jpeg;*.png;*.gif;*.bmp',
                wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_OK:
            self.filename = openFileDialog.GetFilename()
            self.dirname = openFileDialog.GetDirectory()
            self.cs.read_image(openFileDialog.GetPath())
            self.DrawPreview()
        openFileDialog.Destroy()

    def OnSave(self, event):
        saveFileDialog = wx.FileDialog(self, 'Save image file', self.dirname,
                '', 'PNG files (*.png)|*.png|'
                + 'JPEG files (*.jpg,*.jpeg)|*.jpg*.jpeg|'
                + 'GIF files (*.gif)|*.gif|'
                + 'BMP files (*.bmp)|*.bmp',
                wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return

        self.cs.save_image(saveFileDialog.GetPath())
        self.contentNotSaved = False

    def OnDownSample(self, event):
        dlg = wx.TextEntryDialog(None, 'Enter new width', defaultValue='50')
        ret = dlg.ShowModal()
        if ret == wx.ID_OK:
            width = int(dlg.GetValue())
            self.cs.down_sample(int(width))
            self.contentNotSaved = True
            self.DrawPreview()

    def OnLimitColors(self, event):
        dlg = wx.TextEntryDialog(None, 'Enter the number of colors to include',
                defaultValue='16')
        ret = dlg.ShowModal()
        if ret == wx.ID_OK:
            self.cs.limit_colors(int(dlg.GetValue()))
            self.contentNotSaved = True
            self.DrawPreview()

    def OnAbout(self, event):

        description = '''Cross Stitch is a raster pattern generator for Linux,
Mac OS X, and Windows. It features simple downscaling to coarsen the image
resolution, and color depth reduction features.'''

        license = '''Cross Stitch is free software; you can redistribute it
and/or modify it under the terms of the GNU General Public License as published
by the Free Software Foundation; either version 3 of the License, or (at your
option) any later version.

Cross Stitch is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.
See the GNU General Public License for more details. You should have recieved a
copy of the GNU General Public License along with Cross Stitch; if not, write to
the Free Software Foundation, Inc., 59 Temple Palace, Suite 330, Boston, MA
02111-1307  USA'''

        info = wx.AboutDialogInfo()

        info.SetIcon(wx.Icon('icon.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Cross Stitch')
        info.SetVersion('1.01')
        info.SetDescription(description)
        info.SetCopyright('(C) 2014 Anders Damsgaard')
        info.SetWebSite('https://github.com/anders-dc/cross-stitch')
        info.SetLicense(license)
        info.AddDeveloper('Anders Damsgaard')
        info.AddDocWriter('Anders Damsgaard')
        info.AddArtist('Anders Damsgaard')

        wx.AboutBox(info)



def main():
    app = wx.App()
    MainScreen(None, title='Cross Stitch')
    app.MainLoop()

if __name__ == '__main__':
    main()
