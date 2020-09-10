% Uncomment the next line if you want to update the netlist
%makeNetlist('transimpedance', 'AD8610 transimpedance', 'ltspice');
checkCircuit('transimpedance');
%%%%%%%%%%%%%%%%%%%%%%%%%%% CIRCUIT DIAGRAM / NETLIST %%%%%%%%%%%%%%%%%%%%%
htmlPage('Transimpedance circuit diagram and netlist');
text2html(['Below you find the circuit diagram of the transimpedance' ... 
    'amplifier.']);
img2html('transimpedance.png', 600);
netlist2html('transimpedance');
elementData2html();
source('I1');
detector('V_out');
lgRef('E_O1');
%%%%%%%%%%%%%%%%%%%% ASYMPTOTIC GAIN %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
htmlPage('Asymptotic gain');
head2html('Symbolic expression for the asymptotic gain');
simType('symbolic');
gainType('asymptotic');
dataType('laplace');
asymptotic = execute();
asymptoticGain = asymptotic.results(1);
text2html(['The voltage controlled voltage source in the model of the ' ...
    'operational amplifietr is selected as loop gain reference.']);
text2html('The asymptotic gain is then found as:');
syms('Z_f_infty');
eqn2html(Z_f_infty, asymptoticGain);
head2html('Poles and zeros of the asymptotic gain');
text2html('The poles and zeros will be evaluated for the parameter values listed below:');
params2html();
text2html('With $C_c=0$, the asymptotic gain has no poles and no zeros:');
simType('numeric');
dataType('pz');
asymptoticPZG = execute();
pz2html(asymptoticPZG);
%%%%%%%%%%%%%%%%%%%%%%%%%% LOOP GAIN %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
htmlPage('Transimpedance loop gain');
text2html(['Below you find the circuit diagram of the transimpedance' ... 
    'amplifier.']);
img2html('transimpedance.png', 600);
gainType('loopgain');
dataType('laplace');
%{
simType('symbolic');
loopgainS = execute();
loopGainS = loopgainS.results(1);
head2html('Symbolic expression for the loop gain')
expr2html(loopGainS);
transferCoeffsS = coeffsTransfer(loopGainS);
coeffsTransfer2html(transferCoeffsS);
head2html('Numeric expression for the loop gain');
%}
simType('numeric');
loopgainN = execute();
loopGainN = loopgainN.results(1);
%{
text2html('The numeric expression for the loop gain is obtained as:');
expr2html(loopGainN);
transferCoeffsN = coeffsTransfer(loopGainN);
coeffsTransfer2html(transferCoeffsN);
%}
dataType('pz');
loopgainPZG = execute();
pz2html(loopgainPZG);
head3html('Discussion of the results');
text2html('The loop gain of the uncompensated amplifier has four poles:');
text2html('$p_1$: The dominant pole of the operational amplifier');
text2html('$p_2$: The dominant pole caused by $C_s$, $C_i$ and $R_f$');
text2html('$p_3$: The non-dominant pole of the operational amplifier');
text2html('$p_4$: The pole caused by $C_{\\ell}$ and $R_o$');
text2html('$z_1$: The right half plane zero originates from the transfer of the operational amplifier.');
%%%%%%%%%%%%%%%%%%%%%%%%%% HF compensation %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
htmlPage('Bandwidth and HF compensation');
text2html(['Below you find the circuit diagram of the transimpedance' ... 
    'amplifier.']);
img2html('transimpedance.png', 600);
head2html('Estimation of the MFM bandwidth');
% Use the function findServoBandwidth for the bandwidth estimation
Bws = findServoBandwidth(loopGainN);
text2html(['The estimated bandwidth, calculated as the frequency at which ' ...
  'the asymptote of the magnitude charactersitics intersects with unity, is:']);
