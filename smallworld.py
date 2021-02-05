import numpy as np
import random
import matplotlib
import matplotlib.pyplot as plt

#number of nodes
size = 100
#connectivity
spread = 7
diff = int(spread/2)
#threshold choices
probs = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
# number of simulation runs
runs = 1000

def ammendlist(neighbors, id, p=0.3):

	new_neigh = []
	for i in range(len(neighbors)):

		rand = random.random()

		if rand > p:
			new_neigh.append(neighbors[i])

		else:
			new_connect = random.randint(0,size-1)

			while new_connect == id:
				new_connect = random.randint(0,size-1)

			new_neigh.append(new_connect)

	return new_neigh

def reconnect(p=0.3):
	for i in range(len(network)):
		network[i] = ammendlist(network[i], i, p)

def populate():
	for i in range(size):
		network[i] = []
		for j in range(spread):
			n = (i+j-diff) % size
			if i != n:
				network[i].append(n)

def bfs(start,goal):

	frontier = [start]
	frontier_tracker = set()
	frontier_tracker.add(start)
	explored = set()
	nodes_expanded = 0
	goal_state = False

	parents = dict()

	while len(frontier) > 0:
		state = frontier.pop(0)
		explored.add(state)

		if state == goal:
			goal_state = state
			break
		else:
			children = network[state]
			nodes_expanded += 1

			for child in children:
			    
				if (child not in explored) and (child not in frontier_tracker):
					parents[child] = state
					frontier.append(child)
					frontier_tracker.add(child)

	if not goal_state:
		return False, False

	actions = []
	depth = 0
	visited = goal_state
	while True:

		actions.append(visited)
		if visited == start:
			break

		visited = parents[visited]
		depth += 1

	actions.reverse()
	return actions, depth

######################################################
######################################################
######################################################

avgs = []
losses = []
for p in probs:

	total_depth = 0
	total_loss = 0
	count = 0
	for i in range(runs):

		network = dict()
		populate()
		reconnect(p)

		start = random.randint(0,size-1)
		goal = random.randint(0,size-1)

		start_vec = np.array(network[start])
		mean = np.mean(start_vec)
		
		actions, depth = bfs(start,goal)

		if actions:
			total_depth = total_depth + depth
			total_loss = total_loss + abs(mean-start)**0.5
			count = count + 1

	avg = total_depth/count
	avgs.append(avg)

	avg = total_loss/count
	losses.append(avg)

depths = np.array(avgs)
depths /= np.max(np.abs(depths), axis=0)

losses = np.array(losses)
losses /= np.max(np.abs(losses), axis=0)

plt.plot(probs, depths, label="depth")  
plt.plot(probs, losses, label="loss")
plt.plot(probs, depths+losses, label="total cost")

plt.xlabel('random link probability')  
plt.ylabel('cost')  
plt.title('small world life')   
plt.legend(loc="upper left")

plt.show()  



