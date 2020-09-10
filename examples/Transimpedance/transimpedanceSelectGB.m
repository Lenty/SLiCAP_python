% Uncomment the next line if you want to update the netlist
%makeNetlist('transimpedanceSelectGB', 'OpAmp GB product budget', 'ltspice');
checkCircuit('transimpedanceSelectGB');
% Create an HTML page for the schematics.
htmlPage('GB budgetting, circuit diagram and netlist');
head2html('Transimpedance amplifier with operational amplifier.');
text2html(['Below, you find the circuit diagram of the transimpedance' ... 
    ' amplifier with an operational amplifier as controller.' ...
    ' The operational amplifier is modeled with a capacitive input' ...
    ' a resistive output and a single-pole voltage transfer.']);
img2html('transimpedanceSelectGB.png', 800);
%{
netlist2html('transimpedanceSelectGB');
elementData2html();
params2html();
%}
%%%%%%%%%%%%%%%%%%%%%%%%%% Loop gain equation %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
htmlPage('GB budgetting, loop gain evaluation');
head2html('Loop gain according to the asymptotic gain model');
head3html('Hand calculation of the loop gain');
text2html(['Below you find the equivalent circuit for evaluation of the' ...
     ' loop gain according to the asymptotic gain model for the case in'...
     ' which the VCVS of the operational amplifier is selected as loop' ...
     ' gain reference.']);
img2html('GBproductHandCalc.svg', 500);
% Define source, detector and loop gain reference variable
syms('L');
source('I1');
detector('V_out');
lgRef('E1');
simType('symbolic');
gainType('loopgain');
dataType('laplace');
result = execute();
L_s = result.results(1);
head3html('SLiCAP evaluation of the loop gain');
text2html('The loop gain can be written as:');
eqn2html(L, L_s);
text2html(['You can easily obtain the coefficients of s of the numerator and ' ...
    'the denominator of a transfer function, '...
    'with the lowest coefficient of s of the denominator normalized to unity.']);
transferCoeffs = coeffsTransfer(L_s);
numerCoeffs = transferCoeffs(1);
denomCoeffs = transferCoeffs(2);
DCloopGain = numerCoeffs(1);
third_Bw_max = -(DCloopGain/denomCoeffs(4)/8/pi^3); % store for later
coeffsTransfer2html(transferCoeffs);
head2html('Static accuracy');
text2html('The DC loop gain is obtained as:');
eqn2html(sym('L_0'), DCloopGain(1));
text2html(['For a maximum absolute value $\\delta$ of the static inaccuracy with respect to the ideal gain, '...
  'we require: $L_0 < -\\frac{1}{\\delta}$']);
head2html('Bandwidth design');
text2html('It is difficult to draw bandwidth design conclusions from such an expression.');
text2html('To do so, we need to know which poles of the loop gain are dominant.');
text2html('Since we need to select a device, we do not have this knowledge yet.');
text2html(['However, with $R_f \\gg R_{\\ell}$, the pole introduced by $C_{\\ell}$ is' ...
    ' not dominant if $\\frac{1}{2 \\pi R_{\\ell}C_{\\ell}} \\gg f_{max}$.']);
text2html(['Since this is the case, we will define $R_o=0$ and' ...
    ' $C_{\\ell}=0$ and repeat the above calculation in the second order approach below.']);
head2html('Second order approach');
defPar('R_o','0');
defPar('C_ell', '0');
delPar('R_f');
delPar('R_ell');
delPar('C_s');
simType('numeric');
result = execute();
L_s = result.results(1);
text2html('The loop gain is now obtained as:');
eqn2html(L, L_s);
text2html(['Again, we obtain the coefficients of s of the numerator and the denominator of a transfer function, '...
  'with the lowest coefficient of s of the denominator of that transfer function normalized to unity.']);
