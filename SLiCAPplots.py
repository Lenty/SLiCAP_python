#!/usr/bin/python
from SLiCAPpythonMaxima import *

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
        self.markerFaceColor = 'none'        # trace marker face color
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
        self.fileType       = ini.figureFileType    # Graphic file type for saving the figure
        self.axisHeight     = ini.figureAxisHeight  # Height of single axis
        self.axisWidth      = ini.figureAxisWidth   # Width of single axis
        self.axes           = []
        self.show           = False
        self.fileName       = fileName + '.' + ini.figureFileType
        
    def plot(self):                                 # <figure name>.plot()
                                                    # plots m x n axes in the figure
        axes = np.array(self.axes)
        try:
            rows, cols = axes.shape
        except:
            print 'Attribute of <figure>.axes must be a list of lists or a two-dimensional array.'
            return False
        axesList = []
        # Make a single list of plots to be plotted left -> right, then top -> bottom
        for i in range(rows):
            for j in range(cols):
                axesList.append(axes[i][j])
        if len(axesList) == 0:
            print 'Error: no plot data available; plotting skipped.'
            return False
        # Define the matplotlib figure object
        fig = plt.figure(figsize = (self.axisWidth*cols, rows*self.axisHeight))
        # Make all the axis with their plots
        for i in range(len(axesList)):
            if axesList[i] != "":
                ax = fig.add_subplot(rows, cols, i + 1, polar = axesList[i].polar)
                if axesList[i].xLabel:
                    try:
                        ax.set_xlabel(axesList[i].xLabel)
                    except:
                        pass
                if axesList[i].yLabel:        
                    try:
                        ax.set_ylabel(axesList[i].yLabel)
                    except:
                        pass
                if axesList[i].title:
                    try:
                        ax.set_title(axesList[i].title)
                    except:
                        pass
                if axesList[i].xScale:
                    try:
                         ax.set_xscale(axesList[i].xScale)
                    except:
                        pass
                if axesList[i].yScale:
                    try:
                         ax.set_yscale(axesList[i].yScale)
                    except:
                        pass
                if len(axesList[i].xLim) == 2:
                    try:
                        ax.set_xlim(axesList[i].xLim[0], axesList[i].xLim[1])
                    except:
                        pass
                if len(axesList[i].yLim) == 2:
                    try:
                        ax.set_ylim(axesList[i].yLim[0], axesList[i].yLim[1])
                    except:
                        pass
                if len(axesList[i].traces) == 0:
                    print 'Error: Missing trace data for plotting!'
                    return False

                for j in range(len(axesList[i].traces)):
                    if axesList[i].traces[j].color:
                        Color = axesList[i].traces[j].color
                    else:
                        Color = ini.defaultColors[j % len(ini.defaultColors)]
                    if axesList[i].traces[j].marker:
                        Marker = axesList[i].traces[j].marker
                    else:
                        Marker = ini.defaultMarkers[j % len(ini.defaultMarkers)]
                    if axesList[i].traces[j].markerColor:
                        MarkerColor = axesList[i].traces[j].markerColor
                    else:
                        MarkerColor = ini.defaultColors[j % len(ini.defaultColors)]
                    try:
                        if axesList[i].xScaleFactor in SCALEFACTORS.keys():
                            scaleX = 10**eval(SCALEFACTORS[axesList[i].xScaleFactor])
                        else:
                            scaleX = 1
                        if axesList[i].yScaleFactor in SCALEFACTORS.keys():
                            scaleY = 10**eval(SCALEFACTORS[axesList[i].yScaleFactor])
                        else:
                            scaleY = 1
                        plt.plot(axesList[i].traces[j].xData/scaleX, axesList[i].traces[j].yData/scaleY, label = axesList[i].traces[j].label, linewidth = axesList[i].traces[j].lineWidth,
                                 color = Color, marker = Marker, markeredgecolor = MarkerColor, markersize = axesList[i].traces[j].markerSize, markeredgewidth = 2, markerfacecolor = axesList[i].traces[j].markerFaceColor, linestyle = axesList[i].traces[j].lineType)
                    except:
                        print 'Error in plot data of %s.'%self.fileName
                        #return False
                    if axesList[i].text:
                        X, Y, txt = axesList[i].text
                        plt.text(X, Y, txt, fontsize = ini.plotFontSize)  
                    # Set default font sizes and grid
                    defaultsPlot()
        plt.savefig(ini.imgPath + self.fileName)
        if self.show:
            plt.show()
        plt.close(fig)
        return
        
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

