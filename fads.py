import numpy as np
import random
import matplotlib
import matplotlib.pyplot as plt

pop=100
spread = 9
diff = int(spread/2)
n_zero = 0
steps = 10
n_activated = 0
lifespan = 5
n_seeds = 30

#keep array of activated nodes
activated = []

network = dict()
mu, sigma = .4, 0.2
s = np.random.normal(mu, sigma, 100)



for i in range(pop):
	node = dict()
	node['act'] = 0

	thr = s[i]
	max_t = .9
	if thr > max_t:
		thr = max_t
	elif thr < 0:
		thr = 0
		node['act'] = 1
		node['step_lit'] = 0
		n_zero = n_zero + 1
		n_activated+=1
		
	
	node['thr'] = thr
	node['links'] = []
	for j in range(spread):
		n = (i+j-diff) % pop
		if i != n:
			node['links'].append(n)
	network[i] = node



for i in range(n_seeds):
	seed = random.randint(0,99)
	network[seed]['act'] = 1
	network[seed]['step_lit'] = 0
	n_activated+=1
	

for k in range(steps):
	n_changed = 0
	net_copy = network.copy()
	for i in range(len(network)):

		if network[i]['act'] == 0:

			on = 0
			links = network[i]['links']
			total = len(links)
			for j in range(total):
				if net_copy[links[j]]['act'] == 1:
					on = on + 1
			act = on/total

			if act > network[i]['thr']:
				network[i]['act'] = 1
				n_changed = n_changed + 1
				network[i]['step_lit'] = k+1
				n_activated+=1
				

		else:
			step_lit = network[i]['step_lit']
			if k-step_lit == lifespan:
				network[i]['act'] = 0
				n_activated-=1
				
	print(len(activated))

n_act = 0
for i in range(len(network)):
	if network[i]['act'] == 1:
		n_act = n_act + 1

print(n_act)