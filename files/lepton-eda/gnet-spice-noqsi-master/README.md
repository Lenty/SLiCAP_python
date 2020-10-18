# The spice-noqsi back end for lepton-netlist and gnetlist
`gnet-spice-noqsi.scm` is a "back end" for the `lepton-netlist` program, which is part of *Lepton EDA*. See <http://gpleda.org/> for details on *Lepton* and `lepton-netlist`.

The version for *gEDA* and `gnetlist` is frozen. It is tagged [here](https://github.com/noqsi/gnet-spice-noqsi/tree/geda-gaf) as *geda-gaf-release-2*.

`lepton-netlist -L where/the/.scm/file/is/ -g spice-noqsi ...` produces output in SPICE format. It is intended to allow the designer to produce schematics that can be used as input for both SPICE simulation and printed circuit layout. It supports this by providing flexible methods for mapping schematic symbol attributes into the parameters of SPICE declarations and commands.

For a tutorials and reference documentation see the
[Wiki](<https://github.com/noqsi/gnet-spice-noqsi/wiki>).