def plotdBmag(fileName, title, results, fStart, fStop, fNum, xscale = '', yscale = '', show = False):
    """
    """
    fig = figure(fileName)
    fig.show = show
    dBmag = axis(title)
    dBmag.xScaleFactor = xscale
    dBmag.yScaleFactor = yscale
    dBmag.xScale = 'log'
    dBmag.yScale = 'lin'
    if ini.Hz == True:
        dBmag.xLabel = 'frequency [' + xscale + 'Hz]'
    else:
        dBmag.xLabel = 'frequency [' + xscale + 'rad/s]'
    dBmag.yLabel = 'magnitude [' + yscale + 'dB]'
    try:
        xScaleFactor = 10**int(SCALEFACTORS[xscale])
    except:
        xScaleFactor = 1.
    x = np.geomspace(checkNumber(fStart)*xScaleFactor, checkNumber(fStop)*xScaleFactor, checkNumber(fNum))
    dBmag.traces = []
    if type(results) == type(allResults()):
        results = [results]
    colNum = 0
    numColors = len(ini.defaultColors)
    for result in results:
        if result.dataType == 'numer':
            yData = result.numer
            yLabel = 'numer: '
        if result.dataType == 'denom':
            yData = result.denom
            yLabel = 'denom: '
        if result.dataType == 'laplace':
            yData = result.laplace
            yLabel = ''
        else:
            print "Error: wrong data type '%s' for 'plotdBmag()'."%(result.dataType)
            return fig
        if not result.step:
            if ini.Hz == True:
                yData = yData.xreplace({ini.Laplace: 2*sp.pi*sp.I*ini.frequency})
                func = sp.lambdify(ini.frequency, 20*sp.log(abs(yData),10))
            else:
                yData = yData.xreplace({ini.Laplace: sp.I*ini.frequency})
                func = sp.lambdify(ini.frequency, 20*sp.log(abs(yData),10))
            y = [func(x[j]) for j in range(len(x))]
            dBmagTrace = trace([x, y])
            try:
                dBmagTrace.color = ini.gainColors[result.gainType]
            except:
                dBmagTrace.color = ini.defaultColors[colNum % numColors]
                magTrace.color = ini.defaultColors[colNum % numColors]
            if result.gainType == 'vi':
                yLabel += '$' + sp.latex(sp.Symbol(result.detLabel)) + '$'
            else:
                yLabel += result.gainType
            dBmagTrace.label = yLabel
            dBmag.traces.append(dBmagTrace)
        elif type(yData) == list:
            if result.gainType == 'vi':
                yLabel += '$' + sp.latex(sp.Symbol(result.detLabel)) + '$'
            else:
                yLabel += result.gainType
            for i in range(len(yData)):
                if ini.Hz == True:
                    y = yData[i].xreplace({ini.Laplace: 2*sp.pi*sp.I*ini.frequency})
                    func = sp.lambdify(ini.frequency, 20*sp.log(abs(y),10))
                else:
                    y = yData[i].xreplace({ini.Laplace: sp.I*ini.frequency})
                    func = sp.lambdify(ini.frequency, 20*sp.log(abs(y),10))
                y = [func(x[j]) for j in range(len(x))]
                dBmagTrace = trace([x, y])
                dBmagTrace.color = ini.defaultColors[i % numColors]
                dBmagTrace.label = result.gainType
                dBmagTrace.label = yLabel
                if result.stepMethod == 'array':
                    dBmagTrace.label += ', run: %s'%(i+1)
                else:
                    dBmagTrace.label += ', %s = %8.1e'%(result.stepVar, result.stepList[i])
                dBmag.traces.append(dBmagTrace)   
        colNum += 1
    fig.axes = [[dBmag]]
    fig.plot()
    return fig
   
def plotMag(fileName, title, results, fStart, fStop, fNum, xscale = '', yscale = '', yunits = '', show = False):
    """
    """
    fig = figure(fileName)
    fig.show = show
    mag = axis(title)
    mag.xScaleFactor = xscale
    mag.yScaleFactor = yscale
    mag.xScale = 'log'
    mag.yScale = 'log'
    if ini.Hz == True:
        mag.xLabel = 'frequency [' + xscale + 'Hz]'
    else:
        mag.xLabel = 'frequency [' + xscale + 'rad/s]'
    mag.yLabel = 'magnitude [' + yscale + yunits +']'
    try:
        xScaleFactor = 10**int(SCALEFACTORS[xscale])
    except:
        xScaleFactor = 1.
    x = np.geomspace(checkNumber(fStart)*xScaleFactor, checkNumber(fStop)*xScaleFactor, checkNumber(fNum))
    mag.traces = []
    if type(results) == type(allResults()):
        results = [results]
    colNum = 0
    numColors = len(ini.defaultColors)
    for result in results:
        if result.dataType == 'numer':
            yData = result.numer
            yLabel = 'numer: '
        if result.dataType == 'denom':
            yData = result.denom
            yLabel = 'denom: '
        if result.dataType == 'laplace':
            yData = result.laplace
            yLabel = ''
        else:
            print "Error: wrong data type '%s' for 'plotMag()'."%(result.dataType)
            return fig
        if not result.step:
            if ini.Hz == True:
                yData = yData.xreplace({ini.Laplace: 2*sp.pi*sp.I*ini.frequency})
                func = sp.lambdify(ini.frequency, abs(yData))
            else:
                yData = yData.xreplace({ini.Laplace: sp.I*ini.frequency})
                func = sp.lambdify(ini.frequency, abs(yData))
            y = [func(x[j]) for j in range(len(x))]
            magTrace = trace([x, y])
            try:
                magTrace.color = ini.gainColors[result.gainType]
            except:
                magTrace.color = ini.defaultColors[colNum % numColors]
            if result.gainType == 'vi':
                yLabel += '$' + sp.latex(sp.Symbol(result.detLabel)) + '$'
            else:
                yLabel += result.gainType
            magTrace.label = result.gainType
            mag.traces.append(magTrace)
        elif type(yData) == list:
            if result.gainType == 'vi':
                yLabel += '$' + sp.latex(sp.Symbol(result.detLabel)) + '$'
            else:
                yLabel += result.gainType
            for i in range(len(yData)):
                if ini.Hz == True:
                    y = yData[i].xreplace({ini.Laplace: 2*sp.pi*sp.I*ini.frequency})
                    func = sp.lambdify(ini.frequency, abs(y))
                else:
                    y = yData[i].xreplace({ini.Laplace: sp.I*ini.frequency})
                    func = sp.lambdify(ini.frequency, abs(y))
                y = [func(x[j]) for j in range(len(x))]
                magTrace = trace([x, y])
                magTrace.color = ini.defaultColors[i % numColors]
                magTrace.label = yLabel
                if result.stepMethod == 'array':
                    magTrace.label += ', run: %s'%(i+1)
                else:
                    magTrace.label += ', %s = %8.1e'%(result.stepVar, result.stepList[i])
                mag.traces.append(magTrace)  
        colNum += 1   
    fig.axes = [[mag]]
    fig.plot()
    return fig
                
