import subprocess
import rados, sys
import rbd

def GetHumanReadable(size,precision=2):
	suffixes=['B','KB','MB','GB','TB']
	suffixIndex = 0
	while size > 1024 and suffixIndex < 4:
		suffixIndex += 1 #increment the index of the suffix
		size = size/1024.0 #apply the division
    	return "%.*f%s"%(precision,size,suffixes[suffixIndex])




def get_image_size(rbd_names):
	
	for each in rbd_names:
		try:
			with rbd.Image(ioctx, each) as rbd_image:
				size = GetHumanReadable(rbd_image.size())
				print(each+'		:'+str(size))
		
				
				


		except:
			continue

def get_count_images(l):

	if len(rbd_names)>0:
	        print(each + '                  : '+str(len(rbd_names)))

if __name__ == '__main__':
	
	
	cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')

	cluster.connect()

	l = cluster.list_pools()


	for each in l:
        	ioctx = cluster.open_ioctx(each)
		#print(ioctx.__sizeof__())		
		rbd_inst = rbd.RBD()

        	rbd_names = rbd_inst.list(ioctx)

		#get_count_images(l)
		if each=='images':
			get_image_size(rbd_names)

			

