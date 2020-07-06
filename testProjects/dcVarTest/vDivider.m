% file: vDivider.m
% SLiCAP-MATLAB script file
% You should call this script from the file that performs the 
% initialization of a project for your SLiCAP-MATLAB work.
% You need to store this file as well as the circuit file(s) 
% in the project directory.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
checkCircuit('vDivider');
htmlPage('Circuit data voltage divider');
elementData2html();
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
htmlPage('DC variance analysis');
simType('symbolic');
gainType('vi');
dataType('dcvar');
detector('V_out');
result = execute();
dcVar2html(result);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
htmlPage('Standard deviation');
dcStd2html(result);
stophtml();
