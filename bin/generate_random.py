#!/usr/bin/env python

import sys

from paramock.paramock import GeneralTools as generalTools

import matplotlib.pyplot as plt

# Generating Mock Catalogs
# This example shows the use of individual components of the mock generation tools. Each step is explained followed
# by the use of the specific function. Here we use a configuration file which is similar to the original "../data/catget.cfg".
# The only difference is the pathing for the input files in the configuration file. In the future, we will try to remove the hardcoded
# paths from the configuration file.

gt = generalTools(sys.argv[1])

# Generating flat galaxies
# The function (generate_galaxies) is used to generate the galaxies in the mock catalog. User can choose either to use a
# uniform distribution in r in [r_min, r_max] or use the distribution of r from the provided template. The example below show
# the latter use. For the former, one needs to provide the argument 'uniform=True' in the function.
r_flat, theta_flat, phi_flat = gt.generate_flat_galaxies(is_random=True)

# Save the output
# there are two options for user. One output file is in fits format to be used with other TPCF codes
# the other output is in pickle format and it stores detailed information about the mock catalog generated
gt.write_to_fits(is_random=True)

# If the user want to store everything is the catalog structure (galaxies with their corresponding rims, clumps and all)
# the user can uncomment the following line. Be cautious that this requires considerable memory and it may fail if used on
# simple laptop or desktop computer
#gt.write_to_pickle()