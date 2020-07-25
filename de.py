import sqlite3
import base64
import requests
import smtplib

def connect():
	conn = sqlite3.connect("results.db")
	cur = conn.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS results(course TEXT PRIMARY KEY, occur TEXT)")
	conn.commit()
	conn.close()

def add_results(course, occur):
	connect()
	conn = sqlite3.connect("results.db")
	cur = conn.cursor()
	cur.execute("INSERT INTO results VALUES(?,?)",(bytes(course,'utf-8'),bytes(occur,'utf-8')))
	conn.commit()
	conn.close()

def find_results(course):	
	connect()
	conn = sqlite3.connect("results.db")
	cur = conn.cursor()
	cur.execute("SELECT occur FROM results WHERE course=?",(bytes(course,'utf-8'),))
	rows = cur.fetchall()
	print(rows)
	conn.commit()
	conn.close()
	return rows

def close():
    return 0

def mailbot():
	SUBJECT = "Check Your result!"
	TEXT = "Your result seems to be declared!"
	message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
	mail = smtplib.SMTP('smtp.gmail.com',587)
	mail.ehlo()
	mail.starttls()
	mail.login('ipu.check.result@gmail.com','result@987')
	mail.sendmail('ipu.check.result@gmail.com','soumyaawasthi05@gmail.com',message)
	mail.close()

def update_results(course,occur):
    conn = sqlite3.connect("results.db")
    cur = conn.cursor()
    cur.execute("UPDATE results SET occur = ? WHERE course=?",(bytes(occur,'utf-8'),bytes(course,'utf-8')))
    conn.commit()
    conn.close()

def result_check():
	url = "http://164.100.158.135/ExamResults/ExamResultsPrev280520.htm"
	headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
	response = requests.get(url, headers= headers)
	c = response.content
	c = str(c)
	count = c.count("BCA")
	results = find_results("BCA")
	for result in results:
		if count > int(result[0]):
			mailbot()
			update_results("BCA",str(count))
			print("Mail sent and database updated!")
		else:
			print("Result not declared yet!")


update_results("BCA","12")
result_check()





