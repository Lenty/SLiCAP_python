% file: VampFeedbackBiasTotal.m
% SLiCAP-MATLAB script file
% You should call this script from the file that performs the 
% initialization of a project for your SLiCAP-MATLAB work.
% You need to store this file as well as the circuit file(s) 
% in the project directory.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
checkCircuit('VampFeedbackBiasTotal');
%%%%% Netlist and cicuit data %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
htmlPage('Netlist and circuit data');
netlist2html('VampFeedbackBiasTotal');
elementData2html();
%%%%% Resuls of feedback biasing %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
htmlPage('Feedback biasing');
simType('symbolic');
%%%%% DC voltage
gainType('vi');
dataType('dc');
source('V1');
detector('V_out');
result = execute();
syms 'V_outDC' 'A_v';
text2html('The DC voltage $V_{outDC}$ is:');
eqn2html(V_outDC, result.results(1));
%%%%% Laplace transfer function
gainType('gain');
dataType('laplace');
result = execute();
text2html('The voltage transfer $A_v$ from source to load is:');
transfer = result.results(1);
eqn2html(A_v, transfer);
%%%%% High-frequency transfer, ratio of the coefficients of the highest 
% order of s of the numerator and the denominator of the transfer function
sCoeffs = coeffsTransfer(transfer);
nCoeffs = sCoeffs(1);
dCoeffs = sCoeffs(2);
text2html('For high frequencies, this transfer can be written as:');
eqn2html(A_v, nCoeffs(length(nCoeffs))/dCoeffs(length(dCoeffs)));
stophtml();
