% Uncomment the next line if you want to update the netlist
%makeNetlist('transimpedanceIdeal', 'Feedback concept', 'ltspice');
checkCircuit('transimpedanceIdeal');
% Create an HTML page for the schematics.
%{
htmlPage('Ideal transfer circuit diagram and netlist');
head2html('Feedback amplifier concept');
text2html(['Below you find the circuit diagram for evaluation of the ideal '...
  'transfer of the feedback transimpedance amplifier.']);
img2html('transimpedanceIdeal.png', 700);
netlist2html('transimpedanceIdeal');
elementData2html();
params2html();
%}
% Define source and detector
source('I1');
detector('V_out');
%{
% Create an HTML page for the schematics with the matrices.
htmlPage('Ideal transfer matrix equations');
text2html(['Below you find the circuit diagram for evaluation of the ideal '...
  'transfer of the feedback transimpedance amplifier.']);
img2html('transimpedanceIdeal.png', 700);
head2html('Symbolic matrix equations');
simType('symbolic');
dataType('matrix');
matrices2html(execute());
% With numeric analysis the values of parameters as they have been defined
% in parameter definitions (.param) will be substituted into the element expressions.
head2html('Circuit parameters');
text2html(['With the simulation type set to \"symbolic\", the values of the ' ...
  'parameters will be substituted into the element expressions.']);
head2html('Numeric matrix equations');
simType('numeric');
matrices2html(execute());
%}
htmlPage('Ideal gain');
text2html(['Below you find the circuit diagram for evaluation of the ideal '...
  'transfer of the feedback transimpedance amplifier.']);
img2html('transimpedanceIdeal.png', 600);
head2html('Symbolic expression for the ideal gain');
text2html(['The \"ideal gain\" of a negative feedback amplifier is defined as ' ...
  'the source-load transfer with the controller replaced by a nullor.']);
simType('symbolic');
gainType('gain');
dataType('laplace');
ideal = execute();
idealGain = ideal.results(1);
text2html('The ideal gain of the negative feedback transimpedance aplifier is obtained as:');
eqn2html(V_out/I_s, idealGain);
head2html('Hand calculation of the ideal gain');
text2html(['The ideal gain of the amplifier can easily found through '...
    'network inspection:']);
img2html('idealGainHandCalc.svg', 500);
script2html('transimpedanceIdeal');
stophtml();