% Unpack the results
Bw = double(Bws.lpf);
Order = int8(Bws.lpo);
text2html(strcat('The bandwidth is found as:', sprintf('%10.3e', Bw), 'Hz'));
text2html(strcat('The order of the high-frequency roll-off of the servo function:', sprintf('%d', Order), '.'));
text2html('Although the GB product of the AD8610 is two time more than required.');
text2html('This is because its input capacitance $C_i$ adds to $C_s$ and limits the achievable bandwidth.');
loopGainPZG = loopgainPZG.results(1);
loopGainPoles = double(loopGainPZG(1))/2/pi;
dominantPoles = feval(symengine, 'selectPolesOrZeros', loopGainPoles, 0, sqrt(2)*Bw);
text2html('The dominant poles are (in Hz):');
text2html(strcat('$p_1=$', sprintf('%10.3e',double(dominantPoles(1)))));
text2html(strcat('$p_2=$', sprintf('%10.3e',double(dominantPoles(2)))));
head2html('Calculation of a phantom zero');
sumOfPoles = dominantPoles(1) + dominantPoles(2);
text2html(strcat('The sum of the two dominant poles equals: $\\Sigma{p_{1,2}}=$', sprintf('%10.3e',double(sumOfPoles)), 'Hz'));
text2html(strcat('Which is less than $\\sqrt{2}$ times the achievable bandwidth, which is:', sprintf('%10.3e', sqrt(2)*Bw), 'Hz'));
f_zComp = double(-Bw^2/(sqrt(2)*Bw + sumOfPoles));
text2html(strcat('We need a phantom zero at: ', sprintf('%10.2e', f_zComp),'Hz'));
head2html('Implementation of the phantom zero');
R1 = getElementValues('R1');
C_c = double(-1/2/pi/f_zComp/R1);
text2html(strcat('$C_{3}$ implements a phantom zero. It should have a value of: $C_c=$', sprintf('%10.3e', double(C_c)),'F.'));
%
%%%%%%%%%%%%%%%%%%% POLE-ZERO and ROOT LOCUS PLOTS %%%%%%%%%%%%%%%%%%%%%%%%
%
htmlPage('Pole-zero plots and root-locus plots');
% Let us first plot the classical root locus. This requires stepping of the
% loop gain while plotting the poles of the servo function. We will also
% plot the zeros of the servo function. We first do this without
% compensation and then with compensation.
% Set the value of the compensation capacitor C_c to zero:
defPar('C_c', '0');
% Set the step variable to the DC gain of the operational amplifier: 'A_0':
stepVar('A_0');
% Lets step it linearly from zero to 1e6, in 100 steps:
stepStart('0');
stepStop('300k');
stepNum('100');
% Set the gain type to 'servo':
gainType('servo');
dataType('poles');
stepOn();
pz(1) = execute();
% Let us now add the zeros of the loop gain to the plot:
gainType('loopgain');
dataType('zeros');
stepOff();
pz(2) = execute();
fig = plotPZ('Root locus, uncompensated', pz, [-3e6 1e6], [-2e6 2e6]);
head2html('Standard root locus plots with $A_0$ as root locus variable');
fig2html(fig, 'TransimpRootLocusUncomp.svg', 600);
% Do this again for the compensated amplifier:
stepOn();
defPar('C_c', C_c);
gainType('servo');
dataType('poles');
pz(1) = execute();
gainType('loopgain');
dataType('zeros');
stepOff();
pz(2) = execute();
fig = plotPZ('Root locus, compensated', pz, [-3e6 1e6], [-2e6 2e6]);
fig2html(fig, 'TransimpRootLocusComp.svg', 600);
% Let us study the way in which the poles of the gain are affected
% by the phantom zero capacitance C_c:
head2html('Root locus plots with $C_c$ as root locus variable');
stepVar('C_c');
stepStart('0');
stepStop('2.5p');
stepNum('5');
stepOn();
gainType('gain');
dataType('poles');
result = execute();
% For plotting of poles and zeros use:
% plotPZ(< plotTitle >, < plotData >, < xLimits >, < yLimits >)
% Let us first plot all the poles and use 'auto' for x and y limits:
fig = plotPZ('Poles of gain vs. C_c', result, 'auto', 'auto');
fig2html(fig, 'TransimpGainAllPolesCompensating.svg', 600);
% Let us now use the same data and zoom in over a smaller frequency range:
fig = plotPZ('Poles of gain vs. compensation', result, [-3e6 1e6], [-2e6 2e6]);
fig2html(fig, 'TransimpGainDomPolesCompensating.svg', 600);
%
% Let us study the way in which the poles of the compensated 
% gain are affected by the source capacitance C_s:
head2html('Root locus plots with $C_s$ as root locus variable');
stepVar('C_s');
stepStart('10p');
stepStop('20p');
result = execute();
% For plotting of poles and zeros use:
% plotPZ(< plotTitle >, < plotData >, < xLimits >, < yLimits >)
% Let us first plot all the poles and use 'auto' for x and y limits:
fig = plotPZ('Poles of gain vs. C_s', result, 'auto', 'auto');
fig2html(fig, 'TransimpGainAllPolesCs.svg', 600);
% Let us now use the same data and zoom in over a smaller frequency range:
fig = plotPZ('Poles of gain vs. C_s', result, [-3e6 1e6], [-2e6 2e6]);
fig2html(fig, 'TransimpGainDomPolesCs.svg', 600);
%
% Let us study the way in which way the poles of the compensated 
% gain are affected by the load capacitance C_ell:
head2html('Root locus plots with $C_{\\ell}$ as root locus variable');
stepVar('C_ell');
stepStart('0');
stepStop('100p');
result = execute();
% For plotting of poles and zeros use:
% plotPZ(< plotTitle >, < plotData >, < xLimits >, < yLimits >)
% Let us first plot all the poles and use 'auto' for x and y limits:
fig = plotPZ('Poles of gain vs. C_l', result, 'auto', 'auto');
fig2html(fig, 'TransimpGainAllPolesCl.svg', 600);
% Let us now use the same data and zoom in over a smaller frequency range:
fig = plotPZ('Poles of gain vs. C_l', result, [-3e6 1e6], [-2e6 2e6]);
fig2html(fig, 'TransimpGainDomPolesCl.svg', 600);
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% BODE PLOTS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
htmlPage('Magnitude and phase plots');
head2html('Transfer functions of the asymptotic-gain model; uncompensated');
% Disable parameter stepping
stepOff();
% Set the value of the compensation capacitor 'C_c' to zero:
defPar('C_c', '0');
% Change the data type to 'laplace'
dataType('laplace');
% Store all the results for all gain types of the asymptotic-gain feedback model in an array called 'fbm':
% gain type = 'gain':
gainType('gain');
fbm(1) = execute();
% gain type = 'asymptotic':
gainType('asymptotic');
fbm(2) = execute();
% gain type = 'loopgain':
gainType('loopgain');
fbm(3) = execute();
% gain type = 'servo':
gainType('servo');
fbm(4) = execute();
% gain type = 'direct':
gainType('direct');
fbm(5) = execute();
fig = plotdBmag('Transimpedance feedback model uncompensated', fbm, 1e3, 1e9, 500);
fig2html(fig, 'TransimpFeedbackMagUncomp.svg', 600);
fig = plotPhase('Transimpedance feedback model uncompensated', fbm, 1e3, 1e9, 500);
fig2html(fig, 'TransimpFeedbackPhaseUncomp.svg', 600);
head2html('Transfer functions of the asymptotic-gain model; compensated');
% Repeat the above with 'C_c' set to '2.13p':
defPar('C_c', '2.13p');
% gain type = 'gain':
gainType('gain');
fbmc(1) = execute();
% gain type = 'asymptotic':
gainType('asymptotic');
fbmc(2) = execute();
% gain type = 'loopgain':
gainType('loopgain');
fbmc(3) = execute();
% gain type = 'servo':
gainType('servo');
fbmc(4) = execute();
% gain type = 'direct':
gainType('direct');
fbmc(5) = execute();
% Make the plot:
fig = plotdBmag('Transimpedance feedback model compensated', fbmc, 1e3, 1e9, 500);
fig2html(fig, 'TransimpFeedbackMagComp.svg', 600);
fig = plotPhase('Transimpedance feedback model compensated', fbmc, 1e3, 1e9, 500);
fig2html(fig, 'TransimpFeedbackPhaseComp.svg', 600);
%
%%%%%%%%%%%%%%%%%%% BODE PLOTS OF GAIN %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
htmlPage('Bode plots of gain')
stepVar('C_c');
stepStart('0');
stepStop('2.5p');
stepOn();
gainType('gain');
result = execute();
fig = plotdBmag('Transimpedance gain vs. C_c', result, 100e3, 10e6, 500); 
fig2html(fig, 'TransimpGaindBMagCompensating.svg', 600);

