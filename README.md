# usv_optimization
A collection of Python scripts that utilize OpenMDAO to provide a first order synthesis model for the design of an unmanned surface vessel, based on the US Navy's 2019 RFP for the Medium Unmanned Surface Vessel (MUSV)

### Packages Needed
+ OpenMDAO and dependents
  + OpenMDAO contains a number of dependents, not all are strictly needed for these scripts
+ pyOptSparse and dependents
  + mpi4py and petsc are very important, and improper installation appears to cause issues

## Contents
+ [Current Version](#current-version)
+ [Future Work](#future-areas-of-work)
+ [Files](#files)
  + [Run Files](#run-files)
  + [Outputs](#outputs)
  + [OpenMDAO Components](#openmdao-components)
  + [Calculation Scripts](#calculation-scripts)
+ [Deprecated Files](#deprecated-files)
+ [References](#references)

## Current Version
### (June 1, 2020)
*A version label has been added to files to track active development versus established codes.  Below are the last working versions, the version one higher is in development.*
+ Design Space Exploration – `musvDOEv3.py`
+ Multi-variable Optimization – `musvOPTv1.py` (bugs still exist)

## Future Areas of Work
- [x] Add flywheel energy storage devices to model
- [ ] Update Reliability component
- [ ] Development ratios implicit component
- [ ] More tasks...

## Files
#### Run Files
+ `musvDOEv4.py` sets up the MUSV model and executes design space exploration, writing the output to a `.sql` and `.csv` file.  v4 attempted to implement a ratios-based approach, which would first require weight and displacement balance based on dimensionless ratios as inputs.  The current setup works in some cases, but fails in most cases when there is no combination of dimensions that meets all criteria - resulting in no data at that point.  The error handling must be improved for this to be a practical method of design space exploration.
+ `musvDOEv4casePlotter.py` reads `musvDOEv4cases.csv`, downselects all designs to those considered feasbile using if-statements, and outputs a series of plots using `matplotlib.pyplot`.  
+ `musvDOEv3.py` sets up the MUSV model and executes design space exploration, writing the output to a `.sql` and `.csv` file. v3 incorporated flywheel energy storage devices in the model, producing promising initial results.  The design space exploration results in a majority of solutions being infeasible (~98% infeasible), meaning a large number of samples must be generated to produce sufficient results.  Regardless it is possible to observe trends in the results.
+ `musvDOEv3casePlotter.py` reads `musvDOEv3cases.csv`, downselects all designs to those considered feasible using if-statements, and outputs a series of plots using `matplotlib.pyplot`.  
+ `musvOPTv1.py` uses the same model as `musvDOEv3.py` but employs a driver from `pyOptSparse` to perform an NSGA2 optimization.  By my best understanding, `pyOptSparse` is a wrapper that allows OpenMDAO to interface with pre-existing optimization codes (typically written in C).  This optimization appears to work well for default options (Population size of 100, and 1000 generations) however **attempting to change these options causes the script to crash.**  Initial investigations suggest this might be related to improper installation of `mpi4py` or `petsc`, though this is still unclear.
+ `musvOPTv1Plotter.py` reads `nsga2_best_pop.out` and generates plots of all designs.  It is possible to include downselection like used in the DOE plots, however it would be more prudent to add more constraints to the optimization.
#### Outputs
+ `musvDOEv4cases.sql` is an sqlite database generated by a [solver recorder](http://openmdao.org/twodocs/versions/latest/features/recording/solver_options.html) in `musvDOEv4.py`.  It is not human-readable but can be accessed from other scripts using OpenMDAO's [CaseReader object](http://openmdao.org/twodocs/versions/latest/features/recording/case_reader.html).
+ `musvDOEv4cases.csv` is a human-readable `.csv` file containing relevant parameters of each case generated in the designs space exploration created in `musvDOEv4.py`.  The script can be modified to include more or less information in the `.csv` output.
+ `musvDOEv3cases.sql` is an sqlite database generated by a [solver recorder](http://openmdao.org/twodocs/versions/latest/features/recording/solver_options.html) in `musvDOEv3.py`.  It is not human-readable but can be accessed from other scripts using OpenMDAO's [CaseReader object](http://openmdao.org/twodocs/versions/latest/features/recording/case_reader.html).
+ `musvDOEv3cases.csv` is a human-readable `.csv` file containing relevant parameters of each case generated in the designs space exploration created in `musvDOEv3.py`.  The script can be modified to include more or less information in the `.csv` output.
+ `musvOPTv1.xlsx` this was generated manually from a successful run of `musvOPTv1.py`, by converting `nsga2_best_pop.out` to a spreadsheet-format - this was useful to decode the order of variables in `nsga2_##` files.
+ `nsga2_best_pop.out` an output generated by the NSGA2 optimization containing the final feasible population resulting from the optimization.  Note that the order of data columns is: objectives, constraints (two columns per constraint), design variables.  These are in the order they were declared in the run file but are NOT labeled in the output files.
+ `nsga2_final_pop.out` an output generated by the NSGA2 optimization containing the final population resulting from the optimization, whether this is feasible or not.  Note that the order of data columns is: objectives, constraints (two columns per constraint), design variables.  These are in the order they were declared in the run file but are NOT labeled in the output files.
+ `nsga2_initial_pop.out` an output generated by the NSGA2 optimization containing the initial population used in the optimization.  Note that the order of data columns is: objectives, constraints (two columns per constraint), design variables.  These are in the order they were declared in the run file but are NOT labeled in the output files.
+ `nsga2_params.out` an output generated by the NSGA2 optimization containing the limits and information about input variables for the optimization.
+ `nsga2_run.out` an output generated by the NSGA2 optimization with runtime information, which can be useful for debugging.
#### OpenMDAO Components
+ `Weights.py`contains the Weights component, currently configured using the the weight estimation described by Parsons in the NA470 coursepack, as defined in `weightCurves.py`.  Based on OpenMDAO [paraboloid tutorial](http://openmdao.org/twodocs/versions/latest/basic_guide/first_analysis.html).  Also contains the WeightsNoFuel component which is configured to use the Grubisic weight estimation, and requires input of fuel weight (calculated elsewhere) and engine power.
+ `Resistance.py`contains the Resistance component, currently configured using the Series 64 resistance curve as defined in `resistanceCurves.py`.  Based on OpenMDAO [paraboloid tutorial](http://openmdao.org/twodocs/versions/latest/basic_guide/first_analysis.html)
+ `Stability.py` contains the Stability component, currently configured using the GMT estimation `estGMT.py`.  Based on OpenMDAO [paraboloid tutorial](http://openmdao.org/twodocs/versions/latest/basic_guide/first_analysis.html)
+ `Fuel.py` contains the Fuel component.  This employs a fuel estimation function from `fuelEstimate.py` and is configurable to use different fuel estimation functions.
+ `Ratios.py` contains the Ratios component.  This was developed for use with `musvDOEv4.py` to utilize dimensionless ratios as input variables rather than dimensions.  This would ideally limit the number of infeasible solutions, however this component not yet functional.  There is very rudimentary error handling to reject infeasible solutions, but it is neither efficient or robust.  Use of an implicit component to accomplish this functionality is likely more important.
+ `RatiosImp.py` is an **experimental implicit component** to be used in a nested optimization, where inputs are dimensionless ratios that describe vessel principle characteristics and outputs are dimensions that fit all ratio and also balance weight and displacement.  This is very much under development.
+ `Reliability.py` contains the Reliability component, which is **still in development.**  This component will take inputs of engine run time and number of starts, and apply generate a composite probability of failure as a single metric for comparision of designs.
#### Calculation Scripts
+ `estGMT.py` contains a basic estimation of transverse metacentric height (GMT).  Note that this assumes vertical center of gravity is directly proportional to draft, which is not an ideal assumption.
+ `estParam.py` contains two scripts to calculate displacement based on variable definitions, and wetted surface area based on Grubisic 2012.
+ `resistanceCurves.py`contains the Series 64 resistance curve.  More resistance curves can be added as functions.
+ `weightCurves.py`contains the Parson's weight estimation method, and well as two weight estimates based on Grubisic 2009 (one takes fuel weight as an input, one assumes constant speed mission).  More weight estimates can be added as functions.
+ `flywheelWeight.py` contains a rudimentary estimation of the weight of a flywheel energy storage device, based on regression of commercially available models.  More weight estimates can be added as functions.
+ `poweringEstimate.py` estimates required brake propulsion power based on equations in Parsons' NA470 Coursepack
+ `fuelEstimate.py` estimates fuel weight and exports maximum engine power required based on `poweringEstimate`.  Uses a preset mission profile, currently hard-coded with parameters.  For the fuel estimate including flyhweels, flyhweel energy storage device weight is included in fuel weight.
+ `RatioWeights.py` script to attempt balancing weight and displacement for a given set of dimensionless ratios to find dimensions of a vessel. 


## Deprecated Files
*Not all deprecated files listed below. Generally, files with `test` in the filename are testing or debugging scripts, and are potentially less well documented.*
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
