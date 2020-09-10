htmlPage('Summary OpAmp requirements');
text2html(['The table below is an imported .csv file. ' ...
    'It gives an overview of the requirements for the operational amplifier.']);
csv2html('opAmpSpec');
stophtml();