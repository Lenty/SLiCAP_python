#!/usr/bin/python
from SLiCAPmath import *

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
                        if self.axes[i].xScaleFactor in SCALEFACTORS.keys():
                            scaleX = 10**eval(SCALEFACTORS[self.axes[i].xScaleFactor])
                        else:
                            scaleX = 1
                        if self.axes[i].yScaleFactor in SCALEFACTORS.keys():
                            scaleY = 10**eval(SCALEFACTORS[self.axes[i].yScaleFactor])
                        else:
                            scaleY = 1
                        plt.plot(self.axes[i].traces[j].xData/scaleX, self.axes[i].traces[j].yData/scaleY, label = self.axes[i].traces[j].label, linewidth = self.axes[i].traces[j].lineWidth,
                                 color = Color, marker = Marker, markeredgecolor = MarkerColor, markersize = self.axes[i].traces[j].markerSize, markeredgewidth = 2, markerfacecolor = 'none', linestyle = self.axes[i].traces[j].lineType)
                    except:
                        print 'Error in plot data of %s.'%self.fileName
                        #return False
                    if self.axes[i].text:
                        X, Y, txt = self.axes[i].text
                        plt.text(X, Y, txt, fontsize = ini.plotFontSize)  
                    # Set default font sizes and grid
                    defaultsPlot()
        if self.save:
            try:
                plt.savefig(ini.imgPath + self.fileName + '.' + self.fileType)
                print 'Plot \"%s.%s\" saved to disk.'%(self.fileName, self.fileType)
            except:
                print 'Error: could not save the plot!'
            # ToDo save CSV all traces??
        if self.show:
            plt.show()
        plt.close(fig)
        return True

def defaultsPlot():
    """
    Applies default setting for all plots.
    """
    figures = [manager.canvas.figure for manager in plotHelp.Gcf.get_all_fig_managers()]
    for fig in figures:
        plt.tight_layout()
        for i in range(len(fig.axes)):
            fig.axes[i].title.set_fontsize(ini.plotFontSize)
            fig.axes[i].grid(b=True, which='major', color='0.5',linestyle='-')
            fig.axes[i].grid(b=True, which='minor', color='0.5',linestyle=':')
            t = fig.axes[i].xaxis.get_offset_text()
            t.set_fontsize(ini.plotFontSize)
            t = fig.axes[i].yaxis.get_offset_text()
            t.set_fontsize(ini.plotFontSize)
            try:
                fig.axes[i].xaxis.label.set_fontsize(ini.plotFontSize)
                fig.axes[i].yaxis.label.set_fontsize(ini.plotFontSize)
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
                    t.set_fontsize(ini.plotFontSize)
            except:
                pass
            for tick in fig.axes[i].xaxis.get_major_ticks():
                tick.label.set_fontsize(ini.plotFontSize)
            for tick in fig.axes[i].yaxis.get_major_ticks():
                tick.label.set_fontsize(ini.plotFontSize)
                
def plotdBmag(fileName, title, result, fStart, fStop, fNum, xscale = '', yscale = '', show = True, save = True):
    """
    """
    fig = figure(title)
    fig.fileName = fileName
    fig.show = show
    fig.save = save
    dBmag = axis(title)
    dBmag.xScaleFactor = xscale
    dBmag.yScaleFactor = yscale
    dBmag.xScale = 'log'
    dBmag.yScale = 'lin'
    dBmag.xLabel = 'frequency [' + xscale + 'Hz]'
    dBmag.yLabel = 'mag [' + yscale + 'dB]'
    if result.dataType == 'numer':
        yData = result.numer
    if result.dataType == 'denom':
        yData = result.denom
    if result.dataType == 'laplace':
        yData = result.laplace
    else:
        print "Error: wrong data type '%s' for 'plotdBmag()'."%(result.dataType)
        return fig
    yData = yData.subs(LAPLACE, 2*sp.pi*sp.I*FREQUENCY)
    func = sp.lambdify(FREQUENCY, 20*sp.log(abs(yData),10))
    if not result.step:
        x = np.geomspace(fStart, fStop, fNum)
        y = func(x)
        dBmagTrace = trace([x, y])
        dBmagTrace.color = ini.gainColors[result.gainType]
        dBmagTrace.label = result.gainType
        dBmag.traces = [dBmagTrace]
    else:
        pass
    fig.axes = [[dBmag]]
    fig.plot()
    return fig
                
