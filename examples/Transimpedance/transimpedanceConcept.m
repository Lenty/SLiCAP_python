% Uncomment the next line if you want to update the netlist
%makeNetlist('transimpedanceConcept', 'Concept design', 'ltspice');
checkCircuit('transimpedanceConcept');
htmlPage('Concept design');
head2html('Amplifier two-port concept');
text2html(['Below you find the circuit diagram of the application ' ... 
    'in which the amplifier is modeled as a two-port with transmission-1 '...
    'parameters $at$, $bt$, $ct$, $dt$.']);
img2html('transimpedanceConcept.png', 700);
%netlist2html('transimpedanceConcept');
%elementData2html();
%params2html();
text2html(['The transfer of the amplifier does not depend on the source '...
  'and the load impedance if $at = 0$, $bt = 0$, $ct=$ $\\frac{Is}{V_{out}}$ and $dt = 0$.']);
head2html('Source-load transfer');
gainType('gain');
source('I1');
detector('V_out');
simType('numeric');
dataType('Laplace');
resultGain = execute();
% Unpack the resultGain structured array
resultGain = resultGain.results(1);
text2html('The transfer current-to-voltage transfer of this amplifier concept is:');
syms('V_out', 'I_s');
eqn2html(V_out/I_s, resultGain);
head2html('Amplifier type');
text2html('This requires an amplifier with zero input impedance and zero output impedance.');
text2html('A low-noise and power-efficient method to achieve this is to use negative feedback:');
text2html('Voltage sensing and current comparison, in other words: parallel feedback at both amplifier ports.');
script2html('transimpedanceConcept');
params();
stophtml();
