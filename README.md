# usv_optimization
  A basic set up Python scripts that utilize OpenMDAO to provide a first order synthesis model for the design of an unmanned surface vessel, based on the US Navy's 2019 RFP for the Medium Unmanned Surface Vessel (MUSV)

## files
*generally, files with `test` in the filename are testing or debugging scripts, and are potentially less well documented.*
+ `caseReader.py` and `cases.sql` are the generic output from a [case-recording function in OpenMDAO](http://openmdao.org/twodocs/versions/latest/basic_guide/basic_recording.html)
+ `Resistance.py`contains the Resistance component, currently configured using the Series 64 resistance curve as defined in `resistanceCurves.py`.  Based on OpenMDAO [paraboloid tutorial](http://openmdao.org/twodocs/versions/latest/basic_guide/first_analysis.html)
+ `resistanceCurves.py`contains the Series 64 resistance curve.  More resistance curves can be added as functions.
+ `Weights.py`contains the Weights component, currently configured using the the weight estimation described by Parsons in the NA470 coursepack, as defined in `weightCurves.py`.  Based on OpenMDAO [paraboloid tutorial](http://openmdao.org/twodocs/versions/latest/basic_guide/first_analysis.html)
+ `WeightsDOEtest.py` is a testing script to understand design space exploration (Design of Experiments, DOE) using the Weights component.  Based on OpenMDAO [DOE driver tutorial](http://openmdao.org/twodocs/versions/latest/features/building_blocks/drivers/doe_driver.html)
+ `weightCurves.py`contains the Parson's weight estimation method.  More weight estimates can be added as functions.
+ `test1_openMDAO.py` was a first attempt at 'optimization' using OpenMDAO.  It contains a preliminary resistance component, as well as case recording functionality.  Based on the [OpenMDAO paraboloid tutorial](http://openmdao.org/twodocs/versions/latest/basic_guide/first_optimization.html)
+ `test2_openMDAO.py` is a refined version of `test1_openMDAO.py` that incorporates better practices in developing an OpenMDAO model.
+ `test3_openMDAO.py` is a first attempt at combining two related components using OpenMDAO.  It is very much a work in progress and is loosely based on the [OpenMDAO Sellar tutorial](http://openmdao.org/twodocs/versions/latest/basic_guide/sellar.html)
