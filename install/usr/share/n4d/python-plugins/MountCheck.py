import os
import re
import xmlrpclib

class MountCheck:
	
	def __init__(self):
		
		self.autofs_lliurex_file="/etc/auto.lliurex"
		
	#def __init__
	
	
	def _is_autofs_present(self):
		
		return os.path.exists(self.autofs_lliurex_file)
		
	#def is_autofs_present
	
	
	def _get_autofs_mount_source(self):
		
		source=None
		
		if self._is_autofs_present():
			
			f=open(self.autofs_lliurex_file)
			line=f.readlines()[0].strip("\n")
			f.close()
			
			regex="(\S+)\s+(\S+)\s+(\S+)"
			ret=re.match(regex,line)
			if ret:
				source=ret.group(3).strip("/&")
				
		return source
		
	#def get_mount_source
	
	def _is_source_in_mounts(self,source):

		if source!=None:

			f=open("/proc/mounts")
			lines=f.readlines()
			f.close()
			
			for line in lines:
				if source in line:
					return True
				
		return False
		
	#def is_source_in_mounts

	
	# ### PUBLIC FUNCTIONS ### #
	
	def is_autofs_present(self):
		
		try:
			msg=self._is_autofs_present()
			return {"status": True, "msg": msg}
		except Exception as e:
			return {"status": False, "msg": str(e)}
		
	#def is_autofs_present
	
	
	def is_autofs_mounted(self):
		
		try:
			msg=False
			if self._is_autofs_present():
				source=self._get_autofs_mount_source()
				msg=self._is_source_in_mounts(source)
				
			return {"status": True, "msg": msg}
			
		except Exception as e:
			return {"status": False, "msg": str(e)}
			
	#def is_autofs_mounted


	def user_mounts_found(self,user):
		
		try:

			msg=False
			expected_mounts=["home","share","groups_share"]

			f=open("/proc/mounts")
			lines=f.readlines()
			f.close()
			
			ret=[]
			for line in lines:
				if user in line:
					ret.append(line.strip("\n"))

			if len(ret) > 0:

				mounts={}
				mounts["home"]=False
				mounts["share"]=False
				mounts["groups_share"]=False

				for mount in expected_mounts:
					for line in ret:
						if mount in line:
							mounts[mount]=True

				msg=mounts["home"] and mounts["share"] and mounts["groups_share"]
				
			return {"status": True, "msg": msg}
		
		except Exception as e:
			
			return {"status": False, "msg": str(e)}
		
		    
	#def user_mounts_found


	def is_master_alive(self):
		
		try:
			c=xmlrpclib.ServerProxy("https://10.3.0.254:9779")
			c.get_methods()
			return {"status": True, "msg": ""}
		except Exception as e:
			return {"status": False, "msg": str(e)}
		
	#def is_master_alive


	# ### ########################### ### #
	
	
#class MountTest


if __name__=="__main__":
	
	mt=MountCheck()
	source=mt._get_autofs_mount_source()
	print mt._is_source_in_mounts(source)