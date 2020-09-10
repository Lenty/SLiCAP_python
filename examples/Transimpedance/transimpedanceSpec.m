% Uncomment the next line if you want to update the netlist
%makeNetlist('transimpedanceSpec', 'Specifications', 'ltspice');
checkCircuit('transimpedanceSpec');
htmlPage('Application and specifications');
file2html('applicationDescription.txt');
img2html('transimpedanceContext.svg', 800);
head2html('Peformance requirements specifications');
text2html('The table below summarizes the performance requirement specifications.');
csv2html('transimpedanceSpec');
head2html('Environment specifications');
text2html('The table below summarizes the environment specifications.');
csv2html('environmentSpec');
head2html('Cost factor specifications');
text2html('The table below summarizes the cost factor specifications.');
csv2html('costFactorSpec');
script2html('transimpedanceSpec');
head2html('Functional diagram of the amplifier');
text2html(['Below you find the circuit diagram of the application ' ... 
    'in which the amplifier is modeled as a two-port with transmission-1 '...
    'parameters $A_T$, $B_T$, $C_T$, $D_T$.']);
img2html('transimpedanceSpec.png', 700);
text2html('The transmission-1 two port equations are:');
syms V_i I_i A_T B_T C_T D_T V_o I_o;
eqn2html([V_i; I_i],[[A_T B_T]; [C_T D_T]]*[V_o; I_o]);
stophtml();
