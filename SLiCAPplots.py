#!/usr/bin/python

"""
SLiCAP module with plot functions.

Imported by the module SLiCAPhtml.py

"""
from SLiCAPpythonMaxima import *

class trace(object):
    """
    Trace prototype. 
    
    Traces are plotted on axes, which are part of a figure.    
    
    :param traceData: list with list array-like X and Y data of the trace.
    :type traceData: list
    
    :Example:
        
    >>> x_data = np.linspace(0, 2*np.pi, 50)
    >>> y_data = np.sin(x_data)
    >>> sin_trace = trace([x_data, y_data])    
    """
    def __init__(self, traceData):
        self.xData = np.array(traceData[0])
        """
        Array-like data for the x-axis of the trace. On a polar axes this is 
        the angle in radians.
        """
        
        self.yData = np.array(traceData[1])
        """
        Array-like data for the y-axis of the trace. On a polar axes this is 
        the radius.
        """
        
        try:
            if len(self.xData) != len(self.yData):
                print 'Error in plot data.'
        except:
            pass
        
        self.xName = 'x' 
        """
        Heading (*str*) for the x column of a table. Defaults to 'x'.
        """
        
        self.yName = 'y'
        """
        Heading (*str*) for the y column of a table. Defaults to 'y'.
        """
        
        self.label = ''
        """
        Trace label (*str*) that will be displayed in legend box. Defaults to ''.
        """
        
        self.color = False
        """
        Trace color (*str*) in matplotlib format. Defaults to False.
        """
        
        self.marker = False
        """
        Marker type (*str*) in matplotlib format. Defaults to False.
        """
        
        self.markerColor = False
        """
        Marker color (*str*) in matplotlib format. Defaults to False.
        """
        
        self.markerFaceColor = 'none'
        """
        Marker face color (*str*) in matplotlib format. Defaults to 'none'.
        """
        
        self.markerSize = 7 
        """
        Marker size (*int*). Defaults to 7.
        """
        
        self.lineWidth = 2
        """
        Line width (*int*) in pixels. Defaults to 2.
        """
        
        self.lineType = '-'
        """
        Line type (*str*) in matplotlib format. Defaults to '-'.
        """
    
    def makeTable(self):
        """
        Returns a table with trace data in CSV format.
        
        :return: table: CSV table with column headings and x-data and y-data in
                 columns
        :rtype: str
    
        :Example:
            
        >>> x_data = np.linspace(0, 2*np.pi, 10)
        >>> y_data = np.sin(x_data)
        >>> sin_trace = trace([x_data, y_data]) 
        >>> sin_trace.yName = 'sin(x)'
        >>> print sin_trace.makeTable()
        x,sin(x)
          0.000000000000e+00,   0.000000000000e+00
          6.981317007977e-01,   6.427876096865e-01
          1.396263401595e+00,   9.848077530122e-01
          2.094395102393e+00,   8.660254037844e-01
          2.792526803191e+00,   3.420201433257e-01
          3.490658503989e+00,  -3.420201433257e-01
          4.188790204786e+00,  -8.660254037844e-01
          4.886921905584e+00,  -9.848077530122e-01
          5.585053606382e+00,  -6.427876096865e-01
          6.283185307180e+00,  -2.449293598295e-16
        """
        table = str(self.xName) + ',' + str(self.yName) + '\n'
        for i in range(len(self.xData)):
            table += '%20.12e,%20.12e'%(self.xData[i], self.yData[i]) + '\n'
        return table
        
