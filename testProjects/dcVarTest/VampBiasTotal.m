% file: VampBiasTotal.m
% SLiCAP-MATLAB script file
% You should call this script from the file that performs the 
% initialization of a project for your SLiCAP-MATLAB work.
% You need to store this file as well as the circuit file(s) 
% in the project directory.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
checkCircuit('VampBiasTotal');
htmlPage('Netlist and circuit data');
netlist2html('VampBias');
elementData2html();
htmlPage('DC variance analysis');
simType('symbolic');
gainType('vi');
dataType('dcvar');
detector('V_out');
result = execute();
dcVar2html(result);
htmlPage('Contributions to detector voltage variance');
dcVarResults = result.results(1);
dcVarSources = dcVarResults(1);
dcVarDetContribs = dcVarResults(3);
for i = 1:length(dcVarSources)
  text2html(strcat(['The contribution of ', char(dcVarSources(i)), ...
    ' to ${\\sigma}^2_{Vout}$ is:']));
  expr2html(dcVarDetContribs(i));
end
stophtml();