def plotMag(fileName, title, result, fStart, fStop, fNum, xscale = '', yscale = '', yunits = '', show = True, save = True):
    """
    """
    fig = figure(title)
    fig.fileName = fileName
    fig.show = show
    fig.save = save
    mag = axis(title)
    mag.xScaleFactor = xscale
    mag.yScaleFactor = yscale
    mag.xScale = 'log'
    mag.yScale = 'log'
    mag.xLabel = 'frequency [' + xscale + 'Hz]'
    mag.yLabel = 'mag [' + yscale + yunits +']'
    if result.dataType == 'numer':
        yData = result.numer
    if result.dataType == 'denom':
        yData = result.denom
    if result.dataType == 'laplace':
        yData = result.laplace
    else:
        print "Error: wrong data type '%s' for 'plotMag()'."%(result.dataType)
        return fig
    yData = yData.subs(LAPLACE, 2*sp.pi*sp.I*FREQUENCY)
    func = sp.lambdify(FREQUENCY, abs(yData))
    if not result.step:
        x = np.geomspace(fStart, fStop, fNum)
        y = func(x)
        magTrace = trace([x, y])
        magTrace.color = ini.gainColors[result.gainType]
        magTrace.label = result.gainType
        mag.traces = [magTrace]
    else:
        pass
    fig.axes = [[mag]]
    fig.plot()
    return fig
                
def plotPhase(fileName, title, result, fStart, fStop, fNum, xscale = '', yscale = '', show = True, save = True):
    """
    """
    fig = figure(title)
    fig.fileName = fileName
    fig.show = show
    fig.save = save
    phase = axis(title)
    phase.xScaleFactor = xscale
    phase.yScaleFactor = yscale
    phase.xScale = 'log'
    phase.yScale = 'lin'
    phase.xLabel = 'frequency [' + xscale + 'Hz]'
    phase.yLabel = 'phase [' + yscale + 'deg]'
    if result.dataType == 'numer':
        yData = result.numer
    if result.dataType == 'denom':
        yData = result.denom
    if result.dataType == 'laplace':
        yData = result.laplace
    else:
        print "Error: wrong data type '%s' for 'plotPhase()'."%(result.dataType)
        return fig
    yData = yData.subs(LAPLACE, 2*sp.pi*sp.I*FREQUENCY)
    func = sp.lambdify(FREQUENCY, yData)
    if not result.step:
        x = np.geomspace(fStart, fStop, fNum)
        y = 180*np.unwrap(np.angle(func(x)))/np.pi
        phaseTrace = trace([x, y])
        phaseTrace.color = ini.gainColors[result.gainType]
        phaseTrace.label = result.gainType
        phase.traces = [phaseTrace]
    else:
        pass
    fig.axes = [[phase]]
    fig.plot()
    return fig
                
def plotDelay(fileName, title, result, fStart, fStop, fNum, xscale = '', yscale = '', show = True, save = True):
    """
    """
    fig = figure(title)
    fig.fileName = fileName
    fig.show = show
    fig.save = save
    delay = axis(title)
    delay.xScaleFactor = xscale
    delay.yScaleFactor = yscale
    delay.xScale = 'log'
    delay.yScale = 'lin'
    delay.xLabel = 'frequency [' + xscale + 'Hz]'
    delay.yLabel = 'delay [' + yscale + 's]'
    if result.dataType == 'numer':
        yData = result.numer
    if result.dataType == 'denom':
        yData = result.denom
    if result.dataType == 'laplace':
        yData = result.laplace
    else:
        print "Error: wrong data type '%s' for 'plotPhase()'."%(result.dataType)
        return fig
    yData = yData.subs(LAPLACE, 2*sp.pi*sp.I*FREQUENCY)
    func = sp.lambdify(FREQUENCY, yData)
    if not result.step:
        x = np.geomspace(fStart, fStop, fNum)
        y = -np.diff(np.unwrap(np.angle(func(x))))/np.diff(x)/(2*np.pi)
        # y one point less than x after differentiation so remove last point x
        x = x[0:-1] 
        delayTrace = trace([x, y])
        delayTrace.color = ini.gainColors[result.gainType]
        delayTrace.label = result.gainType
        delay.traces = [delayTrace]
    else:
        pass
    fig.axes = [[delay]]
    fig.plot()
    return fig
               