def plotPhase(fileName, title, results, fStart, fStop, fNum, xscale = '', yscale = '', show = False):
    """
    """
    fig = figure(fileName)
    fig.show = show
    phase = axis(title)
    phase.xScaleFactor = xscale
    phase.yScaleFactor = yscale
    phase.xScale = 'log'
    phase.yScale = 'lin'
    if ini.Hz == True:
        phase.xLabel = 'frequency [' + xscale + 'Hz]'
        phase.yLabel = 'phase [' + yscale + 'deg]'
    else:
        phase.xLabel = 'frequency [' + xscale + 'rad/s]'
        phase.yLabel = 'phase [' + yscale + 'rad]'
    try:
        xScaleFactor = 10**int(SCALEFACTORS[xscale])
    except:
        xScaleFactor = 1.
    x = np.geomspace(checkNumber(fStart)*xScaleFactor, checkNumber(fStop)*xScaleFactor, checkNumber(fNum))
    phase.traces = []
    if type(results) == type(allResults()):
        results = [results]
    colNum = 0
    numColors = len(ini.defaultColors)
    for result in results:
        if result.dataType == 'numer':
            yData = result.numer
            yLabel = 'numer: '
        if result.dataType == 'denom':
            yData = result.denom
            yLabel = 'denom: '
        if result.dataType == 'laplace':
            yData = result.laplace
            yLabel = ''
        else:
            print "Error: wrong data type '%s' for 'plotPhase()'."%(result.dataType)
            return fig
        if not result.step:
            if ini.Hz == True:
                yData = yData.xreplace({ini.Laplace: 2*sp.pi*sp.I*ini.frequency})
                func = sp.lambdify(ini.frequency, yData)
                y = 180*np.unwrap(np.angle(func(x)))/np.pi
            else:
                yData = yData.xreplace({ini.Laplace: sp.I*ini.frequency})
                func = sp.lambdify(ini.frequency, yData)
                y = np.unwrap(np.angle(func(x)))
            phaseTrace = trace([x, y])
            try:
                phaseTrace.color = ini.gainColors[result.gainType]
            except:
                phaseTrace.color = ini.defaultColors[colNum % numColors]
            if result.gainType == 'vi':
                yLabel += '$' + sp.latex(sp.Symbol(result.detLabel)) + '$'
            else:
                yLabel += result.gainType
            phaseTrace.label = yLabel
            phase.traces.append(phaseTrace)
        elif type(yData) == list:
            if result.gainType == 'vi':
                yLabel += '$' + sp.latex(sp.Symbol(result.detLabel)) + '$'
            else:
                yLabel += result.gainType
            for i in range(len(yData)):
                if ini.Hz == True:
                    y = yData[i].xreplace({ini.Laplace: 2*sp.pi*sp.I*ini.frequency})
                    func = sp.lambdify(ini.frequency, y)
                    y = 180*np.unwrap(np.angle(func(x)))/np.pi
                else:
                    y = yData[i].xreplace({ini.Laplace: sp.I*ini.frequency})
                    func = sp.lambdify(ini.frequency, y)
                    y = np.unwrap(np.angle(func(x)))
                phaseTrace = trace([x, y])
                phaseTrace.color = ini.defaultColors[i % numColors]
                phaseTrace.label = yLabel
                if result.stepMethod == 'array':
                    phaseTrace.label += ', run: %s'%(i+1)
                else:
                    phaseTrace.label += ', %s = %8.1e'%(result.stepVar, result.stepList[i])
                phase.traces.append(phaseTrace)
        colNum += 1
    fig.axes = [[phase]]
    fig.plot()
    return fig
                
def plotDelay(fileName, title, results, fStart, fStop, fNum, xscale = '', yscale = '', show = False):
    """
    """
    fig = figure(fileName)
    fig.show = show
    delay = axis(title)
    delay.xScaleFactor = xscale
    delay.yScaleFactor = yscale
    delay.xScale = 'log'
    delay.yScale = 'lin'
    if ini.Hz == True:
        delay.xLabel = 'frequency [' + xscale + 'Hz]'
    else:
        delay.xLabel = 'frequency [' + xscale + 'rad/s]'
    delay.yLabel = 'delay [' + yscale + 's]'
    try:
        xScaleFactor = 10**int(SCALEFACTORS[xscale])
    except:
        xScaleFactor = 1.
    x = np.geomspace(checkNumber(fStart)*xScaleFactor, checkNumber(fStop)*xScaleFactor, checkNumber(fNum))
    delay.traces = []
    if type(results) == type(allResults()):
        results = [results]
    colNum = 0
    numColors = len(ini.defaultColors)
    for result in results:
        if result.dataType == 'numer':
            yData = result.numer
            yLabel = 'numer: '
        if result.dataType == 'denom':
            yData = result.denom
            yLabel = 'denom: '
        if result.dataType == 'laplace':
            yData = result.laplace
            yLabel = ''
        else:
            print "Error: wrong data type '%s' for 'plotPhase()'."%(result.dataType)
            return fig
        if not result.step:
            yData = yData.xreplace({ini.Laplace: sp.I*ini.frequency})
            func = sp.lambdify(ini.frequency, yData)
            y = -np.diff(np.unwrap(np.angle(func(x))))/np.diff(x)
            # y one point less than x after differentiation so remove last point x
            x = x[0:-1] 
            delayTrace = trace([x, y])
            try:
                delayTrace.color = ini.gainColors[result.gainType]
            except:
                delayTrace.color = ini.defaultColors[colNum % numColors]
            if result.gainType == 'vi':
                yLabel += '$' + sp.latex(sp.Symbol(result.detLabel)) + '$'
            else:
                yLabel += result.gainType
            delayTrace.label = yLabel
            delay.traces.append(delayTrace)
        elif type(yData) == list:
            if result.gainType == 'vi':
                yLabel += '$' + sp.latex(sp.Symbol(result.detLabel)) + '$'
            else:
                yLabel += result.gainType
            for i in range(len(yData)):
                y = yData[i].xreplace({ini.Laplace: sp.I*ini.frequency})
                func = sp.lambdify(ini.frequency, y)
                y = -np.diff(np.unwrap(np.angle(func(x))))/np.diff(x)
                # y one point less than x after differentiation so remove last point x
                x = x[0:-1] 
                delayTrace = trace([x, y])
                delayTrace.color = ini.defaultColors[i % numColors]
                if result.stepMethod == 'array':
                    delayTrace.label += ', run: %s'%(i+1)
                else:
                    delayTrace.label += ', %s = %8.1e'%(result.stepVar, result.stepList[i])
                delay.traces.append(delayTrace)
        colNum += 1
    fig.axes = [[delay]]
    fig.plot()
    return fig
               
