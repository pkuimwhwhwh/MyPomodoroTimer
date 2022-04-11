from wsgiref import headers
import pandas

def getTasks() -> list:
	dfTasks:pandas.DataFrame=pandas.read_csv("tasks.csv")
	return dfTasks["task_name"].values.tolist()

def addTimeRecord():
	pass