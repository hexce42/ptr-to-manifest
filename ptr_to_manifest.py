#!/usr/bin/python

import dns.query
import dns.zone
import sys

#Configurations:
dnsserver = '192.168.18.156'
zones = [
#"0.10.10.IN-ADDR.ARPA",
#"0.11.10.IN-ADDR.ARPA",
#"0.194.10.IN-ADDR.ARPA",
"0.20.10.IN-ADDR.ARPA",
#"0.4.10.IN-ADDR.ARPA",
"10.168.192.IN-ADDR.ARPA",
"10.4.10.IN-ADDR.ARPA",
#"100.168.192.IN-ADDR.ARPA",
#"11.168.192.IN-ADDR.ARPA",
"12.30.172.IN-ADDR.ARPA",
"128.10.10.IN-ADDR.ARPA",
"128.168.192.IN-ADDR.ARPA",
#"128.194.10.IN-ADDR.ARPA",
"129.168.192.IN-ADDR.ARPA",
"13.168.192.IN-ADDR.ARPA",
"130.168.192.IN-ADDR.ARPA",
"149.30.172.IN-ADDR.ARPA",
"150.168.192.IN-ADDR.ARPA",
#"150.30.172.IN-ADDR.ARPA",
"152.168.192.IN-ADDR.ARPA",
"152.30.172.IN-ADDR.ARPA",
"156.30.172.IN-ADDR.ARPA",
"157.168.192.IN-ADDR.ARPA",
"157.30.172.IN-ADDR.ARPA",
"158.168.192.IN-ADDR.ARPA",
#"160.4.10.IN-ADDR.ARPA",
#"165.168.192.IN-ADDR.ARPA",
"166.168.192.IN-ADDR.ARPA",
"167.168.192.IN-ADDR.ARPA",
"168.168.192.IN-ADDR.ARPA",
"168.30.172.IN-ADDR.ARPA",
"169.168.192.IN-ADDR.ARPA",
"171.30.172.IN-ADDR.ARPA",
"173.168.192.IN-ADDR.ARPA",
"173.30.172.IN-ADDR.ARPA",
"18.168.192.IN-ADDR.ARPA",
#"192.4.10.IN-ADDR.ARPA",
"2.194.10.IN-ADDR.ARPA",
"209.127.10.IN-ADDR.ARPA",
"23.168.192.IN-ADDR.ARPA",
"25.168.192.IN-ADDR.ARPA",
#"25.30.172.IN-ADDR.ARPA",
"27.4.10.IN-ADDR.ARPA",
"31.9.10.IN-ADDR.ARPA",
#"32.168.192.IN-ADDR.ARPA",
"4.194.10.IN-ADDR.ARPA",
"45.168.192.IN-ADDR.ARPA",
"48.168.192.IN-ADDR.ARPA",
#"64.4.10.IN-ADDR.ARPA",
"66.4.10.IN-ADDR.ARPA",
#"69.30.172.IN-ADDR.ARPA",
#"71.30.172.IN-ADDR.ARPA",
#"72.168.192.IN-ADDR.ARPA",
#"72.30.172.IN-ADDR.ARPA",
#"72.31.172.IN-ADDR.ARPA",
#"73.168.192.IN-ADDR.ARPA",
#"73.30.172.IN-ADDR.ARPA",
#"73.31.172.IN-ADDR.ARPA",
#"74.168.192.IN-ADDR.ARPA",
#"74.31.172.IN-ADDR.ARPA",
#"75.168.192.IN-ADDR.ARPA",
#"75.30.172.IN-ADDR.ARPA",
#"76.168.192.IN-ADDR.ARPA",
#"76.30.172.IN-ADDR.ARPA",
#"77.168.192.IN-ADDR.ARPA",
#"77.30.172.IN-ADDR.ARPA",
#"78.168.192.IN-ADDR.ARPA",
#"78.30.172.IN-ADDR.ARPA",
#"79.168.192.IN-ADDR.ARPA",
#"79.30.172.IN-ADDR.ARPA",
"8.194.10.IN-ADDR.ARPA",
#"80.168.192.IN-ADDR.ARPA",
#"80.30.172.IN-ADDR.ARPA",
#"81.168.192.IN-ADDR.ARPA",
#"81.30.172.IN-ADDR.ARPA",
#"82.168.192.IN-ADDR.ARPA",
#"82.30.172.IN-ADDR.ARPA",
#"83.168.192.IN-ADDR.ARPA",
#"83.30.172.IN-ADDR.ARPA",
#"84.30.172.IN-ADDR.ARPA",
#"85.30.172.IN-ADDR.ARPA",
#"86.30.172.IN-ADDR.ARPA",
#"87.30.172.IN-ADDR.ARPA",
"9.168.192.IN-ADDR.ARPA",
#"96.4.10.IN-ADDR.ARPA",	
]
out_dir = '/p/manifests/services.d/dns.d/zone.d'
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
