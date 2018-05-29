import rados
import rbd

def GetHumanReadable(size,precision=2):
        suffixes=['B','KB','MB','GB','TB']
        suffixIndex = 0
        while size > 1024 and suffixIndex < 4:
                suffixIndex += 1 #increment the index of the suffix
                size = size/1024.0 #apply the division
        return "%.*f%s"%(precision,size,suffixes[suffixIndex])


def get_info():

	count=0
        il,el,inlist,tl,fl,isl1,isl2 = [],[],[],[],[],[],[]
        d={}


	try:
		il.append((str(tbs), str(rbd.Image(ioctx, tbs).stat()['block_name_prefix'])))
	except:
		print("Image does not exist.")
		exit()

	for obj in ol:
		if il[0][1] in obj:
			count+=1
			inlist.append(ioctx.stat(obj)[0])
	d[tbs] = (GetHumanReadable(int(sum(inlist))), count)


	for key,value in d.iteritems():
        	try:
                	with rbd.Image(ioctx, key) as rbd_image:
					print("opened image")
                                	size = GetHumanReadable(int(rbd_image.size()))
	                                print(key+'    :    '+size+'    :    '+value[0], value[1])
        	except:
                	pass


def do_rm(a, b):
	for each in ol:
		if a in each:
			ioctx.remove_object(each)
		elif b in each:
			ioctx.remove_object(each)



if __name__ == "__main__":
	
	cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
	cluster.connect()

	pool = raw_input("Enter pool\n")
	tbs = raw_input("Enter image name\n")

	ri = rbd.RBD()
	ioctx = cluster.open_ioctx(pool)

	ol = [str(o.key) for o in ioctx.list_objects()]
	ol.sort()
	
	get_info()	
	
	a = tbs
	b = str(rbd.Image(ioctx, tbs).stat()['block_name_prefix']).split('.')[1]
	print(a)
	print(b)

	do_rm(a,b)


'''
for image in inm:
	try:	
		il.append((str(image), str(rbd.Image(ioctx, image).stat()['block_name_prefix'])))
	except:
		ei.append(str(image))

#for each in il:
#	print(each)

#print('\n'.join(ei))


ol.sort()
#print('\n'.join(ol))

#for each in ol:
#	print(each, GetHumanReadable(int(ioctx.stat(each)[0])))


count_list = []
d = {}
for image in il:
	inlist = []
	count = 0
	for obj in ol:
		if image[1] in obj:
			count+=1
			inlist.append(ioctx.stat(obj)[0])		
	count_list.append(count)
	d[image] = (GetHumanReadable(int(sum(inlist))), count)
#print(d)

tl = []
fl = []
isl1 = []
isl2 = []

for key,value in d.iteritems():
	try:
		with rbd.Image(ioctx, key[0]) as rbd_image:
                                size = GetHumanReadable(int(rbd_image.size()))
                        	print(rbd_image.size())
				isl1.append(rbd_image.size())
				isl2.append(size)     
				print(key[0],'    :    ',size,'    :    ', value[0], value[1])
	except:
		pass

#isl2 = [int(x.strip('L')) for x in isl2]
print('Total no of objects : ', sum(count_list))
print('Total size of images in long int: ', sum(isl1))
#print('Total size of images : ', sum(isl2))


'''
