from dimod import BinaryQuadraticModel
from dwave.system import DWaveSampler, EmbeddingComposite
model =BinaryQuadraticModel('BINARY')

pumps=[0,1, 2 ,3, 4]
time = [0, 1, 2]
costs=[[10, 12, 15],[12, 13, 12],[14, 16, 12],[15, 16, 17],[7, 8, 20]]
flow=[2, 3, 4, 7, 5]
demand=15
x=[[f'P_{p}_1',f'P_{p}_2',f'P_{p}_3'] for p in pumps]
for p in pumps:
    for t in time:
        model.add_variable(x[p][t],costs[p][t])

#Adding Constraints
for p in pumps:
    c1=[(x[p][t], 1) for t in time]
    model.add_linear_inequality_constraint(c1,
    lagrange_multiplier=10,
    label="c1_pump_"+str(p),lb=1,ub=len(pumps))

c2=[(x[p][t],flow[p]) for t in time for p in pumps]
model.add_linear_equality_constraint(c2,
lagrange_multiplier=10,
constant=-demand)

sampler=EmbeddingComposite(DWaveSampler())
sampleset=sampler.sample(model,num_reads=1000)
sample=sampleset.first.sample
print(sample)