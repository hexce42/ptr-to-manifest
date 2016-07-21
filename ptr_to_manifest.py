#!/usr/bin/python

import dns.query
import dns.zone
import sys

#Configurations:
dnsserver = ''
zones = [
]
out_dir = ''
file_prefix = 'auto_'
			
################################################

class PTRManifest:
	def __init__(self,dnsserver,zone):
		self.ptrs=dict()
		self.zone=zone
		
		try:
			z = dns.zone.from_xfr(dns.query.xfr(dnsserver, zone))
		except Exception as e:
			print "@@@@@@@@@@@@@@@@@@@@@@"
			print zone
			print "######################"
			print type(e)
			print e.args
			print e
			return
#			sys.exit()
			
		keys = z.nodes.keys()
		for key in z.nodes:
			for rdataset in  z.nodes[key].rdatasets:
				if rdataset.rdtype == 12:
					for item in rdataset.items:
						self.ptrs[key.to_text()]=item.target.to_text().rstrip('.')

	def to_text(self):
		out = str()
		keys = self.ptrs.keys()
		keys.sort()
		for key in keys:
			line = 'dns::record::ptr {\"'+key+"."+self.zone + '\": zone=>\''+self.zone+'\', host=>\''+key+'\', data=>\''+self.ptrs[key]+'\'}\n'
			out = out+line
		return out

	def to_file(self):
		fname = out_dir+'/'+file_prefix+self.zone.lower().replace('.','_')+'.pp'
		try:
			f = open (fname,'w')
		except Exception as e:
			print "@@@@@@@@@@@@@@@@@@@@@@"
			print fname
			print "######################"
			print type(e)
			print e.args
			print e
			return

		f.write('class dns::zone::ptr_'+self.zone.upper().replace('.','_')+' {\n')
		f.write(self.to_text())
		f.write('}\n')
		f.close()


if __name__ == "__main__":
#	test = PTRManifest('192.168.18.156','25.168.192.IN-ADDR.ARPA')
#	print test.ptrs.keys()
#	test.to_file()

	for zone in zones:
		print 'Creating manifest for '+zone
		manifest = PTRManifest(dnsserver,zone)
		manifest.to_file()