def plotTime(fileName, title, results, tStart, tStop, tNum, xscale = '', yscale = '', yunits = '', show = False):
    """
    """
    fig = figure(fileName)
    fig.show = show
    time = axis(title)
    time.xScaleFactor = xscale
    time.yScaleFactor = yscale
    time.xScale = 'lin'
    time.yScale = 'lin'
    time.xLabel = 'time [' + xscale + 's]'
    time.yLabel = '[' + yscale + yunits + ']'
    try:
        xScaleFactor = 10**int(SCALEFACTORS[xscale])
    except:
        xScaleFactor = 1.
    x = np.linspace(checkNumber(tStart)*xScaleFactor, checkNumber(tStop)*xScaleFactor, checkNumber(tNum))
    time.traces = []
    if type(results) == type(allResults()):
        results = [results]
    colNum = 0
    numColors = len(ini.defaultColors)
    for result in results:
        if result.dataType == 'time':
            yData = result.time
            label = '$%s$'%(sp.latex(sp.Symbol(result.detLabel)))
        elif result.dataType == 'impulse':
            yData = result.impulse
            label = result.gainType
        elif result.dataType == 'step':
            yData = result.stepResp
            label = result.gainType
        else:
            print "Error: wrong data type '%s' for 'plotTime()'."%(result.dataType)
            return fig
        if not result.step:
            func = sp.lambdify(sp.Symbol('t'), yData)
            y = np.real(func(x))
            timeTrace = trace([x, y])
            try:
                timeTrace.color = ini.gainColors[result.gainType]
            except:
                timeTrace.color = ini.defaultColors[colNum % numColors]
            timeTrace.label = label
            time.traces.append(timeTrace)
        elif type(yData) == list:
            if result.gainType == 'vi':
                yLabel += '$' + sp.latex(sp.Symbol(result.detLabel)) + '$'
            else:
                yLabel += result.gainType
            for i in range(len(yData)):
                func = sp.lambdify(sp.Symbol('t',), yData[i])
                y = np.real(func(x))
                timeTrace = trace([x, y])
                timeTrace.color = ini.defaultColors[i % numColors]
                if result.stepMethod == 'array':
                    timeTrace.label += ' run: %s'%(i+1)
                else:
                    timeTrace.label += ', %s = %8.1e'%(result.stepVar, result.stepList[i])
                time.traces.append(timeTrace)
        colNum += 1
    fig.axes = [[time]]
    fig.plot()
    return fig

