from wsgiref import headers
import pandas
from datetime import datetime, timedelta

def getTasks() -> list:
	dfTasks:pandas.DataFrame=pandas.read_csv("tasks.csv")
	return dfTasks["task_name"].values.tolist()

def initTotalSpan() -> timedelta:
	dfTimeLog:pandas.DataFrame = pandas.read_csv("log.csv", parse_dates=["start_time"])
	today=datetime.now()
	res:timedelta=timedelta(seconds=dfTimeLog.loc[dfTimeLog['start_time'].dt.day==today.day, "used_time"].sum())
	return res

def convertSpanToHhmmss(td:timedelta) -> str:
	res:str=""
	res="%02d:%02d:%02d" % (td.total_seconds() // 3600, td.total_seconds() //60,td.total_seconds()%60)
	return res

def addTimeRecord():
	pass