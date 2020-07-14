#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 21:01:21 2020

@author: anton
"""

from SLiCAP import *
# Always run SLiCAP from the project directory, this will define the correct path settings.
t1=time()

prj = initProject('My first RC network') # Sets all the paths and creates the HTML main index page.

fileName = 'myFirstRCnetwork.cir'
i1 = instruction()                       # Creates an instance of an instruction object
i1.checkCircuit(fileName)                # Checks and defines the local circuit object and
                                         # sets the index page to the circuit index page
# We will generate a HTML report (not from within Jupyter). Let us first create an empty HTML page:
htmlPage('Circuit data')
# Put a header on this page and display the circuit diagram on it.
head2html('Circuit diagram')
img2html('myFirstRCnetwork.svg', 250, caption = 'Circuit diagram of the RC network.', label = 'figRCnetwork')
netlist2html(fileName, label = 'netlist') # This displays the netlist
elementData2html(i1.circuit, label = 'elementData') # This shows the data of the expanded netlist
params2html(i1.circuit, label = 'params') # This displays the circuit parameters
# Let us define an instruction to display the symbolic MNA matrix equation.
# This is done by defining attributes of the instruction object 'i1'
i1.simType = 'symbolic';
i1.gainType = 'vi';
i1.dataType = 'matrix';
# We execute the instruction and assign the result to a variable 'MNA'
MNA = i1.execute();
# We will put the instruction on a new HTML page and display it in this notebook
htmlPage('Matrix equations')
# Let us put some explaining text in the report:
text2html('The MNA matrix equation for the RC network is:')
matrices2html(MNA, label = 'MNA')
# The variables in this equation are available in the variable that holds 
# the result of the execution:
#
# 1. The vector 'Iv' with independent variables:
text2html('The vector with independent variables is:')
eqn2html('I_v', MNA.Iv, label = 'Iv')
# 2. The matrix 'M':
text2html('The MNA matrix is:')
eqn2html('M', MNA.M, label = 'M')
# 3. The vercor wit dependent variables 'Dv':
text2html('The vector with dependent variables is:')
eqn2html('D_v', MNA.Dv, label = 'Dv')
# Let us now evaluate the transfer function of this network.
# To this end we need to define a signal source and a detector.
# Both the source and the detector are attributes of the instruction object:
i1.source   = 'V1'    # 'V1' is the identifier of the independent source that we assign as signal source
i1.detector = 'V_out' # 'V_out' is the voltage at node 'out' with respect to ground (node '0')
# The transfer from source to load is called 'gain'. Later we will discuss more transfer types.
i1.gainType = 'gain'
# The data that we would like to obtain is the Laplace transfer of the gain. SLiCAP has many different 
# data types. The data type for an instruction is also an attribute of the instruction object:
i1.dataType = 'laplace'
# SLiCAP performs symbolic calculations, even when the data is numeric. In those case SLiCAP calculates
# with rationals. Only in a limited number of cases SLiCAP calculates with floats.
# Numeric values or combined numeric/symbolic expressions can be assigned to circuit parameters. In cases
# in which the simulation type is set to 'numeric' such definitions are substituted recursively.
#
# Let us display the transfer symbolically. In this case we have no parameters defined, so 'numeric' will
# give the same answer as 'symbolic'.
i1.simType = 'symbolic'
# Let us execute the (modified) instruction 'i1' and assign the result to the variable gain:
gain = i1.execute()
# The laplace transform can now be found in the attribute 'laplace' of 'gain'.
eqn2html('V_out/V_1', gain.laplace, label = 'gainLaplace')
# The parameters 'R' and 'C' stem from the circuit, while 's' is defined as the Laplace variable:
print(ini.Laplace)
# SLiCAP has a lot of predefined plots. The results of an analysis with data type 'laplace' can
# graphically be represented with:
# 1. magnitude plots versus frequency
# 2. dB magnitude plots versus frequency
# 3. phase plots versus frequency
# 4. (group) delay plots versus frequency
# For plotting we need numeric values:
i1.simType = 'numeric' 
numGain = i1.execute() 
# We will create a new HTML page for the plots
htmlPage('Plots')
head2html('Frequency domain plots')
figMag = plotMag('RCmag', 'Magnitude characteristic', numGain, 10, '100k', 100, yunits = '-')
# This will put the figure on the HTML page with a width of 800 pixels, a caption and a label:
fig2html(figMag, 600, caption = 'Magnitude characteristic of the RC network.', label = 'figMag')
figdBmag = plotdBmag('RCdBmag', 'dB magnitude characteristic', numGain, 10, '100k', 100)
fig2html(figdBmag, 600, caption = 'dB Magnitude characteristic of the RC network.', label = 'figdBmag')
figPhase = plotPhase('RCphase', 'Phase characteristic', numGain, 10, '100k', 100,)
fig2html(figPhase, 600, caption = 'Phase characteristic of the RC network.', label = 'figPhase')
# We will display the delay in 'us'
figDelay = plotDelay('RCdelay', 'Group delay characteristic', numGain, 10, '100k', 100, yscale = 'u')
fig2html(figDelay, 600, caption = 'Group delay characteristic of the RC network.', label = 'figDelay')
# With data type: 'pz' we can calculate the DC value of the gain and the poles and the zeros.
# This data type requires numeric component values.
i1.dataType = 'pz'
pzGain      = i1.execute()
# We will create a new HTML page for displaying the results and display them also in this notebook.
htmlPage('Poles and zeros')
pz2html(pzGain, label = 'PZlist')
# Let us also add a pole-zero plot of these results:
head2html("Complex frequency domain plots")
figPZ = plotPZ('PZ', 'Poles and zeros of the RC network', pzGain)
# You can also set the range and the units of the axes of this plot:
# We will redefine the figure object 'figPZ'
figPZ = plotPZ('PZ', 'Poles and zeros of the RC network', pzGain, xmin = -1.9, xmax = 0.1, ymin = -1, ymax = 1, xscale = 'k', yscale = 'k')
fig2html(figPZ, 600, caption = 'Poles and zeros of the RC network.', label = 'figPZ');
# The data types 'poles' and 'zeros' can be used to calculate the poles and the zeros separately. 
# The difference with data type 'pz' is that the latter one cancels poles and zeros that coincide
# withing the display accuracy (ini.disp) and calculated the zero-frequency value of the transfer.
# Displaying the result of all three data types gives you the DC gain and the non observable poles.
#
# With data types 'impulse' and 'step' you can calculate the impulse response and the step response
# of the network, respctively. These responses are obtained from the inverse Laplace transform of
# the transfer function (impulse response) or the transfer function multiplied with 1/ini.Laplace.
i1.dataType = 'step'
numStep = i1.execute()
figStep = plotTime('step', 'Unit step response', numStep, 0, 1, 50, xscale='m')
# Let us put this plot on the page with the plots. You can get a list with page names by typing: 'ini.htmlPages'
ini.htmlPage = 'my-first-RC-network_Plots.html'
head2html('Time domain plots')
fig2html(figStep, 600, caption = 'Unit step response of the RC network.', label = 'figStep')
# SLiCAP is developed for setting up and solving circuit design equations
# In the following section we will write the values of the circuit
# components as a function of the setting time to n bit.
# The procedure is as follows:
# 1. Get a symbolic expression of the output voltage as a function of time
# 2. Get a symbolic expression for the settling error delta_t as function of time
# 3. Find the settling tau_s by solving: delta_t = 2^(-n)
# 4. Find the design equations for  the component values:
#    a. Write the resistance 'R_R1' as a function of 'n', 'tau_s' and 'C'
#    b. Write the capacitance 'C_R1' as a function of 'n', 'tau_s' and 'R'
#
# Let us first create a new page for the above:
htmlPage('Design equations for $R$ and $C$')
head2html('The unit step response')
# Step 1:
i1.simType  = 'symbolic'
i1.dataType = 'step'
symStep     = i1.execute()
mu_t        = sp.Symbol('mu_t')
eqn2html(mu_t, symStep.stepResp, label = 'mu_t')
# Step 2:
head2html("The settling error versus time")
t             = sp.Symbol('t')
settlingError = sp.limit(symStep.stepResp, t, 'oo') - symStep.stepResp
epsilon_t     = sp.Symbol('epsilon_t')
eqn2html(epsilon_t, settlingError, label = 'epsilon_t')
# Step 3:
head2html("The n-bit settling time")
n            = sp.Symbol('n')
settlingTime = sp.solve(settlingError - 2**(-n), t)[0] # In this case there is only one solution
tau_s        = sp.Symbol('tau_s')
eqn2html(tau_s, settlingTime, label = 'tau_s')
# Step 4a:
head2html("The design equation for $R$")
R    = sp.Symbol('R')
RR1  = sp.solve(settlingTime - tau_s, R)[0] # In this case there is only one solution
eqn2html(R, RR1, label = 'RR1')
# Step 4b:
head2html("The design equation for $C$")
C    = sp.Symbol('C')
CC1  = sp.solve(settlingTime - tau_s, C)[0] # In this case there is only one solution
eqn2html(C, CC1, label = 'CC1')
head2html("Numeric example.")
text2html("We will determine R for the case in which we need 10 bit settling within 100ns with a capacitance C=10pF. We obtain:")
Rvalue = sp.N(RR1.subs([(tau_s, 100e-9), (n, 10), (C, 1e-11)]), ini.disp)
eqn2html(R, Rvalue, label = 'Rvalue')
#
htmlPage('Data summary')
#
head2html('Plots')
#
text2html(href('figMag'       , 'Magnitude plot' ))
text2html(href('figdBmag'     , 'dB Magnitude plot' ))
text2html(href('figPhase'     , 'Phase plot' ))
text2html(href('figDelay'     , 'Group delay plot' ))
text2html(href('figPZ'        , 'Pole-zero plot' ))
text2html(href('figStep'      , 'Step response plot' ))
#
head2html('Equations')
#
text2html(href('MNA'          , 'MNA matrix equation'))
text2html(href('Iv'           , 'Vector with independent variables'))
text2html(href('M'            , 'MNA matrix'))
text2html(href('Dv'           , 'Vector with dependent variables'))
text2html(href('gainLaplace'  , 'Laplace transfer function of the RC network'))
text2html(href('PZlist'       , 'Poles and zeros of the RC network'))
text2html(href('mu_t'         , 'Symbolic expression of the step response'))
text2html(href('epsilon_t'    , 'Symbolic expression of the settling error versus time'))
text2html(href('tau_s'        , 'Symbolic expression of the settling time'))
text2html(href('RR1'          , '$R(n, \\tau_s, C)$'))
text2html(href('CC1'          , '$C(n, \\tau_s, R)$'))
text2html(href('Rvalue'       , 'Numeric value of $R$ for 10 bit settling within 100ns with C=10pF'));
#
head2html('Circuit data')
text2html(href('figRCnetwork' , 'Circuit diagram'))
text2html(href('netlist'      , 'Netlist'))
text2html(href('elementData'  , 'Element data'))
text2html(href('params'       , 'Circuit parameters'))
t2 = time()
print "Total time: %3.1fs"%(t2-t1)