def plotPZ(fileName, title, results, xmin = None, xmax = None, ymin = None, ymax = None, xscale = '', yscale = '', show = False):
    """
    """
    fig = figure(fileName)
    fig.show = show
    fig.axisHeight = fig.axisWidth
    pz = axis(title)
    pz.xScaleFactor = xscale
    pz.yScaleFactor = yscale
    pz.xScale = 'lin'
    pz.yScale = 'lin'
    if ini.Hz == True:
        pz.xLabel = 'Re [' + xscale + 'Hz]'
        pz.yLabel = 'Im [' + yscale + 'Hz]'
    else:
        pz.xLabel = 'Re [' + xscale + 'rad/s]'
        pz.yLabel = 'Im [' + yscale + 'rad/s]'
    pzTraces = []
    if xmin != None and xmax != None:
        pz.xLim = [checkNumber(xmin), checkNumber(xmax)]
    if ymin != None and xmax != None:
        pz.yLim = [checkNumber(ymin), checkNumber(ymax)]
    if type(results) == type(allResults()):
        results = [results]
    colNum = 0
    numColors = len(ini.defaultColors)
    for result in results:
        if not result.step:
            if result.dataType == 'poles' or result.dataType == 'pz':
                if ini.Hz == True:
                    polesTrace = trace([np.real(result.poles)/2/np.pi, np.imag(result.poles)/2/np.pi])
                else:
                    polesTrace = trace([np.real(result.poles), np.imag(result.poles)])
                try:
                    polesTrace.markerColor = ini.gainColors[result.gainType]
                except:
                    polesTrace.markerColor = ini.defaultColors[colNum % numColors]
                polesTrace.color = ''
                polesTrace.marker = 'x'
                polesTrace.lineWidth = '0'
                polesTrace.label = 'poles ' + result.gainType
                pzTraces.append(polesTrace)
            if result.dataType == 'zeros' or result.dataType == 'pz':
                if ini.Hz == True:
                    zerosTrace = trace([np.real(result.zeros)/2/np.pi, np.imag(result.zeros)/2/np.pi])
                else:
                    zerosTrace = trace([np.real(result.zeros), np.imag(result.zeros)])
                zerosTrace.color = ''
                try:
                    zerosTrace.markerColor = ini.gainColors[result.gainType]
                except:
                    zerosTrace.markerColor = ini.defaultColors[colNum % numColors]
                zerosTrace.marker = 'o'
                zerosTrace.lineWidth = '0'
                zerosTrace.label = 'zeros ' + result.gainType
                pzTraces.append(zerosTrace)
            if result.dataType != 'poles' and result.dataType != 'zeros' and result.dataType != 'pz':
                print "Error: wrong data type '%s' for 'plotTime()'."%(result.dataType)
                return fig
        elif result.dataType == 'poles' or result.dataType == 'pz':
            poles = result.poles
            if len(poles) != 0:
                # start of root locus
                if ini.Hz == True:
                    polesTrace = trace([np.real(result.poles[0])/2/np.pi, np.imag(result.poles[0])/2/np.pi])
                else:
                    polesTrace = trace([np.real(result.poles[0]), np.imag(result.poles[0])])
                try:
                    polesTrace.markerColor = ini.gainColors[result.gainType]
                except:
                    polesTrace.markerColor = ini.defaultColors[colNum % numColors]
                polesTrace.color = ''
                polesTrace.marker = 'x'
                polesTrace.lineWidth = '0'
                polesTrace.label = 'poles ' + result.gainType
                if result.stepMethod == 'array':
                    polesTrace.label += ', run: 1'
                else:
                    polesTrace.label += ', %s = %8.1e'%(result.stepVar, result.stepList[0])
                pzTraces.append(polesTrace)
                # end of root locus
                if ini.Hz == True:
                    polesTrace = trace([np.real(result.poles[-1])/2/np.pi, np.imag(result.poles[-1])/2/np.pi])
                else:
                    polesTrace = trace([np.real(result.poles[-1]), np.imag(result.poles[-1])])
                try:
                    polesTrace.markerColor = ini.gainColors[result.gainType]
                except:
                    polesTrace.markerColor = ini.defaultColors[colNum % numColors]
                polesTrace.color = ''
                polesTrace.marker = '+'
                polesTrace.markerSize = 10
                polesTrace.lineWidth = '0'
                polesTrace.label = 'poles ' + result.gainType
                if result.stepMethod == 'array':
                    polesTrace.label += ', run: %s'%(len(poles))
                else:
                    polesTrace.label += ', %s = %8.1e'%(result.stepVar, result.stepList[-1])
                pzTraces.append(polesTrace)
                # root locus
                allPoles = np.array([])
                for i in range(len(poles)):
                    allPoles = np.concatenate((allPoles, poles[i]), axis = None)
                if ini.Hz == True:
                    polesTrace = trace([np.real(allPoles)/2/np.pi, np.imag(allPoles)/2/np.pi])
                else:
                    polesTrace = trace([np.real(allPoles), np.imag(allPoles)])
                try:
                    polesTrace.markerColor = ini.gainColors[result.gainType]
                except:
                    polesTrace.markerColor = ini.defaultColors[colNum % numColors]
                polesTrace.color = ''
                polesTrace.marker = '.'
                polesTrace.lineWidth = '0'
                polesTrace.markerSize = 2
                polesTrace.markerFaceColor = polesTrace.markerColor
                polesTrace.label = 'poles ' + result.gainType
                if result.stepMethod == 'array':
                    polesTrace.label += ', run: 1 ... %s'%(len(poles))
                else:
                    polesTrace.label += ', %s = %8.1e ... %8.1e'%(result.stepVar, result.stepList[0], result.stepList[-1])
                pzTraces.append(polesTrace)
        elif result.dataType == 'zeros' or result.dataType == 'pz':
            zeros = result.zeros
            if len(zeros) != 0:
                # start of zeros locus
                if ini.Hz == True:
                    zerosTrace = trace([np.real(result.zeros[0])/2/np.pi, np.imag(result.zeros[0])/2/np.pi])
                else:
                    zerosTrace = trace([np.real(result.zeros[0]), np.imag(result.zeros[0])])
                try:
                    zerosTrace.markerColor = ini.gainColors[result.gainType]
                except:
                    zerosTrace.markerColor = ini.defaultColors[colNum % numColors]
                zerosTrace.color = ''
                zerosTrace.marker = 'o'
                zerosTrace.lineWidth = '0'
                zerosTrace.label = 'zeros ' + result.gainType
                if result.stepMethod == 'array':
                    zerosTrace.label += ', run: 1'
                else:
                    zerosTrace.label += ', %s = %8.1e'%(result.stepVar, result.stepList[0])
                pzTraces.append(zerosTrace)
                # end of zeros locus
                if ini.Hz == True:
                    zerosTrace = trace([np.real(result.zeros[-1])/2/np.pi, np.imag(result.zeros[-1])/2/np.pi])
                else:
                    zerosTrace = trace([np.real(result.zeros[-1]), np.imag(result.zeros[-1])])
                try:
                    zerosTrace.markerColor = ini.gainColors[result.gainType]
                except:
                    zerosTrace.markerColor = ini.defaultColors[colNum % numColors]
                zerosTrace.color = ''
                zerosTrace.marker = 's'
                zerosTrace.lineWidth = '0'
                zerosTrace.label = 'zeros ' + result.gainType
                if result.stepMethod == 'array':
                    zerosTrace.label += ', run: %s'%(len(zeros))
                else:
                    zerosTrace.label += ', %s = %8.1e'%(result.stepVar, result.stepList[-1])
                pzTraces.append(zerosTrace)
                # zeros locus
                allZeros = np.array([])
                for i in range(len(zeros)):
                    allZeros = np.concatenate((allZeros, result.zeros[i]), axis = None)
                if ini.Hz == True:
                    zerosTrace = trace([np.real(allZeros)/2/np.pi, np.imag(allZeros)/2/np.pi])
                else:
                    zerosTrace = trace([np.real(allZeros), np.imag(allZeros)])
                try:
                    zerosTrace.markerColor = ini.gainColors[result.gainType]
                except:
                    zerosTrace.markerColor = ini.defaultColors[colNum % numColors]
                zerosTrace.color = ''
                zerosTrace.marker = '.'
                zerosTrace.lineWidth = '0'
                zerosTrace.markerSize = 2
                zerosTrace.markerFaceColor = zerosTrace.markerColor
                zerosTrace.label = 'zeros ' + result.gainType
                if result.stepMethod == 'array':
                    zerosTrace.label += ', run: 1 ... %s'%(len(zeros))
                else:
                    zerosTrace.label += ', %s = %8.1e ... %8.1e'%(result.stepVar, result.stepList[0], result.stepList[-1])
                pzTraces.append(zerosTrace)    
        colNum += 1                  
    pz.traces = pzTraces
    fig.axes = [[pz]]
    fig.plot()
    return fig

