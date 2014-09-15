import pydot 
import subprocess
graph = pydot.Dot(graph_type='graph')

#Execute cpuinfo
cpuinfo = subprocess.Popen(['cpuinfo', '-d'], shell=False, stdout=subprocess.PIPE)


# NUM_ACTIVE_SOCKETS=$(cat /proc/cpuinfo | grep "physical id" | sort | uniq | wc -l)
# NUM_PHYSICAL_CORES_TOTAL=$(cat /proc/cpuinfo | egrep "core id|physical id" | tr -d "\n" | sed s/physical/\\nphysical/g | grep -v ^$ | sort | uniq | wc -l)
# NUM_PHYSICAL_CORES_PER_SOCKET=$((NUM_PHYSICAL_CORES_TOTAL/NUM_ACTIVE_SOCKETS))
# NUM_LOGICAL_CORES_TOTAL=$((NUM_ACTIVE_SOCKETS*NUM_PHYSICAL_CORES_TOTAL))
# echo Number of active sockets: $NUM_ACTIVE_SOCKETS
# echo Total number of physical cores: $NUM_PHYSICAL_CORES_TOTAL
# echo Number of physical cores per socket: $NUM_PHYSICAL_CORES_PER_SOCKET
# echo Total number of logical cores: $NUM_LOGICAL_CORES_TOTAL



number_of_active_sockets_cmd = r'cat /proc/cpuinfo | grep "physical id" | sort | uniq | wc -l'
number_of_physical_cores_cmd = r'cat /proc/cpuinfo | egrep "core id|physical id" | tr -d "\n" | sed -e s/physical/\\n\nphysical/g | grep -v ^$ | sort | uniq | wc -l'
number_of_active_sockets = int(subprocess.Popen(number_of_active_sockets_cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=False).communicate()[0])
number_of_physical_cores = int(subprocess.Popen(number_of_physical_cores_cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=False).communicate()[0])

number_of_active_sockets =2
number_of_physical_cores = 24


number_of_physical_cores_per_socket = number_of_physical_cores/number_of_active_sockets
num_logical_cores_total = 2 * number_of_physical_cores #Useful only if HT is on.


for i in range(number_of_active_sockets):
    # we can get right into action by "drawing" edges between the nodes in our graph
    # we do not need to CREATE nodes, but if you want to give them some custom style
    # then I would recomend you to do so... let's cover that later
    # the pydot.Edge() constructor receives two parameters, a source node and a destination
    # node, they are just strings like you can see
    edge = pydot.Edge("Motherboard", "Socket %d" % i)
    # and we obviosuly need to add the edge to our graph
    graph.add_edge(edge)


for i in range(number_of_active_sockets):
    # we create new edges, now between our previous lords and the new vassals
    # let us create two vassals for each lord
    for j in range(number_of_physical_cores_per_socket):
        socket_core = i
        edge = pydot.Edge("Socket %d" % i, str(i)+'_Core Id %d' %j)
        graph.add_edge(edge)

# ok, we are set, let's save our graph into a file
graph.write_png('example1_graph.png')


# and we are done!