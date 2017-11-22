import urllib.parse
import http.client
import xml.etree.ElementTree as ET
def connection(sparql_q):
	conn = http.client.HTTPConnection("localhost:3030")
	headers = {
	'cache-control': "no-cache",
	'postman-token': "7ddb9f0a-76e2-5c03-fbea-19a00de7f70c"
	}
	url="/ds/sparql?query="+sparql_q
	conn.request("POST", url, headers=headers)
	res = conn.getresponse()
	data = res.read()
	print(data.decode("utf-8"))
	file =open('sparql_q.xml','w')
	file.write(str(data.decode("utf-8")))
	return data.decode("utf-8")
def parse_xml():
	import xml.etree.ElementTree as ET
	tree = ET.parse('sparql_q.xml')
	root = tree.getroot()
	# print(root.tag)
	my=[]
	# for child in root:
	# 	print(child.tag, child.attrib)
	# 	for sub in child:
	# 		print(sub.get('name'))
	# 		my.append(sub.get('name'))
	# 	break;
	flag=0;
	file=open("output.txt",'w+')
	# file.write("ohk")
	for child in root:
		for sub in child:
			# print(sub.tag)
			for bindings in sub:
				print(bindings.tag)
				for literal in bindings:
					print(literal.tag+"km")
					flag=1
					# file.write("here is deal")
					if flag >= 0:
						if '#' in literal.text:
							file.write(literal.text.split('#')[1]+"\n")
						else:
							file.write(literal.text+"\n")
					else:
						flag=1
				# print(bindings.tag)
	# for sub in child:
	# 	x=sub.get('result/')
	if flag is 0:
		file.write("please ask valid question")
	# for event in root.findall('head'):
	# 	print('event')
	# 	party = event.find('variable')
	# 	if party is None:
	# 		continue
	# 	parties = party.text
	# 	print(parties)
	# 	children = event.get('value')
file = open("/home/manish/project/query_sparql.txt","r")
input_=file.read( )
quey_number=int(input_.split("\n")[1])
# print(quey_number)
file.close( )
file=open("/home/manish/project/sparql.txt","r")
input=file.read( )
input_sparql=input.split("\n\n")
for x in range(0,len(input_sparql)):
	if x%2 is 0:
		i=int(input_sparql[x].split(" ")[0])
		j=int(input_sparql[x].split(" ")[1])
		if quey_number>=i-1 and quey_number<=j-1:
			print(quey_number,i,j)
			print(input_sparql[x+1])
			connection(urllib.parse.quote_plus(input_sparql[x+1]))
			print("ohk")
			parse_xml( )
			break;


