#!/usr/bin/python
from SLiCAPpythonMaxima import *

class trace(object):
    """
    Trace prototype. Traces are plotted on axes, which are part of a figure.
    
    Trace attributes are:
        xData          : numpy array with x data
        yData          : numpy array with y data
        xName          : 'x'     # Header for table
        yName          : 'y'     # Header for table
        label          : ''      # trace label will be displayed in legend box
        color          : False   # trace color
        marker         : False   # trace marker
        markerColor    : False   # trace marker color
        markerFaceColor: 'none'  # trace marker face color
        markerSize     : 7       # trace marker size
        lineWidth      : 2
        lineType       : '-'
        table          :: False
        
    """
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
               
def plotSweep(fileName, title, results, sweepStart, sweepStop, sweepNum, sweepVar = 'auto', sweepScale = '', xVar = 'auto', xUnits = '', xScale = '', axisType = 'auto', funcType = 'auto', yVar = 'auto', yScale = '', yUnits = '', noiseSources = None, show = False):
    """
    """
    plotDataTypes = ['laplace', 'numer', 'denom', 'noise', 'step', 'impulse', 'time', 'params', None]
    funcTypes  = ['mag', 'dBmag', 'phase', 'delay', 'time', 'onoise', 'inoise', 'param']
    axisTypes  = ['lin', 'log', 'semilogx', 'semilogy', 'polar']
    freqTypes  = ['laplace', 'numer', 'denom', 'noise']
    timeTypes  = ['time', 'impulse', 'step']
    fig = figure(fileName)
    fig.show = show
    ax = axis(title)
    if type(results) != list:
        results = [results]
    colNum = 0
    numColors = len(ini.defaultColors)
    # first results defines the axis type and labels
    result = results[0]
    if result.dataType not in plotDataTypes:
        print "Error: cannot plot dataType '%s' with 'plotSweep()'."%(result.dataType)
        return fig
    if funcType == 'auto':
        if result.dataType == 'noise':
            funcType = 'onoise'
        elif result.dataType in freqTypes:
            funcType = 'mag'
        elif result.dataType in timeTypes:
            funcType = 'time'
    elif funcType == 'param':
        if sweepVar == 'auto':
            print "Error: undefined sweep variable."
            return fig
        if yVar == 'auto':
            print "Error: missing parameter to be plotted."
            return fig
        if xVar == 'auto':
            xVar = sweepVar
            xScale = sweepScale
    elif funcType not in funcTypes:
        print "Error: unknown funcType: '%s'."%(funcType)
        return fig
    if axisType == 'auto':
        if funcType == 'param':
            axisType = 'lin'
        elif funcType == 'mag' or result.dataType == 'noise':
            axisType = 'log'
        elif funcType == 'dBmag' or funcType == 'phase' or funcType == 'delay':
            axisType = 'semilogx'
        elif funcType == 'time':
            axisType = 'lin'
    elif axisType not in axisTypes:
        print "Error: unknown axisType: '%s'."%(axisType)
        return fig
    if axisType == 'lin':
        ax.xScale = 'lin'
        ax.yScale = 'lin'
    elif axisType == 'log':
        ax.xScale = 'log'
        ax.yScale = 'log'
    elif axisType == 'semilogx':
        ax.xScale = 'log'
        ax.yScale = 'lin'
    elif axisType == 'semilogy':
        ax.xScale = 'lin'
        ax.yScale = 'log'
    elif axisType == 'polar':
        ax.polar = True
        ax.yScale = 'lin'
    if not ax.polar:
        if funcType == 'param' and xVar != sweepVar:
            ax.xScaleFactor = xScale
        else:
            ax.xScaleFactor = sweepScale
    ax.yScaleFactor = yScale
    ax.traces = []
    # Create the axis labels
    # For parameter plots: the parameter names with units and scalefactors
    if funcType == 'param':
        ax.xLabel = '$' + sp.latex(sp.Symbol(xVar)) + '$ [' + xScale + xUnits + ']'
        ax.yLabel = '$' + sp.latex(sp.Symbol(yVar)) + '$ [' + yScale + yUnits + ']'
    # For time frequency plots we use frequency 'Hz' or 'rad/s' along the x-axis
    elif result.dataType in freqTypes:
        if result.dataType == 'noise':    
            if funcType == 'onoise':
                yUnits = result.detUnits
            if funcType == 'inoise':
                yUnits = result.srcUnits
            ax.xLabel = 'frequency [' + sweepScale + 'Hz]'
        elif ini.Hz == True:
            ax.xLabel = 'frequency [' + sweepScale + 'Hz]'
        else:
            ax.xLabel = 'frequency [' + sweepScale + 'rad/s]'
    # For time plots we use time along the x-axis
    elif funcType in timeTypes:
        ax.xLabel = 'time [' + sweepScale + 's]'
        yUnits = result.detUnits
    # Create the y-label for other than parameter plots
    if funcType == 'mag':
        ax.yLabel = 'magnitude [' + yScale + yUnits + ']'
    elif funcType == 'dBmag':
        ax.yLabel = 'magnitude [' + yScale + 'dB]'
    elif funcType == 'phase':
        if ini.Hz == True:
            ax.yLabel = 'phase [' + yScale + 'deg]'
        else:
            ax.yLabel = 'phase [' + yScale + 'rad]'
    elif funcType == 'delay':
        ax.yLabel = 'group delay [' + yScale + 's]'
    elif funcType == 'time':
        ax.yLabel = '[' + yScale + yUnits + ']'
    elif funcType == 'onoise':
        ax.yLabel = 'spectral density [' + yScale + yUnits +'^2/Hz]'
    elif funcType == 'inoise':
        ax.yLabel = 'spectral density [' + yScale + yUnits +'^2/Hz]'
    # Create the sweep, lin or log depending on the x-axis type
    try:
        xScaleFactor = 10**int(SCALEFACTORS[sweepScale])
    except:
        xScaleFactor = 1.
    if ax.xScale == 'log' or ax.xScale == 'semilogx' or ax.polar == True:
        x = np.geomspace(checkNumber(sweepStart)*xScaleFactor, checkNumber(sweepStop)*xScaleFactor, checkNumber(sweepNum))
    elif ax.xScale == 'lin' or ax.xScale == 'semilogy':
        x = np.linspace(checkNumber(sweepStart)*xScaleFactor, checkNumber(sweepStop)*xScaleFactor, checkNumber(sweepNum))
    # Create the plot:
    # Create the plot data for param plots, only one simulation result alowed
    # Other simulation results are simply ignored (plots would become messy).
    if funcType == 'param':
        xData, yData = stepParams(result, xVar, yVar, sweepVar, x)
        if type(xData) == dict:
            keys = sorted(xData.keys())
            for i in range(len(keys)):
                newTrace = trace([xData[keys[i]], yData[keys[i]]])
                newTrace.label = '$%s$ = %8.1e'%(sp.latex(result.stepVar), result.stepList[i])
                newTrace.color = ini.defaultColors[colNum % numColors]
                colNum += 1
                ax.traces.append(newTrace)
        else:
            newTrace = trace([xData, yData])
            newTrace.label = '$' + sp.latex(sp.Symbol(yVar)) + '$'
            newTrace.color = ini.defaultColors[colNum % numColors]
            ax.traces.append(newTrace)
            colNum += 1
    else:
        for result in results:
            if not result.step:
                if result.dataType == 'numer':
                    yData = result.numer
                    yLabel = 'numer: '
                elif result.dataType == 'denom':
                    yData = result.denom
                    yLabel = 'denom: '
                elif result.dataType == 'laplace':
                    yData = result.laplace
                    yLabel = ''
                elif result.dataType == 'time':
                    yData = result.time
                    yLabel = '$' + sp.latex(sp.Symbol(result.detLabel)) + '$'
                elif result.dataType == 'step':
                    yData = result.stepResp
                    yLabel = '$' + sp.latex(sp.Symbol(result.detLabel)) + '$'
                elif result.dataType == 'impulse':
                    yData = result.impulse
                    yLabel = '$' + sp.latex(sp.Symbol(result.detLabel)) + '$'
                if funcType == 'mag':
                    if ax.polar:
                        radius = magFunc_f(yData, x)
                        angle = phaseFunc_f(yData, x)
                        if ini.Hz:
                            angle = angle/180*np.pi
                        newTrace = trace([angle, radius])
                    else:
                        newTrace = trace([x, magFunc_f(yData, x)])
                elif funcType == 'dBmag':
                    if ax.polar:
                        radius = dBmagFunc_f(yData, x)
                        angle = phaseFunc_f(yData, x)
                        if ini.Hz:
                            angle = angle/180*np.pi
                        newTrace = trace([angle, radius])
                    else:
                        newTrace = trace([x, dBmagFunc_f(yData, x)])
                elif funcType == 'phase':
                    if not ax.polar:
                        newTrace = trace([x, phaseFunc_f(yData, x)])
                elif funcType == 'delay':
                    if not ax.polar:
                        newTrace = trace([x, delayFunc_f(yData, x)])
                elif funcType == 'time':
                    if not ax.polar:
                        func = sp.lambdify(sp.Symbol('t'), yData)
                        y = np.real(func(x))
                        newTrace = trace([x, y])
                if result.dataType != 'noise':
                    try:
                        newTrace.color = ini.gainColors[result.gainType]
                    except:
                        newTrace.color = ini.defaultColors[colNum % numColors]
                        colNum += 1
                    if result.gainType == 'vi':
                        yLabel += '$' + sp.latex(sp.Symbol(result.detLabel)) + '$'
                    else:
                        yLabel += result.gainType
                    try:
                        ax.traces.append(newTrace)
                    except:
                        pass
                else:
                    keys = result.onoiseTerms.keys()
                    if noiseSources == None:
                        if funcType == 'onoise':
                            yData = result.onoise
                        elif funcType == 'inoise':
                            yData = result.inoise
                        func = sp.lambdify(ini.frequency, yData)
                        # y = [func(x[j]) for j in range(len(x))]
                        y = func(x)
                        newTrace = trace([x, y])
                        newTrace.label = funcType
                        ax.traces.append(newTrace)
                    elif noiseSources == 'all':
                        for srcName in keys:
                            if funcType == 'onoise':
                                yData = result.onoiseTerms[srcName]
                            elif funcType == 'inoise':
                                yData = result.inoiseTerms[srcName]
                            func = sp.lambdify(ini.frequency, yData)
                            # y = [func(x[j]) for j in range(len(x))]
                            y = func(x)
                            noiseTrace = trace([x, y])
                            noiseTrace.color = ini.defaultColors[colNum % numColors]
                            noiseTrace.label = funcType + ': ' + srcName
                            ax.traces.append(noiseTrace)
                            colNum += 1
                    elif noiseSources in keys:
                        if funcType == 'onoise':
                            yData = result.onoiseTerms[noiseSources]
                        elif funcType == 'inoise':
                            yData = result.inoiseTerms[noiseSources]
                        func = sp.lambdify(ini.frequency, yData)
                        # y = [func(x[j]) for j in range(len(x))]
                        y = func(x)
                        noiseTrace = trace([x, y])
                        noiseTrace.color = ini.defaultColors[colNum % numColors]
                        noiseTrace.label = funcType + ': ' + sources
                        ax.traces.append(noiseTrace)
                        colNum += 1
                    elif type(noiseSources) == list:
                        for srcName in noiseSources:
                            if srcName in keys:
                                if funcType == 'onoise':
                                    yData = result.onoiseTerms[srcName]
                                elif funcType == 'inoise':
                                    yData = result.inoiseTerms[srcName]
                                func = sp.lambdify(ini.frequency, yData)
                                # y = [func(x[j]) for j in range(len(x))]
                                y = func(x)
                                noiseTrace = trace([x, y])
                                noiseTrace.color = ini.defaultColors[colNum % numColors]
                                noiseTrace.label = funcType + ': ' + srcName
                                ax.traces.append(noiseTrace)
                                colNum += 1
                    else:
                        print 'Error: cannot understand "sources=%s".'%(str(sources))
                        return fig
            else:
                if result.stepMethod != 'array':
                    stepNum = len(result.stepList)
                else:
                    stepNum = len(result.stepArray[0])
                for i in range(stepNum):
                    if result.dataType == 'numer':
                        yData = result.numer[i]
                        yLabel = 'numer: '
                    elif result.dataType == 'denom':
                        yData = result.denom[i]
                        yLabel = 'denom: '
                    elif result.dataType == 'laplace':
                        yData = result.laplace[i]
                        yLabel = ''
                    elif result.dataType == 'time':
                        yData = result.time[i]
                    elif result.dataType == 'step':
                        yData = result.stepResp[i]
                    elif result.dataType == 'impulse':
                        yData = result.impulse[i]
                    elif result.dataType == 'noise':
                        if funcType == 'onoise':
                            yData = result.onoise[i]
                        elif funcType == 'inoise':
                            yData = result.inoise[i]
                    if result.gainType == 'vi':
                        if result.dataType == 'noise':
                            yLabel = funcType
                        else:
                            yLabel += '$' + sp.latex(sp.Symbol(result.detLabel)) + '$'
                    else:
                        yLabel = result.gainType     
                    if result.stepMethod == 'array':
                        yLabel += ', run: %s'%(i+1)
                    else:
                        yLabel += ', %s = %8.1e'%(result.stepVar, result.stepList[i])    
                    if funcType == 'mag':
                        if ax.polar:
                            radius = magFunc_f(yData, x)
                            angle = phaseFunc_f(yData, x)
                            if ini.Hz:
                                angle = angle/180*np.pi
                            newTrace = trace([angle, radius])
                        else:
                            newTrace = trace([x, magFunc_f(yData, x)])
                    elif funcType == 'dBmag':
                        if ax.polar:
                            radius = dBmagFunc_f(yData, x)
                            angle = phaseFunc_f(yData, x)
                            if ini.Hz:
                                angle = angle/180*np.pi
                            newTrace = trace([angle, radius])
                        else:
                            newTrace = trace([x, dBmagFunc_f(yData, x)])
                    elif funcType == 'phase':
                        if not ax.polar:
                            newTrace = trace([x, phaseFunc_f(yData, x)])
                    elif funcType == 'delay':
                        if not ax.polar:
                            newTrace = trace([x, delayFunc_f(yData, x)])
                    elif funcType == 'time':
                        if not ax.polar:
                            func = sp.lambdify(sp.Symbol('t'), yData)
                            y = np.real(func(x))
                            newTrace = trace([x, y])
                    elif funcType == 'onoise' or funcType == 'inoise':
                        if not ax.polar:
                            func = sp.lambdify(ini.frequency, yData)
                            #y = [func(x[j]) for j in range(len(x))]
                            y = func(x)
                            newTrace = trace([x, y])
                    newTrace.color = ini.defaultColors[colNum % numColors]
                    colNum += 1
                    newTrace.label = yLabel
                    try:
                        ax.traces.append(newTrace)
                    except:
                        pass
    fig.axes = [[ax]]
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

