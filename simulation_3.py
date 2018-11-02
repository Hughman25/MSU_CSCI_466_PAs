'''
Authors: Hugh Jackovich and Matthew Sagen
Date: 10/29/18
simulation_3:
'''

import network_3
import link_3
import threading
from time import sleep

##configuration parameters
router_queue_size = 0 #0 means unlimited
simulation_time = 1 #give the network sufficient time to transfer all packets before quitting




if __name__ == '__main__':
    object_L = [] #keeps track of objects, so we can kill their threads
    msg_S = "This is a very long message, of at least over 80 characters " \
            "that contain very precious information, wouldn't you like to get your hands on it?"
    #create network nodes
    client1 = network_3.Host(1)
    client2 = network_3.Host(2)
    server1 = network_3.Host(3)
    server2 = network_3.Host(4)
    #add nodes to list
    object_L.append(client1)
    object_L.append(client2)
    object_L.append(server1)
    object_L.append(server2)
    #create router forwarding tables
    #destination:outInterface
    routeTableA = {"3":0, "4":1}
    routeTableB = {"3":0}
    routeTableC = {"3":0}
    routeTableD = {"3":0, "4":1}
    #create routers
    router_a = network_3.Router(routeTableA, name='A', intf_count=2,max_queue_size=router_queue_size)
    router_b = network_3.Router(routeTableB, name='B', intf_count=1,max_queue_size=router_queue_size)
    router_c = network_3.Router(routeTableC, name='C', intf_count=1,max_queue_size=router_queue_size)
    router_d = network_3.Router(routeTableD, name='D', intf_count=2,max_queue_size=router_queue_size)
    #add routers to list
    object_L.append(router_a)
    object_L.append(router_b)
    object_L.append(router_c)
    object_L.append(router_d)


    #create a Link Layer to keep track of links between network nodes
    link_layer = link_3.LinkLayer()
    object_L.append(link_layer)
    print(len(msg_S))
    #add all the links
    #link parameters: from_node, from_intf_num, to_node, to_intf_num, mtu
    #add link between host1 and A
    link_layer.add_link(link_3.Link(client1, 0, router_a, 0, 147))
    #add link between host2 and A
    link_layer.add_link(link_3.Link(client2, 0, router_a, 1, 147))
    #add link between A interface 0 to B interface 0
    link_layer.add_link(link_3.Link(router_a, 0, router_b, 0, 147))
    #add link between A interface 1 to C interface 0
    link_layer.add_link(link_3.Link(router_a, 1, router_c, 0, 147))
    #add link between B interface 0 to D interface 0
    link_layer.add_link(link_3.Link(router_b, 0, router_d, 0, 147))
    #add link between C interface 0 to D interface 1
    link_layer.add_link(link_3.Link(router_c, 0, router_d, 1, 147))
    #add link between D interface 0 to host3 interface 0
    link_layer.add_link(link_3.Link(router_d, 0, server1, 0, 147))
    #add link between D interface 1 to host4 interface 0
    link_layer.add_link(link_3.Link(router_d, 1, server2, 0, 147))



    #start all the objects
    thread_L = []
    thread_L.append(threading.Thread(name=client1.__str__(), target=client1.run))
    thread_L.append(threading.Thread(name=client2.__str__(), target=client2.run))

    thread_L.append(threading.Thread(name=server1.__str__(), target=server1.run))
    thread_L.append(threading.Thread(name=server2.__str__(), target=server2.run))

    thread_L.append(threading.Thread(name=router_a.__str__(), target=router_a.run))
    thread_L.append(threading.Thread(name=router_b.__str__(), target=router_b.run))
    thread_L.append(threading.Thread(name=router_c.__str__(), target=router_c.run))
    thread_L.append(threading.Thread(name=router_d.__str__(), target=router_d.run))

    thread_L.append(threading.Thread(name="Network", target=link_layer.run))

    for t in thread_L:
        t.start()


    #create some send events. Source,destination,message
    client1.udt_send(1,3,msg_S)
    client2.udt_send(2,4,msg_S)


    #give the network sufficient time to transfer all packets before quitting
    sleep(simulation_time)

    #join all threads
    for o in object_L:
        o.stop = True
    for t in thread_L:
        t.join()

    print("All simulation threads joined")
