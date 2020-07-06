% File: VampBiasNullor.m
% SLiCAP-MATLAB script file
% You should call this script from the file that performs the 
% initialization of a project for your SLiCAP-MATLAB work.
% You need to store this file as well as the circuit file(s) 
% in the project directory.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
checkCircuit('VampBiasNullor');
htmlPage('Netlist and circuit data');
netlist2html('VampBiasNullor');
elementData2html();
htmlPage('DC analysis');
detector('V_6');
simType('symbolic');
gainType('vi');
dataType('dc');
result = execute();
DCvalue = simplify(result.results(1));
syms 'V_6'
text2html('The DC voltage $V_6$ is obtained as:');
eqn2html(V_6, DCvalue);
stophtml();