def plot(fileName, title, axisType, plotData, xName = '', xScale = '', xUnits = '', yName = 'auto', yScale = '', yUnits = '', show = False):
    """
    """
    fig = figure(fileName)
    fig.show = show
    ax = axis(title)
    colNum = 0
    numColors = len(ini.defaultColors)
    if axisType == 'lin':
        ax.xScale = 'lin'
        ax.yScale = 'lin'
    elif axisType == 'log':
        ax.xScale = 'log'
        ax.yScale = 'log'
    elif axisType == 'semilogx':
        ax.xScale = 'log'
        ax.yScale = 'lin'
    elif axisType == 'semilogy':
        ax.xScale = 'lin'
        ax.yScale = 'log'
    elif axisType == 'polar':
        ax.polar = True
        ax.yScale = 'lin'
    else:
        print "Error: unknown axis type '%s'."%(axisType)
        return fig
    ax.xScaleFactor = xScale
    ax.yScaleFactor = yScale
    ax.traces = []
    # Create the axis labels
    ax.xLabel = xName + ' [' + xScale + xUnits + ']'
    ax.yLabel = yName + ' [' + yScale + yUnits + ']'
    for key in sorted(plotData.keys()):
        newTrace = trace(plotData[key])
        newTrace.label = key
        newTrace.color = ini.defaultColors[colNum % numColors]
        ax.traces.append(newTrace)
        colNum += 1
    fig.axes = [[ax]]
    fig.plot()
    return fig

