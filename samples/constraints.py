"""This sample checks if particles or a polymer added to the system obey(s) constraints."""

from __future__ import print_function
import espressomd

# Check if necessary features have been compiled
#############################################################

required_features = ["LENNARD_JONES"]
espressomd.assert_features(required_features)

from espressomd import thermostat
from espressomd import interactions
from espressomd import shapes
from espressomd import polymer

import numpy as np

# System parameters
#############################################################

system = espressomd.System(box_l=[50.0, 50.0, 50.0])
system.seed = system.cell_system.get_state()['n_nodes'] * [1234]
np.random.seed(seed=system.seed)

# if no seed is provided espresso generates a seed

system.time_step = 0.01
system.cell_system.skin = 10.0
system.thermostat.set_langevin(kT=1.0, gamma=1.0)
system.cell_system.set_n_square(use_verlet_lists=False)

system.non_bonded_inter[0, 0].lennard_jones.set_params(
    epsilon=1, sigma=1,
    cutoff=2**(1. / 6), shift="auto")

num_part = 30

# create random positions in the box sufficiently away from the walls
ran_pos = np.random.uniform(low=1, high=49, size=(num_part,3))
system.part.add(id=np.arange(num_part), pos=ran_pos, type=np.zeros(num_part,dtype=int))

# bottom wall, normal pointing in the +z direction, laid at z=0.1
floor = shapes.Wall(normal=[0, 0, 1], dist=0.1)
c1 = system.constraints.add(
    particle_type=0, penetrable=False, only_positive=False, shape=floor)

# top wall, normal pointing in the -z direction, laid at z=49.9, since the normal direction points down, dist is -49.9
ceil = shapes.Wall(normal=[0, 0, -1], dist=-49.9)
c2 = system.constraints.add(
    particle_type=0, penetrable=False, only_positive=False, shape=ceil)


# create_polymer will avoid violating the contraints

fene = interactions.FeneBond(k=30, d_r_max=2)
system.bonded_inter.add(fene)
# start it next to the wall to test it!
start = np.array([1, 1, 1])

#polymer.create_polymer(N_P=1, bond_length=1.0, MPC=50, start_id=num_part, start_pos=start, type_poly_neutral=0, type_poly_charged=0,  bond=fene, constraints=1)


# Warmup
#############################################################

warm_steps = 200
warm_n_times = 100
min_dist = 0.9

lj_cap = 5
system.force_cap = lj_cap
i = 0
act_min_dist = system.analysis.min_dist()
system.thermostat.set_langevin(kT=0.0, gamma=1.0)

# warmp with zero temperature to remove overlaps
while ( act_min_dist < min_dist or c1.min_dist()<min_dist or c2.min_dist()<min_dist):
    for j in range(warm_steps+lj_cap):
        print(j)
        system.integrator.run(1)
#    system.integrator.run(warm_steps + lj_cap)
    # Warmup criterion
    act_min_dist = system.analysis.min_dist()
    i += 1
    lj_cap = lj_cap + 1
    system.force_cap = lj_cap

lj_cap = 0
system.force_cap = lj_cap
system.integrator.run(warm_steps)

# ramp up to simulation temperature
temp = 0
while (temp < 1.0):
    system.thermostat.set_langevin(kT=temp, gamma=1.0)
    system.integrator.run(warm_steps)
    temp += 0.1
system.thermostat.set_langevin(kT=1.0, gamma=1.0)
system.integrator.run(warm_steps)


for t in range(300):
    system.integrator.run(1000)
    # print the position to see if it stays within imposed constraints
    print(system.part[0].pos)
