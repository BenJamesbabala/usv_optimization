import openmdao.api as om

# open database of previously saved cases
cr = om.CaseReader("cases.sql")

# get a list of cases that were recorded by the driver
driver_cases = cr.list_cases('driver')

# # report number of cases
# print(len(driver_cases))
#
# # get the first driver case and inspect the variables of interest
# case = cr.get_case(driver_cases[0])
#
# objectives = case.get_objectives()
# design_vars = case.get_design_vars()
# constraints = case.get_constraints()
#
# print(objectives['resist.R'])
# print(design_vars)
# print(constraints)
#
# # get a list of cases that we manually recorded
# print(cr.list_cases('problem'))

# get the final case and inspect the variables of interest
case = cr.get_case('final')

objectives = case.get_objectives()
design_vars = case.get_design_vars()
constraints = case.get_constraints()

print(objectives['resist.R'])
print(design_vars)
print(constraints)
