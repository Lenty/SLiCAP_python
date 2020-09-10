% Define 'F' as symbol for frequency.
F = sym('F');
% Uncomment the next line if you want to update the netlist
%makeNetlist('transimpedanceNoise', 'OpAmp noise budgets', 'ltspice');
checkCircuit('transimpedanceNoise');
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% PAGE 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Create an HTML page for the schematics with the netlist.
%{
htmlPage('Noise design circuit diagram and netlist');
head2html('Circuit diagram with noise sources');
text2html(['Below you find the circuit diagram of the ideal transimpedance ' ... 
  'amplifier with added noise sources.']);
text2html('During SLiCAP noise analysis, independent sources are regarded as uncorrelated noise sources.');
text2html('They need to be specified with their spectral densities:');
text2html('$V^2/Hz$ and $A^2/Hz$ for voltage sources and current sources, respectively.');
img2html('transimpedanceNoise.png', 700);
netlist2html('transimpedanceNoise');
elementData2html();
params2html();
%}
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% PAGE 2 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Symbolic noise analysis:
htmlPage('Symbolic noise analysis');
%
% Create an HTML page for the schematics.
text2html(['Below you find the circuit diagram of the ideal transimpedance ' ... 
    'amplifier with added noise sources.']);
img2html('transimpedanceNoise.png', 700);
%
% Set the data type to noise and the mimulation type to symbolic
gainType('vi');
dataType('noise');
simType('symbolic');
%
text2html('As with SPICE, noise analysis requires the definition of a detector (output).');
text2html(['For evaluation of the source-referred (input) noise, SLiCAP requires the '...
  'definition of a signal source.']);
text2html('The detector has been defined as $V_{out}$.');
detector('V_out');
% Define a source if you want to get results for source-referred noise.
source('I1');
text2html('The signal source has been defined as $I1$.');
symNoise = execute();
noise2html(symNoise);
syms('V_n', 'B');
totOnoise = RMSnoise(getOnoise(symNoise), 0, B);
head2html('Total RMS output noise');
eqn2html(V_n, totOnoise);
%
head2html('Hand calculations of the noise performance');
text2html(['The influence of the feedback resistor in the transimpedance ' ...
    'amplifier on the noise performance can be evaluated as if this ' ...
    'resistor is connected in parallel with the signal source.']);
img2html('noiseHandCalc.svg', 800);
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% PAGE 3 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Again but now numeric
htmlPage('Numeric noise analysis');
text2html(['Below you find the circuit diagram of the ideal transimpedance ' ... 
  'amplifier with added noise sources.']);
img2html('transimpedanceNoise.png', 700);
simType('numeric');
numNoise = execute();
noise2html(numNoise);
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% PAGE 4 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
htmlPage('Determine budgets for amplifier noise');
text2html(['Below you find the circuit diagram of the ideal transimpedance ' ... 
  'amplifier with added noise sources.']);
img2html('transimpedanceNoise.png', 700);
text2html('You can find a budgets for a design parameter by solving the design equations.');
text2html(['To this end, a design parameter of interest is taken as dependent variable and the specifications, ' ...
  'as well other design parameters are taken as independent variables.']);
head2html('Numeric determination of design limits');
text2html(['We can find the design limit (show-stopper value) for the spectral density $S_{v}$' ...
  ' when assuming zero for the current noise spectrum $S_{i}$.']);
text2html(['According to the specifications we want maximally 100$\\mu$V RMS output voltage noise' ...
  ' over a frequency range from 1kHz to 0.5MHz. The design question that needs to be answered here is:' ...
  ' which is the maximally allowed value for $S_{v}$ in case we neglect the contribution of $S_{i}$,' ...
  ' and vice versa.']);
text2html('Lets find the show stopper budget for $S_{v}$ by setting $S_{i}$ to zero.');
syms('S_v', 'S_i', 'real');
% Set current noise to zero.
defPar('S_i', '0');
% Obtain noise results.
result = execute();
% Calculate the noise over the frequency range of interest
tot = RMSnoise(getOnoise(result), 1e3, 0.5e6);
% Equate the total noise with 100uV and solve S_v from this equation.
sol1 = solve(tot-100E-6, S_v);
text2html('We obtain:');
eqn2html(S_v, sol1);
text2html('Let us now find the show stopper budget for $S_{i}$ by assuming zero for $S_{v}$.');
defPar('S_v', '0');
delPar('S_i');
result = execute();
tot = RMSnoise(getOnoise(result), 1e3, 0.5e6);
sol2 = solve(tot - 100E-6, S_i);
text2html('We obtain:');
eqn2html(S_i, sol2);
%
% Lets do this symbolically while keeping both spectral densities unknown.
head2html('Symbolic determination of design limits');
text2html('We can also find relations between the allowed values for $S_{v}$ and $S_{i}$');
text2html(['To do so, we need to remove the parameter definitions for both $S_{v}$ and $S_{i}$ and obtain the ' ...
  'budget for $S_{v}$ for any value of $S_{i}$ and vice versa.']);
delPar('S_v');
result = execute();
tot = RMSnoise(getOnoise(result), 1e3, 0.5e6);
sol3 = solve(tot-100E-6, S_v);
text2html('We obtain:');
eqn2html(S_v, sol3);
result = execute();
tot = RMSnoise(getOnoise(result), 1e3, 0.5e6);
sol4 = solve(tot-100E-6, S_i);
text2html('and:');
eqn2html(S_i, sol4);
%
% Design conclusions
head2html('Noise design and verification');
text2html('Hence, we need an OpAmp with a voltage noise spectrum less than (units = V/rt(Hz)):');
expr2html(sqrt(sol1));
text2html('And a current noise spectrum below (units = A/rt(Hz)):');
expr2html(sqrt(sol2));
%
% Verification of the noise behavior
% 
htmlPage('Noise verification');
head2html('Selection of the operational amplifier');
text2html('Later, it will become clear that the AD8610 can be used as operational amplifier');
text2html('This opamp has a voltage noise spectrum of 6nV/rt(Hz) and a current noise spectrum of 5fA/rt(Hz)');
defPar('S_v',36e-18);
defPar('S_i',25e-30);
simType('numeric');
result = execute();
tot = RMSnoise(getOnoise(result), 1e3, 0.5e6);
text2html('With this device, the total RMS noise voltage at the detector with this device becomes:');
eqn2html(sym('v_n'), tot);
head2html('Influence of $C_s$ in the noise performance');
text2html(['We used the largest value of $C_s$ to determine the budgets' ...
    ' for the noise contributions of the operational amplifier.']);
text2html('The plots below show the influence of $C_s$ on the noise performance of the amplifier.');
stepVar('C_s');
stepStart('10p');
stepStop('20p');
stepNum('10');
stepMethod('lin');
stepOn();
simType('numeric');
result = execute();
fig = plotInoise('Source referred noise spectrum', result, 1e3, 1e6, 100);
fig2html(fig, 'inoise.png', 600);
fig = plotOnoise('Noise spectrum at detector', result, 1e3, 1e6, 100);
fig2html(fig, 'onoise.png', 600);
goalFunction = {'totalOnoise', 1e-3, 0.5e6};
fig = plotVsStep( 'Integrated noise at detector, 1kHz ... 0.5MHz', result, goalFunction);
legend({'onoise'}, 'Location','eastoutside', 'Box', 'off');
fig2html(fig, 'int-onoise-stepC_s.png', 600);
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% PAGE 6 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
script2html('transimpedanceNoise');
stophtml();