def plotTime(fileName, title, result, tStart, tStop, tNum, xscale = '', yscale = '', yunits = '', show = True, save = True):
    """
    """
    fig = figure(title)
    fig.fileName = fileName
    fig.show = show
    fig.save = save
    time = axis(title)
    time.xScaleFactor = xscale
    time.yScaleFactor = yscale
    time.xScale = 'lin'
    time.yScale = 'lin'
    time.xLabel = 'time [' + xscale + 's]'
    time.yLabel = '[' + yscale + yunits + ']'
    if result.dataType == 'time':
        yData = result.time
    if result.dataType == 'impulse':
        yData = result.impulse
    if result.dataType == 'step':
        yData = result.stepResp
    else:
        print "Error: wrong data type '%s' for 'plotTime()'."%(result.dataType)
        return fig
    func = sp.lambdify(sp.Symbol('t', real=True), yData)
    if not result.step:
        x = np.linspace(tStart, tStop, tNum)
        y = np.real(func(x))
        timeTrace = trace([x, y])
        timeTrace.color = ini.gainColors[result.gainType]
        timeTrace.label = result.gainType
        time.traces = [timeTrace]
    else:
        pass
    fig.axes = [[time]]
    fig.plot()
    return fig

def plotPZ(fileName, title, result, xmin = None, xmax = None, ymin = None, ymax = None, xscale = '', yscale = '', show = True, save = True):
    """
    """
    fig = figure(title)
    fig.fileName = fileName
    fig.show = show
    fig.save = save
    fig.axisHeight = fig.axisWidth
    pz = axis(title)
    pz.xScaleFactor = xscale
    pz.yScaleFactor = yscale
    pz.xScale = 'lin'
    pz.yScale = 'lin'
    pz.xLabel = 'Re [' + xscale + 'Hz]'
    pz.yLabel = 'Im [' + yscale + 'Hz]'
    pzTraces = []
    if xmin != None and xmax != None:
        pz.xLim = [checkNumber(xmin), checkNumber(xmax)]
    if ymin != None and xmax != None:
        pz.yLim = [checkNumber(ymin), checkNumber(ymax)]
    if result.dataType == 'poles' or result.dataType == 'pz':
        polesTrace = trace([np.real(result.poles)/2/np.pi, np.imag(result.poles)/2/np.pi])
        polesTrace.markerColor = ini.gainColors[result.gainType]
        polesTrace.color = ''
        polesTrace.marker = 'x'
        polesTrace.lineWidth = '0'
        polesTrace.label = 'poles ' + result.gainType
        pzTraces.append(polesTrace)
    if result.dataType == 'zeros' or result.dataType == 'pz':
        zerosTrace = trace([np.real(result.zeros)/2/np.pi, np.imag(result.zeros)/2/np.pi])
        zerosTrace.color = ''
        zerosTrace.markerColor = ini.gainColors[result.gainType]
        zerosTrace.marker = 'o'
        zerosTrace.lineWidth = '0'
        zerosTrace.label = 'zeros ' + result.gainType
        pzTraces.append(zerosTrace)
    if result.dataType != 'poles' and result.dataType != 'zeros' and result.dataType != 'pz':
        print "Error: wrong data type '%s' for 'plotTime()'."%(result.dataType)
        return fig
    pz.traces = pzTraces
    fig.axes = [[pz]]
    fig.plot()
    return fig

if __name__=='__main__':
    x = np.linspace(0, 2*np.pi, endpoint = True)
    y1 = np.sin(x)
    y2 = np.cos(x)
    sine = trace([x, y1])
    sine.label = 'sine'
    sine.color = ''
    sine.lineWidth = '0'
    sine.marker = 'o'
    sine.markerColor = 'r'
    cosine = trace([x, y2])
    cosine.label = 'cosine'
    cosine.color = ''
    cosine.marker = 'x'
    cosine.markerColor = 'b'
    sincos = axis('sine and cosine')
    sincos.xScale = 'lin'
    sincos.yScale = 'lin'
    sincos.traces = [sine, cosine]
    testFig = figure('testFig')
    testFig.axes = [[sincos, ""],["",sincos]]
    testFig.show = True
    testFig.plot()
    plt.show()
    