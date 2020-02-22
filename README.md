# usv_optimization
  A basic set up Python scripts that utilize OpenMDAO to provide a first order synthesis model for the design of an unmanned surface vessel, based on the US Navy's 2019 RFP for the Medium Unmanned Surface Vessel (MUSV)

## files
*generally, files with `test` in the filename are testing or debugging scripts, and are potentially less well documented.*
+ `caseReader.py` and `cases.sql` are the generic output from a [case-recording function in OpenMDAO](http://openmdao.org/twodocs/versions/latest/basic_guide/basic_recording.html)
+ `Resistance.py`contains the Resistance component, currently configured using the Series 64 resistance curve as defined in `resistanceCurves.py`.  Based on OpenMDAO [paraboloid tutorial](http://openmdao.org/twodocs/versions/latest/basic_guide/first_analysis.html)
+ `resistanceCurves.py`contains the Series 64 resistance curve.  More resistance curves can be added as functions.
+ `Weights.py`contains the Weights component, currently configured using the the weight estimation described by Parsons in the NA470 coursepack, as defined in `weightCurves.py`.  Based on OpenMDAO [paraboloid tutorial](http://openmdao.org/twodocs/versions/latest/basic_guide/first_analysis.html)
+ `weightCurves.py`contains the Parson's weight estimation method.  More weight estimates can be added as functions.