class axis(object):
    """
    Axis prototype.
    
    :param title: Title of the axis. The title will be placed on top of the axis.
    :type title: str
    """
    
    def __init__(self, title):
        self.title = title
        """
        Title (*str*) of the axis, will be placed on top of the axis
        """
        
        self.xLabel = False
        """
        Label (*str*) for the x-axis, e.g. 'frequency [Hz]'. Defaults to False.
        """
        
        self.yLabel = False 
        """
        Label (*str*) for the x-axis, e.g. 'voltage [V]'. Defaults to False.
        """
        
        self.xScale = 'lin'
        """
        Scale (*str*) for the x-axis can be 'lin' or 'log'. Defaults to 'lin'.
        """
        
        self.yScale = 'lin'
        """
        Scale (*str*) for the y-axis can be 'lin' or 'log'. Defaults to 'lin'.
        """
        
        self.xLim = []
        """
        Limits (*list*) for the x-scale: [<xMin>, <xMax>]. Defaults to [].
        """
        
        self.yLim = []
        """
        Limits (*list*) for the y-scale: [<yMin>, <yMax>]. Defaults to [].
        """
        
        self.traces = []
        """
        List with **SLiCAPplots.trace** objects to be plotted on this axis: 
        [<trace1>(,<trace2>,...,<traceN>)]. Defaults to [].
        """
        
        self.text = [0, 0, '']
        """
        Text (*[int, int, str]*) with relative plot position: [<xPos>, <yPos>, <text>].
        Defaults to [0, 0, ''].
        """
        
        self.polar = False
        """
        (*bool*) True if a polar axis is required. Defaults to False.
        """
        
        self.xScaleFactor = ''
        """
        Scale factor (*str*) for the x-scale; e.g. M for 1E6. Defaults to ''.
        """
        self.yScaleFactor = ''
        """
        Scale factor (*str*) for the y-scale; e.g. M for 1E6. Defaults to ''.
        """
        return

class figure(object):
    """
    Prototype SLiCAP figure object.
    
    :param fileName: Name of the file for saving the figure.
    :type fileName: str
    """
    def __init__(self, fileName):
        
        self.fileType = ini.figureFileType
        """
        Graphic file type (*str*) for saving the figure. Defaults to fileName
        """
        
        self.axisHeight = ini.figureAxisHeight
        """
        Relative height (*int, float*) of a single axis. Defaults to ini.figureAxisHeight.
        
        To do: absolute measures in inch or cm.
        """
        
        self.axisWidth = ini.figureAxisWidth
        """
        Relative width (*int, float*) of a single axis. Defaults to ini.figureAxisWidth.
        
        To do: absolute measures in inch or cm.
        """
        
        self.axes = []
        """
        List with **SLiCAPplots.axis** objects to be plotted on this figure. 
        Defaults to [].
        """
        
        self.show = False
        """
        (*bool*) if 'True' the figure will be displayed with the method 
        **SLiCAPplots.figure.plot()**. Defaults to [].
        """
        
        self.fileName = fileName + '.' + ini.figureFileType
        """
        File name of the figure. Defaults to: fileName + '.' + ini.figureFileType.
        """
        
    def plot(self):
        """
        Creates the figure, displays it if SLiCAPplots.figure.show == True and 
        saves it to disk.
        """
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
        # Create the axes with their plots
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
                    if axesList[i].text:
                        X, Y, txt = axesList[i].text
                        plt.text(X, Y, txt, fontsize = ini.plotFontSize)  
                    # Set default font sizes and grid
                    defaultsPlot()
        # Save the figure"
        plt.savefig(ini.imgPath + self.fileName)
        if self.show:
            plt.show()
        plt.close(fig)
        return
        
