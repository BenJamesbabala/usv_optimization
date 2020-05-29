# usv_optimization
  A basic set up Python scripts that utilize OpenMDAO to provide a first order synthesis model for the design of an unmanned surface vessel, based on the US Navy's 2019 RFP for the Medium Unmanned Surface Vessel (MUSV)

## Last Working Versions (May 29, 2020)
*A version label has been added to files to track active development versus established codes.  Below are the last working versions, the version one higher is in development.*
+ Design Space Exploration – `musvDOEv3.py`
+ Multi-variable Optimization – `musvOPTv1.py` (bugs still exist)

## Files
#### Run Files
+ `musvDOEv4.py`
+ `musvDOEv4casePlotter.py`
+ `musvOPTv1.py`
+ `musvOPTv1Plotter.py`
#### Outputs
+ `musvDOEv4cases.sql`
+ `musvDOEv4cases.csv`
+ `musvDOEv3cases.sql`
+ `musvDOEv3cases.csv`
+ `musvOPTv1.xlsx`
+ `nsga2_best_pop.out`
+ `nsga2_final_pop.out`
+ `nsga2_initial_pop.out`
+ `nsga2_params.out`
+ `nsga2_run.out`
#### OpenMDAO Components
+ `Weights.py`contains the Weights component, currently configured using the the weight estimation described by Parsons in the NA470 coursepack, as defined in `weightCurves.py`.  Based on OpenMDAO [paraboloid tutorial](http://openmdao.org/twodocs/versions/latest/basic_guide/first_analysis.html)
+ `Resistance.py`contains the Resistance component, currently configured using the Series 64 resistance curve as defined in `resistanceCurves.py`.  Based on OpenMDAO [paraboloid tutorial](http://openmdao.org/twodocs/versions/latest/basic_guide/first_analysis.html)
+ `Stability.py` contains the Stability component, currently configured using the GMT estimation `estGMT.py`.  Based on OpenMDAO [paraboloid tutorial](http://openmdao.org/twodocs/versions/latest/basic_guide/first_analysis.html)
+ `Fuel.py`
+ `Ratios.py`
+ `RatiosImp.py`
+ `Reliability.py`
#### Calculation Scripts
+ `estGMT.py` contains a basic estimation of transverse metacentric height (GMT).  Note that this assumes vertical center of gravity is directly proportional to draft, which is not an ideal assumption.
+ `estParam.py` contains two scripts to calculate displacement based on variable definitions, and wetted surface area based on Grubisic 2012.
+ `resistanceCurves.py`contains the Series 64 resistance curve.  More resistance curves can be added as functions.
+ `weightCurves.py`contains the Parson's weight estimation method, and well as two weight estimates based on Grubisic 2009 (one takes fuel weight as an input, one assumes constant speed mission).  More weight estimates can be added as functions.
+ `flywheelWeight.py` contains a rudimentary estimation of the weight of a flywheel energy storage device, based on regression of commercially available models.  More weight estimates can be added as functions.
+ `poweringEstimate.py` estimates required brake propulsion power based on equations in Parsons' NA470 Coursepack
+ `fuelEstimate.py`
+ `RatioWeights.py`


## Deprecated Files
*generally, files with `test` in the filename are testing or debugging scripts, and are potentially less well documented.*
+ `caseReader.py` and `cases.sql` are the generic output from a [case-recording function in OpenMDAO](http://openmdao.org/twodocs/versions/latest/basic_guide/basic_recording.html)
+ `WeightsDOEtest.py` is a testing script to understand design space exploration (Design of Experiments, DOE) using the Weights component.  Based on OpenMDAO [DOE driver tutorial](http://openmdao.org/twodocs/versions/latest/features/building_blocks/drivers/doe_driver.html)
+ `test1_openMDAO.py` was a first attempt at 'optimization' using OpenMDAO.  It contains a preliminary resistance component, as well as case recording functionality.  Based on the [OpenMDAO paraboloid tutorial](http://openmdao.org/twodocs/versions/latest/basic_guide/first_optimization.html)
+ `test2_openMDAO.py` is a refined version of `test1_openMDAO.py` that incorporates better practices in developing an OpenMDAO model.
+ `test3_openMDAO.py` is a first attempt at combining two related components using OpenMDAO.  It is very much a work in progress and is loosely based on the [OpenMDAO Sellar tutorial](http://openmdao.org/twodocs/versions/latest/basic_guide/sellar.html)

## References
Grubisic, I. (2008).
Reliability of weight prediction in the small craft concept design.

Grubisic, I. and Begovic E. (2009).
Upgrading weight prediction in small craft concept design.
13th Congress of Intl. Maritime Assoc. of Mediterranean, October 2009

Grubisic, I. and Begovic E. (2012).
Reliability of attribute prediction in small craft concept design.
Sustainable Maritime Transportation and Exploitation of Sea Resources, 439-448.

Parsons, M. (2018).
NA470/NA570 Coursepack.
University of Michigan, Department of Naval Architecture and Marine Engineering
