#!/usr/bin/python
from matplotlib import pyplot as plt
import matplotlib._pylab_helpers as plotHelp
import numpy as np
import SLiCAPini as ini
class trace(object):
    def __init__(self, traceData):
        """
        """
        self.xData          = np.array(traceData[0])
        self.yData          = np.array(traceData[1])
        try:
            if len(self.xData) != len(self.yData):
                print 'Error in plot data.'
        except:
            pass
        self.xName          = 'x'           # Header for table
        self.yName          = 'y'           # Header for table
        self.label          = ''            # trace label will be displayed in legend box
        self.color          = False         # trace color
        self.marker         = False         # trace marker
        self.markerColor    = False         # trace marker color
        self.markerSize     = 7             # trace marker size
        self.lineWidth      = 2
        self.lineType       = '-'
        self.table          = False
    
    def makeTable(self):
        """
        Returns a table with all axis data in CSV format.
        """
        out = str(self.xName) + ',' + str(self.yName) + '\n'
        for i in range(len(self.xData)):
            out += '%20.12e,'%(self.xData[i]) + '%20.12e'%(self.yData[i]) + '\n'
        self.table = out
        return
        
class axis(object):
    def __init__(self, title):
        self.title          = title         # Title of the axis, will be placed on top of the axis
        self.xLabel         = False         # Label for the x-axis, e.g. 'frequency [Hz]'
        self.yLabel         = False         # Label for the y-axis, e.q. 'Voltage [V]'
        self.xScale         = 'linear'      # Scale for the x-axis can be 'linear' or 'log'
        self.yScale         = 'linear'      # Scale for the y-axis can be 'linear' or 'log'
        self.xLim           = []            # List: [<xMin>, <xMax>], limits for the x-scale
        self.yLim           = []            # List: [<yMin>, <yMax>], limits for the y-scale
        self.traces         = []            # List: [<trace1>(,<trace2>)...(,<traceN>)]
        self.text           = False         # Text and relative plot position
        self.polar          = False         # True if a polar plot is used. In that case: xLists = [<list of radians>]
        self.xScaleFactor   = ' '           # Scale factor (engineering notation, e.g. M for 1E6) for x-axis
        self.yScaleFactor   = ' '           # Scale factor (engineering notation, e.g. M for 1E6) for y-axis
        return