def defaultsPlot():
    """
    Applies default settings for plots.
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
                             
def plotSweep(fileName, title, results, sweepStart, sweepStop, sweepNum, sweepVar = 'auto', sweepScale = '', xVar = 'auto', xScale = '', xUnits = '', axisType = 'auto', funcType = 'auto', yVar = 'auto', yScale = '', yUnits = '', noiseSources = None, show = False):
    """
    Plots a function by sweeping one variable and optionally stepping another. 
    
    The function to be plotted depends on the arguments 'yVar' and 'funcType':
    
    - If funcType == 'params', the variable 'yVar' must be the name of a circuit
      parameter.
    - If funcType == 'auto', the default function that will be plotted depends 
      on the data type of the instruction:
          
      - data type == 'noise': funcType = 'onoise'
      - data type == 'laplace', 'numer' or 'denom': funcType = 'mag'
      - data type == 'time', 'impulse' or 'step': funcType = 'time'
      
    The variable plotted along the x-axis defaults to the sweep variable. However,
    for multivariate functions obtained with data type 'params', the x variable 
    can be choosen from all circuit parameters.
    
    - If sweepVar == 'auto', the sweep variable will be determined from the data type:
        
      - data type == 'noise', 'laplace', 'numer' or 'denom': sweepVar = ini.frequency
        for data types 'laplace', 'numer' or 'denom' the laplace variable will
        be replaced with sympy.i*ini.frequency or with 2*sympy.pi*sympy.i*ini.frequency
        before sweeping, when ini.Hz == False, or ini.Hz== True, respectively.
      - dataType == 'time', 'impulse' or 'step': sweepVar = sympy.Symbol('t')
    
    The type of axis can be 'lin', 'log', 'semilogx', 'semilogy' or 'polar'.
    
    :param fileName: Name of the file for saving it to disk.
    :type fileName: str
        
    :param title: Title of the figure.
    :type title: str
    
    :param results: Results of the execution of an instruction, or a list with
                    SLiCAPprotos.allResults objects.
    :type results: list, SLiCAPprotos.allResults
    
    :param sweepStart: Start value of the sweep parameter
    :type sweepStart: float, int, str
    
    :param sweepStop: Stop value of the sweep parameter
    :type sweepStop: float, int, str
    
    :param sweepNum: Number of points of the sweep parameter
    :type sweepNum: int
    
    :param sweepVar: Name of the sweep variable
    :type sweepVar: sympy.Symbol, str
    
    :param sweepScale: Scale factor of the sweep variable. Both the start and 
                       the stop value will be multiplied with a factor that
                       corresponds with this scale factor.
    :type sweepScale: str
    
    :param xVar: Name of the variable to be plotted along the x axis
    :type xvar: str, sympy.Symbol
    
    :param xScale: Scale factor of the x axis variable.
    :type xScale: str
    
    :param xUnits: Units of the x axis variable.
    :type xUnits: str
    
    :param axisType: Type of axis: 'lin', 'log', 'semilogx', 'semilogy' or 'polar'.
    :type axisType: str
    
    :param funcType: Type of function can be: 'mag', 'dBmag', 'phase', 'delay',
                     'time', 'onoise', 'inoise' or 'param'.
    :type funcType: str
    
    :param yScale: Scale factor of the y axis variable.
    :type yScale: str
    
    :param yUnits: Units of the y axis variable.
    :type yUnits: str
    
    :param noiseSources: Noise sources of which the contribution to the detector-
                         referred noise (funcType = 'onoise') or the source-
                         referred noise (funcType = 'inoise') should be plotted.
                         Can be 'all', a list with names of noise sources or an
                         ID of a noise source.
    :type noiseSources: list, str
    
    :param show: If 'True' the plot will be shown in the workspace.
    :type show: bool
    
    :return: fig
    :rtype: SLiCAPplots.figure
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
    Creates a pole-zero scatter plot. 
    
    If parameter stepping of the instruction is enabled, a root locus is drawn 
    with the parameter as root locus variable.
    
    In such cases special begin end endpoint markers are used:
        
    - poles begin of root locus: 'x'
    - poles end of root locus: '+'
    - zeros begin of root locus: 'o'
    - zeros end of root locus: 'square'
    
    The root locus itself is drawn with dots for each position of a pole or zero.
    
    Results of multiple analysis can be combined in one plot by putting them in
    a list.
    
    The type of the axis is 'lin'.
    
    :param fileName: Name of the file for saving it to disk.
    :type fileName: str
        
    :param title: Title of the figure.
    :type title: str
    
    :param results: Results of the execution of an instruction, or a list with
                    SLiCAPprotos.allResults objects. The data type of these
                    instructions should be 'poles', 'zeros' or 'pz'.
    :type results: list, SLiCAPprotos.allResults
    
    :param xmin: Minimum value of the x axis; defaults to None.
    :type xmin: int, float, str
    
    :param xmax: Maximum value of the x axis; defaults to None.
    :type xmax: int, float, str
    
    :param ymin: Minimum value of the y axis; defaults to None.
    :type ymin: int, float, str
    
    :param ymax: Maximum value of the y axis; defaults to None.
    :type ymax: int, float, str
    
    :param xscale: x axis scale factor; defaults to ''.
    :type xscale: str
    
    :param yscale: y axis scale factor; defaults to ''.
    :type yscale: str
    
    :param show: If 'True' the plot will be shown in the workspace. Defaults to False.
    :type show: bool
    
    :return: fig
    :rtype: SLiCAPplots.figure
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
    if type(results) != list:
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
                print "Error: wrong data type '%s' for 'plotPZ()'."%(result.dataType)
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

