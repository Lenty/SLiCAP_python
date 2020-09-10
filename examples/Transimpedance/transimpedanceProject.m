% This is a SLiCAP project file
% It initializes the project and calls SLiCAP files that are part of this project
%
% ALWAYS RUN THIS FILE IN THE PROJECT DIRECTORY
%
clear all;
close all;
tic
initProject('Transimpedance', mfilename('fullpath'));
transimpedanceSpec();
transimpedanceConcept();
transimpedanceIdeal();
transimpedanceNoise();
transimpedanceSelectGB();
transimpedance();
stophtml();
toc
% Uncomment the instruction below if you have python and sphinx installed
% system('sphinx-build rst/ sphinx/');