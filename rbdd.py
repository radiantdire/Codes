





import subprocess
import rados, sys
import rbd
#from subprocess import call
#call('ceph osd pool stats volumes', shell=True)

cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')

#for each in dir(cluster):
#	print(each)

#print("\n Rados Version: " + str(cluster.version()) )

cluster.connect()

#print("\n Cluster ID: " + cluster.get_fsid())

#cs = cluster.get_cluster_stats()

#for key, value in cs.iteritems():
#	print(key, value)

#print('\n'.join(dir(cluster)))
print("\n#######\n")
print('\n'.join(cluster.list_pools()))
#print(cluster.__class__())

l = cluster.list_pools()
 
for each in l:
	
	ioctx = cluster.open_ioctx(each)

	rbd_inst = rbd.RBD()
	rbd_names = rbd_inst.list(ioctx)

	#print('\n'.join(rbd_names))
	print(each + ' 			: '+str(len(rbd_names)))

#object_iterator = ioctx.list_objects()
#print('Objectsssssssssssssssssssssssssssssssssssssssssssssssssssssssss : ', object_iterator)

'''
while True :

	try :
		rados_object = object_iterator.next()
		print "Object contents = " + rados_object.read()

	except StopIteration :
		break
'''
