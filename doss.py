import rados,rbd



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
pool = raw_input("Enter pool\n")
ioctx = cluster.open_ioctx(pool)
il = ri.list(ioctx)

print('\n'.join(il))

inm = raw_input("Enter image\n")

image = rbd.Image(ioctx, inm)

si = rbd.SnapIterator(image)
for each in si:
	print(each)

newl = [(x['name'],x['size']) for x in si]
#print(GetHumanReadable(sum(newl[1])))

for each in newl:
	image.remove_snap(each[0])

image.close()

try:
	ri.remove(ioctx, inm)
	print("removed image")
except (rbd.ImageBusy):
	print("Image is busy")

ioctx = cluster.open_ioctx(pool)
il = ri.list(ioctx)

print('\n'.join(il))
