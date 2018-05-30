import rados,rbd
import prettytable
from prettytable import PrettyTable


def GetHumanReadable(size,precision=2):
        suffixes=['B','KB','MB','GB','TB']
        suffixIndex = 0
        while size > 1024 and suffixIndex < 4:
                suffixIndex += 1 #increment the index of the suffix
                size = size/1024.0 #apply the division
        return "%.*f%s"%(precision,size,suffixes[suffixIndex])


cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
cluster.connect()


ri = rbd.RBD()
pool = raw_input("\nEnter pool name\n\n")
ioctx = cluster.open_ioctx(pool)
il = ri.list(ioctx)



finlist = []


for img in il:
	size1 = 0
	size = 0
	nob = 0
	try : 
		with rbd.Image(ioctx, img) as image:
			size1 = image.size()
			for snap in rbd.SnapIterator(image):
				size += snap['size']
				nob+=1
		finlist.append((img, size1, size, nob))
	except (rbd.ImageNotFound):
		pass
x = PrettyTable(["Image name", "Image Size", "Snapshots Size", "No of snapshots"])
#x.set_field_align("Image name", "l")
#x.set_padding_width(1)

print('\n')
for each in finlist :
#	print(each[0]+'  :  '+str(GetHumanReadable(each[1]))+'  :  '+str(GetHumanReadable(each[2]))+'  :  '+str(each[3]))
	x.add_row([each[0], str(GetHumanReadable(each[1])), str(GetHumanReadable(each[2])), str(each[3])])
print(x)

if len(il) == 0:
	print("No images in the pool")
	exit()
else:
	inm = raw_input("\nEnter image name\n\n")


try:

	with rbd.Image(ioctx, inm) as image:
		si = rbd.SnapIterator(image)

		newl = [(x['name'],x['size']) for x in si]
	#print(GetHumanReadable(sum(newl[1])))

		for each in newl:
			image.remove_snap(each[0])
except(rbd.ImageNotFound):
	print("Image does not exist!")
	exit()
try:
	ri.remove(ioctx, inm)
	print("\n\nRemoved the image\n")
except (rbd.ImageBusy):
	print("Image is busy")

ioctx = cluster.open_ioctx(pool)
il = ri.list(ioctx)

if len(il)!= 0:
	print("List of images in pool "+pool+' : \n')
	print('\n'.join(il))
else:
	print("There are no images in the pool now.")