def plotNoise(fileName, title, results, fStart, fStop, fNum, noise = 'onoise', sources = None, xscale = '', yscale = '', show = False):
    """
    """
    fig = figure(fileName)
    fig.show = show
    ax = axis(title)
    ax.xScaleFactor = xscale
    ax.yScaleFactor = yscale
    ax.xScale = 'log'
    ax.yScale = 'log'
    ax.xLabel = 'frequency [' + xscale + 'Hz]'
    if noise == 'onoise':
        yunits = results.detUnits
    if noise == 'inoise':
        yunits = results.srcUnits
    ax.yLabel = 'spectral density [' + yscale + yunits +'^2/Hz]'
    try:
        xScaleFactor = 10**int(SCALEFACTORS[xscale])
    except:
        xScaleFactor = 1.
    x = np.geomspace(checkNumber(fStart)*xScaleFactor, checkNumber(fStop)*xScaleFactor, checkNumber(fNum))
    ax.traces = []
    if type(results) == type(allResults()):
        results = [results]
    colNum = 0
    numColors = len(ini.defaultColors)
    for result in results:
        keys = result.onoiseTerms.keys()
        if not result.step:
            if noise == 'onoise':
                if sources == None:
                    yData = result.onoise
                    func = sp.lambdify(ini.frequency, yData)
                    y = [func(x[j]) for j in range(len(x))]
                    noiseTrace = trace([x, y])
                    noiseTrace.label = 'onoise'
                    ax.traces.append(noiseTrace)
                elif sources == 'all':
                    for srcName in keys:
                        yData = result.onoiseTerms[srcName]
                        func = sp.lambdify(ini.frequency, yData)
                        y = [func(x[j]) for j in range(len(x))]
                        noiseTrace = trace([x, y])
                        noiseTrace.color = ini.defaultColors[colNum % numColors]
                        noiseTrace.label = 'onoise: ' + srcName
                        ax.traces.append(noiseTrace)
                        colNum += 1
                elif sources in keys:
                    yData = result.onoiseTerms[sources]
                    func = sp.lambdify(ini.frequency, yData)
                    y = [func(x[j]) for j in range(len(x))]
                    noiseTrace = trace([x, y])
                    noiseTrace.color = ini.defaultColors[colNum % numColors]
                    noiseTrace.label = 'onoise: ' + sources
                    ax.traces.append(noiseTrace)
                    colNum += 1
                elif type(sources) == list:
                    for srcName in sources:
                        if srcName in keys:
                            yData = result.onoiseTerms[srcName]
                            func = sp.lambdify(ini.frequency, yData)
                            y = [func(x[j]) for j in range(len(x))]
                            noiseTrace = trace([x, y])
                            noiseTrace.color = ini.defaultColors[colNum % numColors]
                            noiseTrace.label = 'onoise: ' + srcName
                            ax.traces.append(noiseTrace)
                            colNum += 1
                else:
                    print 'Error: cannot understand "sources=%s".'%(str(sources))
                    return fig
            elif noise == 'inoise':
                if sources == None:
                    yData = result.inoise
                    func = sp.lambdify(ini.frequency, yData)
                    y = [func(x[j]) for j in range(len(x))]
                    noiseTrace = trace([x, y])                                
                    noiseTrace.color = ini.defaultColors[colNum % numColors]
                    noiseTrace.label = 'inoise'
                    ax.traces.append(noiseTrace)
                    colNum += 1
                elif sources == 'all':
                    for srcName in keys:
                        yData = result.inoiseTerms[srcName]
                        func = sp.lambdify(ini.frequency, yData)
                        y = [func(x[j]) for j in range(len(x))]
                        noiseTrace = trace([x, y])
                        noiseTrace.color = ini.defaultColors[colNum % numColors]
                        noiseTrace.label = 'inoise: ' + srcName
                        ax.traces.append(noiseTrace)
                        colNum += 1
                elif sources in keys:
                    yData = result.inoiseTerms[sources]
                    func = sp.lambdify(ini.frequency, yData)
                    y = [func(x[j]) for j in range(len(x))]
                    noiseTrace = trace([x, y])
                    noiseTrace.color = ini.defaultColors[colNum % numColors]
                    noiseTrace.label = 'inoise: ' + sources
                    ax.traces.append(noiseTrace)
                    colNum += 1  
                elif type(sources) == list:
                    for srcName in sources:
                        if srcName in keys:
                            yData = result.inoiseTerms[srcName]
                            func = sp.lambdify(ini.frequency, yData)
                            y = [func(x[j]) for j in range(len(x))]
                            noiseTrace = trace([x, y])
                            noiseTrace.color = ini.defaultColors[colNum % numColors]
                            noiseTrace.label = 'inoise: ' + srcName
                            ax.traces.append(noiseTrace) 
                            colNum += 1    
                else:
                    print 'Error: cannot understand "sources=%s".'%(str(sources))
                    return fig
            else:
                print 'Error: cannot understand "noise=%s".'%(str(noise))
                return fig
        else:
            numRuns = len(result.onoiseTerms[keys[0]])
            if type(sources) == list or sources == 'all':
                print 'Error: plotting of stepped noise analysis for multiple sources is not suported.'
                return fig
            else:
                for i in range(numRuns):
                    if sources == None:
                        if noise == 'onoise':
                            label = 'onoise:'
                            yData = result.onoise[i]
                        elif noise == 'inoise':
                            label = 'inoise:'   
                            yData = result.inoise[i]
                    elif sources in keys:
                        if noise == 'onoise':
                            label = 'onoise: %s,'%(sources)
                            yData = result.onoiseTerms[sources][i]
                        elif noise == 'inoise':
                            label = 'inoise: %s,'%(sources)
                            yData = result.inoiseTerms[sources][i]
                    else:
                        print 'Error:  cannot understand "sources=%s".'%(str(sources))
                        return
                    if result.stepMethod == 'array':
                        label += ' run: %s'%(i+1)
                    else:
                        label += ' %s = %8.1e'%(result.stepVar, result.stepList[i])
                    # add trace
                    func = sp.lambdify(ini.frequency, yData)
                    y = [func(x[j]) for j in range(len(x))]
                    noiseTrace = trace([x, y])
                    noiseTrace.label = label
                    ax.traces.append(noiseTrace)
    fig.axes = [[ax]]
    fig.plot()
    return fig