fig = plotMag('Transimpedance gain vs. C_c', result, 100e3, 10e6, 500);  
fig2html(fig, 'TransimpGainMagCompensating.svg', 600);

fig = plotPhase('Transimpedance gain vs. C_c', result, 100e3, 10e6, 500);  
fig2html(fig, 'TransimpGainPhaseComensating.svg', 600);
%
defPar('C_c','2.13p');
stepVar('C_s');
stepStart('10p');
stepStop('20p');
result = execute();
fig = plotdBmag('Transimpedance gain vs. C_s', result, 100e3, 10e6, 500); 
fig2html(fig, 'TransimpGaindBMagCompensated.png', 600);

fig = plotMag('Transimpedance gain vs. C_s', result, 100e3, 10e6, 500);  
fig2html(fig, 'TransimpGainMagCompensatied.svg', 600);

fig = plotPhase('Transimpedance gain vs. C_s', result, 100e3, 10e6, 500);  
fig2html(fig, 'TransimpGainPhaseComensated.svg', 600);
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% STEP RESPONSES %%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
htmlPage('Step responses');
simType('numeric');
gainType('gain');
dataType('step');

stepVar('C_c');
stepStart('0');
stepStop('2.5p');
stepNum('5');
stepMethod('lin');
t(1) = execute();
fig = plotTime('Unit step response vs. C_c', t, 0, 5e-6, 500);
ylabel('[V]');
fig2html(fig, 'stepResponses.svg', 600);
defPar('C_c','2.13p');
stepVar('C_s');
stepStart('10p');
stepStop('20p');
t = execute();
fig = plotTime('Unit step response compensated vs. C_s', t, 0, 5e-6, 500);
ylabel('[V]');
fig2html(fig, 'stepResponsesCompensated.svg', 600);
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%% MATLAB SCRIPT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
script2html('transimpedance');
stophtml();