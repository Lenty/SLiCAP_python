makeNetlist('transimpedanceSpec', 'Specifications');
checkCircuit('transimpedanceSpec');
eps2svg('transimpedanceSpec');
htmlPage('Application and specifications');
file2html('applicationDescription.txt');
head2html('Functional diagram');
text2html(['Below you find the circuit diagram of the application ' ... 
    'in which the amplifier is modeled as a two-port with transmission-1 '...
    'parameters $A_T$, $B_T$, $C_T$, $D_T$.']);
text2html('The transmission-1 two port equations are:');
syms V_i I_i A_T B_T C_T D_T V_o I_o;
eqn2html([V_i; I_i],[[A_T B_T]; [C_T D_T]]*[V_o;-I_o]);
img2html('transimpedanceSpec.svg', 500);
head2html('Peformance requirements specifications');
text2html('The table below summarizes the performance requirement specifications.');
csv2html('transimpedanceSpec');
head2html('Environment specifications');
text2html('The table below summarizes the environment specifications.');
csv2html('environmentSpec');
head2html('CostFactor specifications');
text2html('The table below summarizes the cost factor specifications.');
csv2html('costFactorSpec');
script2html('specifications');
stophtml();