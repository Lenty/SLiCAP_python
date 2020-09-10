% Initialization of the SLiCAP global variables do not change!
global LOG_TOKENS MSG CIR_PATH LIB_PATH SUBST_DEPTH GLOBAL_PARAMS ...
    LAPLACE DISP SEP FREQUENCY NUMERIC MATHJAX_LOCAL CIR_EXT IMG_PATH ...
    INCL_PATH CSV_PATH INSTALL_PATH
% Initialization of the built-in symbolic variables. You can add global
% variables in the symbolic definition below and assign their values in
% the GLOBAL_PARAMS structured array.
syms('k', 'q', 'T', 'U_T', 'epsilon_0', 'epsilon_SiO2', 'mu_0', 'c');
GLOBAL_PARAMS = struct( ...               % Global parameters
    'k', 1.38064852e-23, ...              % Boltzmann's constant [J/K ]
    'q', 1.60217662e-19, ...              % Electron charge [C]
    'T', 300, ...                         % Simulation temeprature [K]
    'U_T', k*T/q, ...                     % Thermal voltage [V]
    'mu_0', 4*pi*1e-7, ...                % Permeability of vacuum [H/m]
    'c',  2.99792458e+08, ...             % Speed of light [m/s]
    'epsilon_0', 1/c^2/mu_0, ...          % Permittivity of vacuum [F/m]
    'epsilon_SiO2', 3.9);                 % Relative permittivity of SiO2 [-]
% Default names and values of the SLiCAP parameters; be careful with changing
% these definitions!
FREQUENCY     = sym('f');                 % Variable for frequency [Hz].
LAPLACE       = sym('s');                 % Laplace variable
NUMERIC       = true;                     % Conversion of pi and integer
                                          % rationals to floats in
                                          % latex expressions.
DISP          = 4;                        % Number of digits for 
                                          % displaying floats.
SEP           = '\\cdot';                 % LaTeX separator of exponent 
                                          % in floating numbers; 
                                          % use '\\cdot' or '\\times'.
MSG           = english_;                 % Language for error messages
                                          % Available languages:
                                          % english_
                                          % nerderlands_
LIB_PATH      = [INSTALL_PATH, '/lib/'];  % Library search path
CIR_PATH      = 'circuits/';              % Search path for circuit files
IMG_PATH      = 'img/';                   % Default search path for images
CIR_EXT       = '.cir';                   % File extension for circuit files
INCL_PATH     = 'include/';               % Default search path for file2html()
CSV_PATH      = 'csv/';                   % Default search path for csc2html()
MATHJAX_LOCAL = false;                    % True for local rendering of 
                                          % LaTeX in HTML pages.
SUBST_DEPTH   = 10;                       % Max. number of recursive 
                                          % parameter substitutions in
                                          % expressions.
% For debug purposes only:
LOG_TOKENS  = false;                      % Set to true for displaying
                                          % the tokens of the input file.
