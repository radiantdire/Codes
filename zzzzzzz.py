import rados
import rbd
import subprocess
from subprocess import call

def GetHumanReadable(size,precision=2):
        suffixes=['B','KB','MB','GB','TB']
        suffixIndex = 0
        while size > 1024 and suffixIndex < 4:
                suffixIndex += 1 #increment the index of the suffix
                size = size/1024.0 #apply the division
        return "%.*f%s"%(precision,size,suffixes[suffixIndex])

def get_pool(tbs):
	ul,tl = [],[]
	ri = rbd.RBD()
	for pool in cluster.list_pools():
		ioctx1 = cluster.open_ioctx(pool)
		for image in ri.list(ioctx1):
			if tbs in image:
				print("Image found in pool "+str(pool)+" with name "+str(image)+"\n")
				return ([pool,image])


def basic(pool):
	ri = rbd.RBD()
        try:
               ioctx = cluster.open_ioctx(pool)
        except:
                exit()
        inm = ri.list(ioctx)

        ol = [str(o.key) for o in ioctx.list_objects()]
        ol.sort()
	return([ioctx,inm,ol])






def get_info():

	count=0
        il,el,inlist,tl,fl,isl1,isl2,count_list,ei = [],[],[],[],[],[],[],[],[]
        d={}
	for image in inm:
        	try:
                	il.append((str(image), str(rbd.Image(ioctx, image).stat()['block_name_prefix'].split('.')[1])))
        	except:
                	ei.append(str(image))



	for image in il:
		inlist=[]	
        	for obj in ol:
                	if image[1] in obj:
                        	count+=1
	                        inlist.append(ioctx.stat(obj)[0])

        	count_list.append(count)
		print(image[0], GetHumanReadable(int(sum(inlist))))
	        d[image] = (GetHumanReadable(int(sum(inlist))), count)
	
	print("                    Image Name                 :     Size of Image    :     Size of Snapshots    :      No of Objects")
	for key,value in d.iteritems():
        	try:
                	with rbd.Image(ioctx, key[0]) as rbd_image:
                        	        size = GetHumanReadable(int(rbd_image.size()))
                                	#print(rbd_image.size())
	                                isl1.append(rbd_image.size())
	                                isl2.append(size)
        	                        print(key[0],'    :    ',size,'    :    ', value[0],'     :     ', value[1])
	        except:
        	        pass


	print('Total no of objects : ', sum(count_list))
	print('Total size of images in long int: ', sum(isl1))
	print('Total size of images : ', GetHumanReadable(sum(isl1)))

def show_menu():
	print('\nSelect\n\n1. List Pool\n2.Delete Image\n3.Exit\n')



def do_rm(a, b, c):
	for each in ol:
		if a in each:
			ioctx.remove_object(each)
		elif b in each:
			ioctx.remove_object(each)
	call(c, shell=True)
	

if __name__ == "__main__":
	
	cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
	cluster.connect()
	show_menu()
	#pool = raw_input("Enter pool\n")
	option = raw_input()
	while(option !=3):
		if option == '1':
			pool = raw_input("Enter pool name : \n")
			tl = basic(pool)
			ioctx,inm,ol=tl[0],tl[1],tl[2]
			get_info()
		elif option == '2':
			tbs = raw_input("Enter image to be deleted : \n")
			wew = get_pool(tbs)
	
			a = str(wew[1])
			pool = str(wew[0])
			tl = basic(pool)
                        ioctx,inm,ol=tl[0],tl[1],tl[2]
			c = 'rbd remove '+pool+'/'+a
			get_info()
			b = str(rbd.Image(ioctx, tbs).stat()['block_name_prefix']).split('.')[1]
			do_rm(a,b,c)	
		elif option == '3':
			exit()
		else:
			print("Wrong option\n")
		show_menu()
		option = raw_input()
	#do_rm(a,b)