def plotParams(fileName, title, plotData, xaxis = 'lin', yaxis = 'lin', xunits = '', yunits= '', punits = '', xscale = '', yscale = '', pscale = '', show = False):
    if type(plotData) != type(paramPlot()):
        print "Error: unexpected input data."
        return
    if type(plotData) == bool or type(plotData.yValues) == bool:
        print "Error: incomplete plot data."
        return
    try:
        xScaleFactor = 10**int(SCALEFACTORS[xscale])
    except:
        xScaleFactor = 1.
    try:
        yScaleFactor = 10**int(SCALEFACTORS[yscale])
    except:
        yScaleFactor = 1.
    try:
        pScaleFactor = 10**int(SCALEFACTORS[pscale])
    except:
        pScaleFactor = 1.
    colNum = 0
    numColors = len(ini.defaultColors)
    pVar = '$' + sp.latex(sp.sympify(plotData.pVar)) +'$'
    xVar = '$' + sp.latex(sp.sympify(plotData.xVar)) +'$'
    yVar = '$' + sp.latex(sp.sympify(plotData.yVar)) +'$'
    fig = figure(fileName)
    fig.show = show
    ax = axis(title)
    ax.xScale = xaxis
    ax.yScale = yaxis
    ax.xLabel = xVar + ' [' + xscale + xunits +']'
    ax.yLabel = yVar + ' [' + yscale + yunits +']'
    if type(plotData.xValues) == dict:
        xDict = True
    else:
        xDict = False
    if type(plotData.yValues) == list:
        xyTrace = trace(plotData.xValues/xScaleFactor, plotData.yValues/yScaleFactor)
        xyTrace.label = yVar + '(' + plotData.xVar + ')'
        xyTrace.color = ini.defaultColors[colNum]
        ax.traces.append(xyTrace)
    else:
        stepVals = plotData.yValues.keys()
        stepVals.sort()
        for stepVal in stepVals:
            if xDict:
                xyTrace = trace([plotData.xValues[stepVal]/xScaleFactor, plotData.yValues[stepVal]/yScaleFactor])
            else:
                xyTrace = trace([plotData.xValues/xScaleFactor, plotData.yValues[stepVal]/yScaleFactor])
            xyTrace.color = ini.defaultColors[colNum % numColors]   
            xyTrace.label = pVar + '=%s [%s%s]'%(stepVal/pScaleFactor, pscale, punits)
            ax.traces.append(xyTrace)
            colNum += 1
    fig.axes = [[ax]]
    fig.plot()
    return fig

def plotCSV(fileName):
    return

def plotVsStep(fileName, title, result, goalFuncObj, show = False, save = True):
    """
    plotVsStep(figTitle, results, goalFuncObj) 
    """
    errors = 0
    if type(result) != type(allResults()):
        print "Error: plotVsStep only accepts single allResults() objects."
        errors += 1
    if result.step == False:
        print "Error: parameter stepping should be enabled for this plot."
        errors += 1
    if result.stepMethod == 'array':
        print "Error: array stepping is not supported by 'plotVsStep'."
    if goalFuncObj.type == 'totalNoise' or goalFuncObj.type == 'NF':
        if result.dataType != 'noise':
            print "Error: goal function requires dataType 'noise'."
            errors += 1
    elif goalFuncObj.type == 'stdDev':
        if result.dataType != 'dcvar':
            print "Error: goal function requires dataType 'dcvar'."
            errors += 1
    elif goalFuncObj.type == 'YatX':
        pass
    else:
        print "Error: unknown goal function."
        errors += 1
    if errors != 0:
        return
    fig = figure(fileName)
    fig.show = show
    vsStep = axis(title)
    vsStep.xScaleFactor = goalFuncObj.pscale
    vsStep.yScaleFactor = goalFuncObj.yscale
    if result.stepMethod == 'log':
        vsStep.xScale = 'log'
    else:
        vsStep.xScale = 'lin'
    vsStep.yLabel = goalFuncObj.ylabel + ' [' + goalFuncObj.yscale + goalFuncObj.yunits + ']'
    vsStep.yScale = goalFuncObj.ylinlog
    vsStep.xLabel = str(result.stepVar) + ' [' + goalFuncObj.pscale + goalFuncObj.punits + ']'
    vsStep.traces = [makeGoalFuncTrace(result, goalFuncObj)]
    fig.axes = [[vsStep]]
    fig.plot()
    return

def makeGoalFuncTrace(result, goalFuncObj):
    """
    """
    if ini.Hz:
        freq = 2*sp.pi*sp.I*ini.frequency
    else:
        freq = sp.I*ini.frequency
    x = np.array(result.stepList) 
    if result.dataType == 'numer' and goalFuncObj.type == 'YatX':
        y = np.array([sp.Abs(result.numer[i].subs(ini.Laplace, freq).subs(ini.frequency, goalFuncObj.value)) for i in range(len(x))])
    elif result.dataType == 'denom' and goalFuncObj.type == 'YatX':
        y = np.array([sp.Abs(result.denom[i].subs(ini.Laplace, freq).subs(ini.frequency, goalFuncObj.value)) for i in range(len(x))])
    elif result.dataType == 'laplace' and goalFuncObj.type == 'YatX':
        y = np.array([sp.Abs(result.laplace[i].subs(ini.Laplace, freq).subs(ini.frequency, goalFuncObj.value)) for i in range(len(x))])
    elif result.dataType == 'time' and goalFuncObj.type == 'YatX':
        y = np.array([result.time[i].subs(sp.Symbol('t'), goalFuncObj.value) for i in range(len(x))])
    elif result.dataType == 'impulse' and goalFuncObj.type == 'YatX':
        y = np.array([result.impulse[i].subs(sp.Symbol('t'),goalFuncObj.value) for i in range(len(x))])
    elif result.dataType == 'step' and goalFuncObj.type == 'YatX':
        y = np.array([result.step[i].subs(sp.Symbol('t'), goalFuncObj.value) for i in range(len(x))])
    elif result.dataType == 'noise':
        if goalFuncObj.type == 'totalNoise':
            y = np.array([rmsNoise(result, goalFuncObj.noiseType, goalFuncObj.fmin, goalFuncObj.fmax, source = goalFuncObj.source)])
        if goalFuncObj.type == 'YatX':
            if goalFuncObj.source != None:
                if goalFuncObj.source in result.onoiseTerms.keys():
                    if goalFuncObj.noiseType == 'onoise':
                        y = np.array([result.onoiseTerms[goalFuncObj.source][i].subs(ini.frequency, goalFuncObj.value) for i in range(len(x))])
                    if goalFuncObj.noiseType == 'inoise':
                        y = np.array([result.inoiseTerms[goalFuncObj.source][i].subs(ini.frequency, goalFuncObj.value) for i in range(len(x))])
                else:
                    print "Error: unknown noise source '%s'."%(goalFuncObj.source)
            else:
                if goalFuncObj.noiseType == 'onoise':
                    y = np.array([result.onoise[i].subs(ini.frequency, goalFuncObj.value) for i in range(len(x))])
                if goalFuncObj.noiseType == 'inoise':
                    y = np.array([result.inoise[i].subs(ini.frequency, goalFuncObj.value) for i in range(len(x))])
        elif goalFuncObj.type == 'NF':
            if result.source == None or result.source not in result.inoiseTerms.keys():
                print "Error: goal function 'NF' requires noise associated with the signal source."
            else:
                totalOnoise       = rmsNoise(result, 'onoise', goalFuncObj.fmin, goalFuncObj.fmax)
                totalOnoiseSource = rmsNoise(result, 'onoise', goalFuncObj.fmin, goalFuncObj.fmax, source = result.source)
                y = np.array([20*sp.log(totalOnoise[i]/totalOnoiseSource[i])/sp.log(10) for i in range(len(x))])
    elif result.dataType == 'dcvar':
        if goalFuncObj.type == 'stdDev':
            if goalFuncObj.source != None:
                if goalFuncObj.dcvarType == 'ivar':
                    if goalFuncObj.source not in result.ivarTerms.keys():
                        print "Error: unknown source '%s'."%(goalFuncObj.source)
                    else:
                        data = result.ivarTerms[goalFuncObj.source]
                if goalFuncObj.dcvarType == 'ovar':
                    if goalFuncObj.source not in result.ovarTerms.keys():
                        print "Error: unknown source '%s'."%(goalFuncObj.source)
                    else:
                        data = result.ovarTerms[goalFuncObj.source]
            y = np.sqrt(np.array(data))
    elif result.dataType == 'dc' and goalFuncObj.type == 'dc':
        y = np.array(result.dc)
    try:
        xScaleFactor = 10**int(SCALEFACTORS[pscale])
    except:
        xScaleFactor = 1.
    try:
        yScaleFactor = 10**int(SCALEFACTORS[yscale])
    except:
        yScaleFactor = 1.
    return trace([x/xScaleFactor, y/yScaleFactor])