class figure(object):
    def __init__(self, fileName):
        self.fileName       = fileName              # Name of the file for saving the figure
        self.fileType       = ini.figureFileType    # Graphic file type for saving the figure
        self.axisHeight     = ini.figureAxisHeight  # Height of single axis
        self.axisWidth      = ini.figureAxisWidth   # Width of single axis
        self.axes           = []
        self.show           = False
        self.save           = False
        
    def plot(self):                                 # <figure name>.plot()
                                                    # plots m x n axes in the figure
        axes = np.array(self.axes)
        try:
            rows,cols = axes.shape
        except:
            print 'Argument of the <figure>.plot() method must be a list of lists or a two-dimensional array.'
            return False
        self.axes = []
        # Make a single list of plots to be plotted left -> right, then top -> bottom
        for i in range(rows):
            for j in range(cols):
                self.axes.append(axes[i][j])
        if not self.axes:
            print 'Error: no plot data available; plotting skipped.'
            return False
        # Define the matplotlib figure object
        fig = plt.figure(figsize = (self.axisWidth*cols, rows*self.axisHeight))
        # Make all the axis with their plots
        for i in range(len(self.axes)):
            if self.axes[i] != "":
                ax = fig.add_subplot(rows, cols, i + 1, polar = self.axes[i].polar)
                if self.axes[i].xLabel:
                    try:
                        ax.set_xlabel(self.axes[i].xLabel)
                    except:
                        pass
                if self.axes[i].yLabel:        
                    try:
                        ax.set_ylabel(self.axes[i].yLabel)
                    except:
                        pass
                if self.axes[i].title:
                    try:
                        ax.set_title(self.axes[i].title)
                    except:
                        pass
                if self.axes[i].xScale:
                    try:
                         ax.set_xscale(self.axes[i].xScale)
                    except:
                        pass
                if self.axes[i].yScale:
                    try:
                         ax.set_yscale(self.axes[i].yScale)
                    except:
                        pass
                if len(self.axes[i].xLim) == 2:
                    try:
                        ax.set_xlim(self.axes[i].xLim[0], self.axes[i].xLim[1])
                    except:
                        pass
                if len(self.axes[i].yLim) == 2:
                    try:
                        ax.set_ylim(self.axes[i].yLim[0], self.axes[i].yLim[1])
                    except:
                        pass
                if len(self.axes[i].traces) == 0:
                    print 'Error: Missing trace data for plotting!'
                    return False

                for j in range(len(self.axes[i].traces)):
                    if self.axes[i].traces[j].color:
                        Color = self.axes[i].traces[j].color
                    else:
                        Color = ini.defaultColors[j % len(ini.defaultColors)]
                    if self.axes[i].traces[j].marker:
                        Marker = self.axes[i].traces[j].marker
                    else:
                        Marker = ini.defaultMarkers[j % len(ini.defaultMarkers)]
                    if self.axes[i].traces[j].markerColor:
                        MarkerColor = self.axes[i].traces[j].markerColor
                    else:
                        MarkerColor = ini.defaultColors[j % len(ini.defaultColors)]
                    try:
                        if self.axes[i].xScaleFactor in ini.SCALEFACTORS.keys():
                            scaleX = 10**eval(ini.SCALEFACTORS[self.axes[i].xScaleFactor])
                        else:
                            scaleX = 1
                        if self.axes[i].yScaleFactor in ini.SCALEFACTORS.keys():
                            scaleY = 10**eval(ini.SCALEFACTORS[self.axes[i].yScaleFactor])
                        else:
                            scaleY = 1
                        plt.plot(self.axes[i].traces[j].xData/scaleX, self.axes[i].traces[j].yData/scaleY, label = self.axes[i].traces[j].label, linewidth = self.axes[i].traces[j].lineWidth,
                                 color = Color, marker = Marker, markeredgecolor = MarkerColor, markersize = self.axes[i].traces[j].markerSize, markeredgewidth = 2, markerfacecolor = 'none', linestyle = self.axes[i].traces[j].lineType)
                    except:
                        print 'Error in plot data of %s.'%self.fileName
                        #return False
                    if self.axes[i].text:
                        X, Y, txt = self.axes[i].text
                        plt.text(X, Y, txt, fontsize = 11)  
                    # Set default font sizes and grid
                    defaultsPlot()
        if self.save:
            try:
                plt.savefig(self.fileName + '.' + self.fileType)
                print '\tPlot \"%s.%s\" saved to disk.'%(self.fileName, self.fileType)
            except:
                print 'Error: could not save the plot!'
        if self.show:
            plt.show()
        return True

def defaultsPlot():
    """
    Applies default setting for all plots.
    """
    figures = [manager.canvas.figure for manager in plotHelp.Gcf.get_all_fig_managers()]
    for fig in figures:
        plt.tight_layout()
        for i in range(len(fig.axes)):
            fig.axes[i].title.set_fontsize(11)
            fig.axes[i].grid(b=True, which='major', color='0.5',linestyle='-')
            fig.axes[i].grid(b=True, which='minor', color='0.5',linestyle=':')
            t = fig.axes[i].xaxis.get_offset_text()
            t.set_fontsize(9)
            t = fig.axes[i].yaxis.get_offset_text()
            t.set_fontsize(9)
            try:
                fig.axes[i].xaxis.label.set_fontsize(11)
                fig.axes[i].yaxis.label.set_fontsize(11)
            except:
                pass
            try:
                leg = fig.axes[i].legend(loc = ini.legendLoc,
                                borderpad = 0.2,
                                labelspacing = 0,
                                handletextpad = 0.2,
                                handlelength = 1,
                                scatterpoints = 1,
                                numpoints = 1)
                for t in leg.get_texts():
                    t.set_fontsize(9)
            except:
                pass
            for tick in fig.axes[i].xaxis.get_major_ticks():
                tick.label.set_fontsize(9)
            for tick in fig.axes[i].yaxis.get_major_ticks():
                tick.label.set_fontsize(9)
        
if __name__=='__main__':
    x = np.linspace(0,2*np.pi, endpoint = True)
    y1 = np.sin(x)
    y2 = np.cos(x)
    sine = trace([x, y1])
    sine.label = 'sine'
    sine.color = 'b'
    sine.marker = 'o'
    sine.markerColor = 'r'
    cosine = trace([x, y2])
    cosine.label = 'cosine'
    cosine.color = 'k'
    cosine.marker = 'x'
    cosine.markerColor = 'b'
    sincos = axis('sine and cosine')
    sincos.xScale = 'lin'
    sincos.yScale = 'lin'
    sincos.traces = [sine, cosine]
    testFig = figure('testFig')
    testFig.axes = [[sincos, ""],["",sincos]]
    testFig.plot()
    plt.show()
    
