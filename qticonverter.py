#import textparser
import xml.etree.ElementTree as ET
import unicodedata as UD

new_file = open("clpt_questions.txt", "w")
output = 'CLPT Python Questions\n'

manifest = ET.parse("/Users/Bryan/clpt_questions_final/imsmanifest.xml")
manifest = manifest.getroot()
resources = manifest.find('{http://www.imsglobal.org/xsd/imscp_v1p1}resources')


namespace = {'assessment_item': 'http://www.imsglobal.org/xsd/imsqti_v2p2', 'question': 'http://www.w3.org/2001/XMLSchema-instance'}
q_num = 0
choice_count =0
choice_dict = {1:'A', 2:'B', 3:'C', 4:'D', 5: 'E'}
success = 0
failed = 0
total = 0

for resource in resources:
	total += 1
	try:
		path = str(resource.get('identifier'))
		path = ("/Users/Bryan/clpt_questions_final/" + path + "/qti.xml")
		root = ET.parse(path)
		root = root.getroot()

		#output += '\n' + root.get('title') + '\n'
		q_num += 1
		prompt = ''
		head = '\nQ%d: %s\n' % (q_num, root.get('label'))
		print(head)

		item_body_list = root.findall('assessment_item:itemBody', namespace)

		try:
			for item_body in item_body_list:
				for gridrow in item_body:
					try:
						item_body_3 = gridrow[0][0]
					except:
						print('IB 3 failed')
						item_body_3 = []

					prompt_check = 0
					choice_count = 0
					try:
						g_text = gridrow.text
						print([g_text])
					except:
						print('g text failed')

					try:
						check = gridrow[0]
						check = check.text
						print([check])
						check = check.replace('\t', '')
						check = check.replace('\n', '')
						check = check.strip()
						print(check)
					except:
						print('Item Body 2 Check failed')

					try:
						check2 = item_body_3
						check2 = check2.text
						check2 = check2.replace('\t', '')
						check2 = check2.replace('\n', '')
						check2 = check2.strip()
						print(check2)
					except:
						print('Item Body 3 Check failed')	
					
					#check for prompt in class col-12
					try:
						if check != None and check != '':
							prompt += ("%s\n" % (check))
							prompt_check = 1
					except:
						print('Check output failed')
					try:
						if check2 != None and check2 != '':
							prompt += ("%s\n" % (check2))
							prompt_check = 1
					except:
						print('Check2 output failed')

					output += head + prompt


		#answer options
					for child in item_body_3:
						#prompt
						choice_p=''
						if child.tag == '{%s}%s' % (namespace["assessment_item"], 'prompt'):
							try:
								for kid in child:
									if kid.text != '' and kid.text != None:
										output +=  ("%s\n" % (kid.text))
									for baby in kid:
										if baby.text != '' and baby.text != None:
											output +=  ("%s\n" % (baby.text))
							except:
								print('Prompt fail')
							output +=  ("%s\n" % (child.text))
						#more prompt text?
						elif child.tag == '{%s}%s' % (namespace["assessment_item"], 'p'):
							try:
								output += " " + child.text + ('\n')
							except:
								print('p failed')
						#mc options
						elif child.tag == '{%s}%s' % (namespace["assessment_item"], 'simpleChoice'):
							choice_count += 1
							try:	
								choice_p = child[0].text
							except:
								choice_p = ''
							output += ('\t%s. %s%s\n' % (choice_dict[choice_count], child.text.strip(), choice_p))
						
						#inline selection
						elif child.tag == '{%s}%s' % (namespace["assessment_item"], 'inlineChoice'):
							if child.text == None:
								pass
							else:
								try:
									choice_count += 1
								except:
									print('Inline Choice count failed')
								try:
									output += ('\t%s. %s\n' % (choice_dict[choice_count], child.text))
								except:
									print('Inline output failed')
						elif child.tag == '{%s}%s' % (namespace["assessment_item"], 'pre'):
							print('Pre passed')
							try:
								output += child.text
							except:
								print('Pre failed')

						else:
							pass
						head = ''
						prompt = ''
						#end of nested for loops
			success += 1
		except:
			print('For loops failed')

		
	except:
		failed += 1	
		print('%s failed' % path)

print("%d questions numbered, %d questions passed, %d questions failed, %d total loops" % (q_num, success, failed, total))


#for child in root:
#	print(child.tag, child.attrib)








new_file.write(output)
new_file.close()