def rmsNoise(noiseResult, noise, fmin, fmax, source = None):
    """
    """
    if fmin == None or fmax == None:
        print "Error in frequency range specification."
        return None
    if fmin != None and fmax != None:
        if checkNumber(fmin) != None and  checkNumber(fmin) != None and fmin >= fmax:
            print "Error in frequency range specification."
            return None
    if noiseResult.dataType != 'noise':
        print "Error: expected dataType noise, got: '%s'."%(noiseResult.dataType)
        rms = None
    keys = noiseResult.onoiseTerms.keys()
    if noise == 'inoise':
        if source == None:
            noiseData = noiseResult.inoise
        elif source in keys:
            noiseData = noiseResult.inoiseTerms[source]
        else:
            print "Error: unknown noise source: '%s'."%(source)
            rms = None
    elif noise == 'onoise':
        if source == None:
            noiseData = noiseResult.onoise
        elif source in keys:
            noiseData = noiseResult.onoiseTerms[source]
        else:
            print "Error: unknown noise source: '%s'."%(source)
            rms = None
    else:
        print "Error: unknown noise type: '%s'."%(noise)
        rms = None
    if type(noiseData) != list:
        noiseData = [noiseData]    
    rms =  np.array([sp.N(sp.sqrt(maxIntegrate(noiseData[i], ini.frequency, start=fmin, stop=fmax, numeric=noiseResult.simType))) for i in range(len(noiseData))])
    if len(rms) == 1:
        rms = rms[0]
    return rms

def plotFunction(fileName, title, funcObject, start, stop, points, save=True, show=False):
    """
    """
    xvars = list(funcObject.expr.atoms(sp.Symbol))
    if len(xvars) > 1:
        print "Error: too many fuction variables."
        return
    try:
        xScaleFactor = 10**int(SCALEFACTORS[funcObject.xscale])
    except:
        xScaleFactor = 1.
    try:
        yScaleFactor = 10**int(SCALEFACTORS[funcObject.yscale])
    except:
        yScaleFactor = 1.
    fig = figure(fileName)
    fig.show = show
    ax = axis(title)
    ax.xScaleFactor = funcObject.xscale
    ax.yScaleFactor = funcObject.yscale
    ax.xScale = funcObject.xaxis
    ax.xLabel = str(xvars[0]) + ' [' + funcObject.xscale + funcObject.xunits + ']'
    ax.yScale = funcObject.yaxis
    ax.yLabel = funcObject.ylabel + ' [' + funcObject.yscale + funcObject.yunits + ']'
    start  = checkNumber(start)
    stop   = checkNumber(stop)
    points = checkNumber(points)
    if start != None and stop != None and points != None:
        start *= xScaleFactor
        stop  *= xScaleFactor
        if funcObject.xaxis == 'lin':
            x = np.linspace(start, stop, points)
        elif funcObject.xaxis == 'log':
            x = np.geomspace(start, stop, points)
    else:
        print "Error(s) in x range specification."
        return
    function = sp.lambdify(xvars[0], funcObject.expr)
    y = np.array([function(x[i]) for i in range(len(x))])
    t = trace([x, y])
    t.label = funcObject.fname
    ax.traces = [t]
    fig.axes = [[ax]]
    fig.plot()
    return fig

class func(object):
    def __init__(self):
        self.expr = None
        self.xVar = None
        self.xscale = ''
        self.xunits = ''
        self.xaxis  = 'lin'
        self.ylabel = ''
        self.yscale = ''
        self.yunits = ''
        self.yaxis  = 'lin'
        self.color  = None
        self.fname  = None

if __name__=='__main__':
    ini.imgPath = ''
    x = np.linspace(0, 2*np.pi, endpoint = True)
    y1 = np.sin(x)
    y2 = np.cos(x)
    sine = trace([x, y1])
    sine.label = 'sine'
    sine.color = ''
    sine.lineWidth = '0'
    sine.marker = '.'
    sine.markerFaceColor = 'r'
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
    testFig.plot()
    plt.show()