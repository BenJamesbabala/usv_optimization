import openmdao.api as om
from openmdao.test_suite.components.paraboloid import Paraboloid

prob = om.Problem()
model = prob.model

model.add_subsystem('p1', om.IndepVarComp('x', 0.), promotes=['*'])
model.add_subsystem('p2', om.IndepVarComp('y', 0.), promotes=['*'])
model.add_subsystem('comp', Paraboloid(), promotes=['*'])

model.add_design_var('x', lower=-10, upper=10)
model.add_design_var('y', lower=-10, upper=10)
model.add_objective('f_xy')

prob.driver = om.DOEDriver(om.UniformGenerator(num_samples=10))
#prob.driver = om.DOEDriver(om.LatinHypercubeGenerator(samples=10))
prob.driver.add_recorder(om.SqliteRecorder("cases.sql"))

prob.setup()
prob.run_driver()
prob.cleanup()

cr = om.CaseReader("cases.sql")
cases = cr.list_cases('driver')

print(len(cases))

values = []
for case in cases:
    outputs = cr.get_case(case).outputs
    values.append((outputs['x'], outputs['y'], outputs['f_xy']))

print("\n".join(["x: %5.2f, y: %5.2f, f_xy: %6.2f" % xyf for xyf in values]))