def plot(fileName, title, axisType, plotData, xName = '', xScale = '', xUnits = '', yName = '', yScale = '', yUnits = '', show = False):
    """
    Plots x-y data, or multiple pairs of x-y data. 
    
    :param fileName: Name of the file for saving it to disk.
    :type fileName: str
        
    :param title: Title of the figure.
    :type title: str
    
    :param axisType: Type of axis: 'lin', 'log', 'semilogx', 'semilogy' or 'polar'.
    :type axisType: str
    
    :param plotData: List of lists with pairs of x data and y data.
    :type plotData: list
    
    :param xName: Name of the variable to be plotted along the x axis. Defaults to ''.
    :type xName: str
    
    :param xScale: Scale factor of the x axis variable. Defaults to ''.
    :type xScale: str
    
    :param xUnits: Units of the x axis variable. Defaults to ''.
    :type xUnits: str
    
    :param yName:  Name of the variable to be plotted along the y axis. Defaults to ''.
    :type funcType: str, sympy.Symbol
    
    :param yScale: Scale factor of the y axis variable. Defaults to ''.
    :type yScale: str
    
    :param yUnits: Units of the y axis variable. Defaults to ''.
    :type yUnits: str
    
    :param show: If 'True' the plot will be shown in the workspace.
    :type show: bool
    
    :return: fig
    :rtype: SLiCAPplots.figure
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

def stepParams(results, xVar, yVar, sVar, sweepList):
    """
    Returns parameter values as a result of sweeping and stepping parameters.
        
    Called by **SLiCAPplots.plotSweep()** in cases in which funcType = 'param'.
    
    - If parameter stepping is enabled it returns a tuple with two dictionaries:
        
        #. {stepVal[j]: [xVal[i] for i in range(len(sweepValues))], ...}
        #. {stepVal[j]: [yVal[i] for i in range(len(sweepValues))], ...}
        
    - If parameter stepping is disabled it returns a tuple with two lists:
        
        #. [xVal[i] for i in range(len(sweepValues))]
        #. [yVal[i] for i in range(len(sweepValues))]
    
    :param results: Results of the execution of an instruction with data type 'params'.
    :type results: SLiCAPprotos.allResults
    
    :param xVar: Name of the parameter to be plotted along the x axis
    :type xvar: str
    
    :param yVar: Name of the parameter to be plotted along the y axis
    :type yvar: str
    
    :param sVar: Name of the sweep parameter
    :type svar: str
    
    :param sweepList: Array-like sweep values.
    :type sweepList: list, numpy.array
    
    :return: parameter values as a result of sweeping and stepping parameters.
    :rtype: tuple
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
                yValues[parValue] = yfunc(sweepList)
                if xVar != sVar:
                    x = g.subs(results.stepVar, parValue)
                    xfunc = sp.lambdify(sp.Symbol(sVar), x)
                    xValues[parValue] = xfunc(sweepList)
                else:
                    xValues[parValue] = sweepList
        else:
            y = sp.lambdify(sp.Symbol(sVar), f)
            yValues = y(sweepList)
            if xVar != sVar:
                x = sp.lambdify(sp.Symbol(sVar), g)
                xValues = x(sweepList)
            else:
                xValues = sweepList
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
    sincos.text = [3.14, 0.1, '$blah_9^{14}$']
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