import rados
import rbd


def GetHumanReadable(size,precision=3):
        suffixes=['B','KB','MB','GB','TB']
        suffixIndex = 0
        while size > 1024 and suffixIndex < 4:
                suffixIndex += 1 #increment the index of the suffix
                size = size/1024.0 #apply the division
        return "%.*f%s"%(precision,size,suffixes[suffixIndex])

def cal(l):
	a,b,c,d,e = 0,0,0,0,0
	s1,s2,s3,s4,s5 = 0,0,0,0,0
	for each in l:
		if "id" in each:
			a+=1
			s1+=ioctx.stat(each)[0]
		elif "header" in each:
			b+=1
			s2+=ioctx.stat(each)[0]
		elif "map" in each:
			c+=1
			s3+=ioctx.stat(each)[0]
		elif "data" in each:
			d+=1
			s4+=ioctx.stat(each)[0]
		else:
			e+=1
			s5+=ioctx.stat(each)[0]
	print('id : ', a, GetHumanReadable(int(s1)),s1)
	print('header : ', b, GetHumanReadable(int(s2)),s2)
	print('map : ', c, GetHumanReadable(int(s3)),s3)
	print('data : ', d, GetHumanReadable(int(s4)),s4)
	print('other : ',e, GetHumanReadable(int(s5)),s5)
	if(a+b+c+d+e == len(l)):
		print("Trueeeeee")
			





cluster = rados.Rados(conffile='/etc/ceph/ceph.conf')
cluster.connect()

ri = rbd.RBD()

pool = raw_input("Enter the pool	")

ioctx = cluster.open_ioctx(pool)

inm = ri.list(ioctx)

l = [obj.key for obj in ioctx.list_objects()]
l.sort()
cal(l)

