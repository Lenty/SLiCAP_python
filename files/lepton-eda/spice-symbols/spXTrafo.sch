v 20200319 2
C 44600 49400 1 0 1 spF.sym
{
T 44150 50700 5 6 0 0 0 6 1
device=F-spice
T 43550 50000 5 8 1 1 0 6 1
refdes=F1
T 43550 49700 5 8 1 1 0 6 1
value={-value}
T 43545 49857 5 8 1 1 0 6 1
vref=V1
}
C 43800 49400 1 0 0 spE.sym
{
T 42700 51100 5 8 0 0 0 0 1
device=E-spice
T 44300 50600 5 8 1 1 0 0 1
refdes=E1
T 44300 50450 5 8 1 1 0 0 1
value={value}
}
C 44800 48700 1 0 0 spV.sym
{
T 44800 49900 5 6 0 0 0 0 1
device=V-spice
T 45250 49000 5 8 1 1 0 0 1
value=0
T 45250 49150 5 8 1 1 0 0 1
refdes=V1
}
N 45000 50300 45500 50300 4
{
T 45100 50350 5 8 1 1 0 0 1
netname=outP
}
N 45000 48700 45500 48700 4
{
T 45100 48750 5 8 1 1 0 0 1
netname=outN
}
N 43800 50300 43250 50300 4
{
T 43700 50350 5 8 1 1 0 6 1
netname=inP
}
N 43800 49500 43250 49500 4
{
T 43700 49550 5 8 1 1 0 6 1
netname=inP
}
T 43292 49542 8 8 0 1 0 0 1
netname=inN
C 43200 50800 1 0 0 spCommand.sym
{
T 43100 51100 5 6 0 0 0 0 1
device=directive
T 43100 50900 5 8 1 1 0 0 1
refdes=A1
T 43300 50900 5 8 1 1 0 0 1
value=.subckt spXTrafo ouP outN inP inN params value=value@
}
