from bs4 import BeautifulSoup
import json
import csv
finaldata = {}

va_sections = set([])
di_sections = set([])
qa_sections = set([])
sections = ["va", "di", "qa"]

pages = ['03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '25']
# pages = ['03', '04']

for current_page in pages:
	url = 'analysis/19'+current_page+'_files/aimcat_performance.html'
	test_name = "AIMCAT19"+current_page
	data = {}
	print(url)
	raw_html = open(url).read()
	soup = BeautifulSoup(raw_html, 'html.parser')
	# print(soup.prettify())
	# Each section is in a table with class table-bordered
	tables = soup.findAll("table", {"class": "table-bordered"})
	# When we enumerate tables we can get index in tx
	for tx, table in enumerate(tables):
		data[sections[tx]] = {}
		# topicRows represents tr elements inside a table. These represent the table header and the table body rows
		topicRows = table.findAll("tr")
		# topicData is data inside a single row of the table
		for topicData in topicRows[1:]:
		# In each row, we need to save topic name, question numbers and attempt stats
			r = [0, 0, 0]
			w = [0, 0, 0]
			u = [0, 0, 0]
			# this is the td element with topic name
			topic = topicData.find("th", {"class": "aim-left"})
			# this is the td element with number of questions in the current topic
			qNos = int(topicData.select("td:nth-of-type(1)")[0].text)
			# this is the td that represents attempted questions. In each td there are multiple spans which contain an anchor tag and a font tag inside it
			attempted = topicData.select("td:nth-of-type(2)")[0].findAll("span")
			# We will take each span element and explore it
			for attempts in attempted:
				a_class = attempts["class"][0]
				# span > a > font > "<question number>/<difficulty level>" and we need only the last character for difficulty level as we are classifying VE in E and VD in D
				a_level = attempts.select("a > font")[0].text.strip()[-1]
				# print("class: ", a_class)
				# print("level: ", a_level)
				# Here we need to keep a count of right and wrong questions in attempted questions
				if(a_class=="box-green"):
					if(a_level=="D"):
						r[0] = r[0]+1
					elif(a_level=="M"):
						r[1] = r[1]+1
					elif(a_level=="E"):
						r[2] = r[2]+1
					else:
						print("error in levels ", topic, " ", tx, " ", a_class, " ", a_level)
				elif(a_class=="box-red"):
					if(a_level=="D"):
						w[0] = w[0]+1
					elif(a_level=="M"):
						w[1] = w[1]+1
					elif(a_level=="E"):
						w[2] = w[2]+1
					else:
						print("error in levels ", topic, " ", tx, " ", a_class, " ", a_level)
				else:
					print("error in class ", topic, " ", tx, " ", a_class)
			# Now we move to unattempted questions and the structure is same as before
			unattempted = topicData.select("td:nth-of-type(3)")[0].findAll("span")
			for unattempts in unattempted:
			# We don't need class information here because it doesn't represent anything more than difficulty level
				a_level = unattempts.select("a > font")[0].text.strip()[-1]
				if(a_level=="D"):
					u[0] = u[0]+1
				elif(a_level=="M"):
					u[1] = u[1]+1
				elif(a_level=="E"):
					u[2] = u[2]+1
				else:
					print("error in levels ", topic, " ", tx, " ", a_class, " ", a_level)

			data[sections[tx]][topic.text] = {"q": qNos, "r": r, "w": w, "u": u}
		
	finaldata[test_name] = data
	# print("final: ", finaldata)

# d = finaldata["AIMCAT1903"].copy()
# d.update(finaldata["AIMCAT1904"])
# print(d)

# Now we create a consolidated list of all topics in each section
for page in pages:
	test_name = "AIMCAT19"+page
	for topicName, topicData in finaldata[test_name]["va"].items():
		va_sections.add(topicName)
	for topicName, topicData in finaldata[test_name]["di"].items():
		di_sections.add(topicName)
	for topicName, topicData in finaldata[test_name]["qa"].items():
		qa_sections.add(topicName)

# print(va_sections)
# print(di_sections)
# print(qa_sections)

summary = {}
summary["va"] = {}
summary["di"] = {}
summary["qa"] = {}

# for each section
for section in va_sections:
	summary["va"][section] = {"q":0, "r":[0, 0, 0], "w":[0, 0, 0], "u":[0, 0, 0]}
	# for each aimcat
	for page in pages:
		test_name = "AIMCAT19"+page
		if section in finaldata[test_name]["va"]:
			sectionData = finaldata[test_name]["va"][section]
			summary["va"][section]["q"] = summary["va"][section]["q"] + sectionData["q"]
			summary["va"][section]["r"][0] = summary["va"][section]["r"][0] + sectionData["r"][0]
			summary["va"][section]["r"][1] = summary["va"][section]["r"][1] + sectionData["r"][1]
			summary["va"][section]["r"][2] = summary["va"][section]["r"][2] + sectionData["r"][2]
			summary["va"][section]["w"][0] = summary["va"][section]["w"][0] + sectionData["w"][0]
			summary["va"][section]["w"][1] = summary["va"][section]["w"][1] + sectionData["w"][1]
			summary["va"][section]["w"][2] = summary["va"][section]["w"][2] + sectionData["w"][2]
			summary["va"][section]["u"][0] = summary["va"][section]["u"][0] + sectionData["u"][0]
			summary["va"][section]["u"][1] = summary["va"][section]["u"][1] + sectionData["u"][1]
			summary["va"][section]["u"][2] = summary["va"][section]["u"][2] + sectionData["u"][2]

for section in di_sections:
	summary["di"][section] = {"q":0, "r":[0, 0, 0], "w":[0, 0, 0], "u":[0, 0, 0]}
	for page in pages:
		test_name = "AIMCAT19"+page
		if section in finaldata[test_name]["di"]:
			sectionData = finaldata[test_name]["di"][section]
			summary["di"][section]["q"] = summary["di"][section]["q"] + sectionData["q"]
			summary["di"][section]["r"][0] = summary["di"][section]["r"][0] + sectionData["r"][0]
			summary["di"][section]["r"][1] = summary["di"][section]["r"][1] + sectionData["r"][1]
			summary["di"][section]["r"][2] = summary["di"][section]["r"][2] + sectionData["r"][2]
			summary["di"][section]["w"][0] = summary["di"][section]["w"][0] + sectionData["w"][0]
			summary["di"][section]["w"][1] = summary["di"][section]["w"][1] + sectionData["w"][1]
			summary["di"][section]["w"][2] = summary["di"][section]["w"][2] + sectionData["w"][2]
			summary["di"][section]["u"][0] = summary["di"][section]["u"][0] + sectionData["u"][0]
			summary["di"][section]["u"][1] = summary["di"][section]["u"][1] + sectionData["u"][1]
			summary["di"][section]["u"][2] = summary["di"][section]["u"][2] + sectionData["u"][2]

for section in qa_sections:
	summary["qa"][section] = {"q":0, "r":[0, 0, 0], "w":[0, 0, 0], "u":[0, 0, 0]}
	for page in pages:
		test_name = "AIMCAT19"+page
		if section in finaldata[test_name]["qa"]:
			sectionData = finaldata[test_name]["qa"][section]
			summary["qa"][section]["q"] = summary["qa"][section]["q"] + sectionData["q"]
			summary["qa"][section]["r"][0] = summary["qa"][section]["r"][0] + sectionData["r"][0]
			summary["qa"][section]["r"][1] = summary["qa"][section]["r"][1] + sectionData["r"][1]
			summary["qa"][section]["r"][2] = summary["qa"][section]["r"][2] + sectionData["r"][2]
			summary["qa"][section]["w"][0] = summary["qa"][section]["w"][0] + sectionData["w"][0]
			summary["qa"][section]["w"][1] = summary["qa"][section]["w"][1] + sectionData["w"][1]
			summary["qa"][section]["w"][2] = summary["qa"][section]["w"][2] + sectionData["w"][2]
			summary["qa"][section]["u"][0] = summary["qa"][section]["u"][0] + sectionData["u"][0]
			summary["qa"][section]["u"][1] = summary["qa"][section]["u"][1] + sectionData["u"][1]
			summary["qa"][section]["u"][2] = summary["qa"][section]["u"][2] + sectionData["u"][2]


# print(summary)

# Output as data.json
# with open('data.json', 'w') as outfile:
#     json.dump(summary, outfile)

# Output each section as csv for pasting in analysis sheet
with open('analysis.csv', mode='w', newline='') as analysis_file:
	analysis_writer = csv.writer(analysis_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	section = "qa"
	for topic in summary[section]:
		temp = summary[section][topic]
		analysis_writer.writerow([topic, temp["r"][0], temp["r"][1], temp["r"][2], temp["w"][0], temp["w"][1], temp["w"][2], temp["u"][0], temp["u"][1], temp["u"][2]])