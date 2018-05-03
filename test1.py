from david import David
import tensorflow as tf

import simulator
a=David()

for i in range(40):
	print(simulator.testrun(a,10))