transferCoeffs = coeffsTransfer(L_s);
coeffsTransfer2html(transferCoeffs);
text2html('If all poles are dominant we obtain the lowest requirement for $G_B$.');
text2html('The coefficient of the highest order of $s$ is then a measure for the achievable bandwidth.');
%
%%%%%%%%%%%%%%%%%%%%%%%%%% SECOND ORDER G_B %%%%%%%%%%%%%%%%%%%%%%%%%%%
%
htmlPage('Determine budget for GB and $C_i$');
text2html(['If both poles of the loop gain are dominant, the squared bandwidth of the '...
  'servo function, in (rad/s)^2, is found as the absolute value of the product of the poles of the loop gain and the DC loop gain']);
text2html(['The product of the poles of the loop gain in (rad/s)^2, equals the reciprocal value of the coefficient of the highest order of s ' ...
  'of the denominator of $L$.']);
numerCoeffs = transferCoeffs(1);
denomCoeffs = transferCoeffs(2);
DCloopGain2 = numerCoeffs(1);
sqrd_Bw_max = -(DCloopGain2/denomCoeffs(3)/4/pi^2);
syms B_omega G_Bmin B_omega_3;
eqn2html(B_omega^2, sqrd_Bw_max);
GBmin = solve(sqrd_Bw_max - 0.25e12, sym('G_B'));
text2html('Since we need a bandwidth of 0.5MHz, the minimum required value for $G_B$ is found as:');
eqn2html(G_Bmin, GBmin);
defPar('C_s', '20p');
defPar('R_f', '100k');
text2html(strcat('With $C_s=$', sprintf('%10.1e', double(getElementValues('C1'))),'F, and $R_f=$', sprintf('%10.1e', double(getElementValues('R1'))),'$\\Omega$, we obtain:'));
syms('C_s', 'R_f');
eqn2html(G_Bmin, subs(GBmin, [C_s, R_f], [getElementValues('C1'), getElementValues('R1')]));
%
%%%%%%%%%%%%%%%%%%%%%%%%%% THIRD ORDER G_B %%%%%%%%%%%%%%%%%%%%%%%%%%%
%
htmlPage('Determine budget for GB, $C_i$ and $R_o$');
text2html('We have found a second-order bandwith:');
eqn2html(B_omega^2, sqrd_Bw_max);
text2html('In a similar way, we can find a third-order bandwidth if we do not ignore the pole due to $C_{\\ell}$.');
text2html('We will assume $R_o \\ll R_f$.');
text2html('We obtain:');
eqn2html(B_omega_3^3, third_Bw_max);
text2html(['The pole introduced by $C_{\\ell}$ must be considered dominant' ...
    ' if the absolute value of its frequency is smaller than two times' ...
    ' the minimum required bandwidth.']);
text2html('The absolute value $p_3$ of this frequency is found as:');
syms('C_ell', 'R_o');
p_3 = 1/(2*pi*C_ell*R_o);
eqn2html(abs(sym('p_3')),p_3);
C_ell = 20E-12;
R_oDom = double(1/(2*pi*0.5E6*C_ell));
text2html(['According to the above, the pole introduced by $C_{\\ell}$' ...
    ' must be considered dominant if $R_o$ exceeds: ', sprintf('%10.1e', R_oDom), '.']);
GBmin = solve(third_Bw_max - 1.25e17, sym('G_B'));
GBmin = subs(GBmin, [R_f, C_s, C_ell],[100E3, 20E-12, 20E-12]);
GBmin = feval(symengine, 'float', GBmin);
text2html('If so, the relation between $GB$, $C_i$ and $R_o$ becomes:');
eqn2html(G_Bmin, GBmin);
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%% STRATEGY GB Ci Ro %%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
htmlPage('HF design stragegy');
file2html('hfStrategy.html');
%
htmlPage('Summary OpAmp requirements');
text2html(['The table below is an imported .csv file. ' ...
    'It gives an overview of the requirements for the operational amplifier.']);
csv2html('opAmpSpec');
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%% MATLAB SCRIPT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
script2html('transimpedanceSelectGB');
stophtml();
