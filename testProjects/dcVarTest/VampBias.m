% file: VampBias.m
% SLiCAP-MATLAB script file
% You should call this script from the file that performs the 
% initialization of a project for your SLiCAP-MATLAB work.
% You need to store this file as well as the circuit file(s) 
% in the project directory.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
checkCircuit('VampBias');
htmlPage('Netlist and circuit data');
netlist2html('VampBias');
elementData2html();
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
htmlPage('DC variance analysis');
simType('symbolic');
gainType('vi');
dataType('dcvar');
detector('V_out');
dcVar2html(execute());
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
htmlPage('Biasing results');
dataType('dc');
result = execute();
DCvalue = result.results(1);
syms 'V_out' 'sigma_Vout'
head2html('The DC output voltage');
text2html('The DC output voltage is obtained as:');
eqn2html(V_out, DCvalue);
dataType('dcvar');
result = execute();
DCvarResult = result.results(1);
detRefVar = DCvarResult(5);       % Detector-referred variance
head2html('DC output voltage variance');
text2html('The variance of the DC output voltage is obtained as:');
eqn2html((sigma_Vout)^2, detRefVar);
stophtml();