def stepParams(results, xVar, yVar, sVar, s):
    """
    Called by plotSweep in cases in which funcType = 'param'
    Can also be used to generate a dict with plotData for plot().
    """
    parNames = results.circuit.parDefs.keys() + results.circuit.params
    errors = 0
    xValues = {}
    yValues = {}
    # check the input
    if xVar == None:
         print "Error: missing x variable."
         errors +=1
    elif sp.Symbol(xVar) not in parNames:
        print "Error: unknown parameter: '%s' for 'x variable'."%(xVar)
        errors += 1
    if sVar == None:
         svar = xVar
    elif sp.Symbol(xVar) not in parNames:
        print "Error: unknown parameter: '%s' for sweep variable."%(xVar)
        errors += 1
    if yVar == None:
         print "Error: missing y variable."
         errors +=1
    elif sp.Symbol(yVar) not in parNames:
        print "Error: unknown parameter: '%s' for y variable."%(yVar)
        errors += 1
    if errors == 0 and results.step:
        if results.stepMethod.lower() == 'lin':
            p = np.linspace(results.stepStart, results.stepStop, num = results.stepNum)
        elif xMethod.lower() == 'log':
            p = np.geomspace(results.stepStart, results.stepStop, num = results.stepNum)
    if errors == 0:
        substitutions = {}
        for parName in results.circuit.parDefs.keys():
            if parName != sp.Symbol(sVar) and parName != results.stepVar:
                substitutions[parName] = results.circuit.parDefs[parName]\
        # Obtain the y-variable as a function of the sweep and the step variable:
        f = fullSubs(results.circuit.parDefs[sp.Symbol(yVar)], substitutions)
        # Obtain the x-variable as a function of the sweep and the step variable:
        g = fullSubs(results.circuit.parDefs[sp.Symbol(xVar)], substitutions)
        if results.step:
            for parValue in p:
                y = f.subs(results.stepVar, parValue)
                yfunc = sp.lambdify(sp.Symbol(sVar), y)
                yValues[parValue] = yfunc(s)
                if xVar != sVar:
                    x = g.subs(results.stepVar, parValue)
                    xfunc = sp.lambdify(sp.Symbol(sVar), x)
                    xValues[parValue] = xfunc(s)
                else:
                    xValues[parValue] = s
        else:
            y = sp.lambdify(sp.Symbol(sVar), f)
            yValues = y(s)
            if xVar != sVar:
                x = sp.lambdify(sp.Symbol(sVar), g)
                xValues = x(s)
            else:
                xValues = s
    return (xValues, yValues)

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
    sincos.polar = False
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