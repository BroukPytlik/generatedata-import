#!/usr/bin/env python2.7
# 
# Generatedata-import
#
# My quick'n dirty solution for importing mysql databases into generatedata.
#
# Report bugs to:
# Jan Tulak - jan at tulak.me
# or on http://github.com/BroukPytlik/generatedata-import
#
# Licensed under MIT license.
#
#
# Requres SQL Alchemy, mysql-python

import argparse
import sqlalchemy
import json
import sys

output_tables={}


def create_sql_insert(table_name,status,account_id,configuration_name,content, rows):
	return """INSERT INTO `%s` (status, account_id, date_created, last_updated, configuration_name, content, num_rows_generated)
	VALUES ('%s', %d, '%s', '%s', '%s', '%s', %d);
	

""" % (
			
		table_name,
		status, account_id, "2014-01-01 00:00:00", "2014-01-01 00:00:00", 
		configuration_name, content, rows
	)

def get_database(server, user, password, db):

	engine = sqlalchemy.create_engine('mysql://'\
			+user+':'\
			+password+'@'\
			+server+'/'+db)

	connection = engine.connect()

	metadata = sqlalchemy.schema.MetaData()
	metadata.reflect(engine)

	for table in metadata.sorted_tables:
		columns = []
		for column in table.columns:
			columns.append(generatedata_json_get_column(column.name, column.type))

		col = generatedata_content(table.name, columns)
		col = str(col).replace("'",'"')#.replace('\\\\','\\')
		#col += generatedata_json_footer()
		output_tables[table.name] = create_sql_insert("configurations",
				"private", 1, table.name, col, 0)

	connection.close()



def main():
	parser = argparse.ArgumentParser(description=\
			"My quick andn dirty solution for importing mysql databases"
			" into generatedata.")
	parser.add_argument('-s', '--server',required=1)
	parser.add_argument('-u', '--user',required=1)
	parser.add_argument('-p', '--password',required=1)
	parser.add_argument('-d', '--db',required=1)
	args = parser.parse_args()


	get_database(args.server, args.user, args.password, args.db)

	for col in output_tables:
		print output_tables[col]

def generatedata_get_type(mysql_type):
	
	return "data-type-NumberRange"

def generatedata_get_type_data(mysql_type):

	return {"rangeMin":"0","rangeMax":"50"}

def generatedata_json_get_column(name, type):
	column = {'title': name, 
		'dataType': generatedata_get_type(type),
		'data':generatedata_get_type_data(type)}
	return column

def generatedata_content(table_name, columns_list):
	return {
		"exportTarget":"inPage",
		"numResults":"100",
		"dataTypes": columns_list,
		"exportTypes":{"export-type-CSV":{"delimiter":"|",
		"eol":"Windows"},
		"export-type-JSON":{"stripWhitespace":"0"},
		"export-type-HTML":{"dataFormat":"table",
		"useCustomExportFormat":"0",
		"customExportSmartyContent":r"{if $isFirstBatch}\n<!DOCTYPE html>\n<html>\n<head>\n\t<meta charset=\"utf-8\">\n\t<style type=\"text\/css\">\n\tbody { margin: 10px; }\n\ttable,th,td,li,dl { font-family: \"lucida grande\",arial; font-size: 8pt; }\n\tdt { font-weight: bold; }\n\ttable { background-color: #efefef; border: 2px solid #dddddd; width: 100%; }\n\tth { background-color: #efefef; }\n\ttd { background-color: #ffffff; }\n\t<\/style>\n<\/head>\n<body>\n\n<table cellspacing=\"0\" cellpadding=\"1\">\n<tr>\n{foreach $colData as $col}\n\t<th>{$col}<\/th>\n{\/foreach}\n<\/tr>\n{\/if}\n{foreach $rowData as $row}\n<tr>\n{foreach $row as $r}\t<td>{$r}<\/td>\n{\/foreach}\n<\/tr>\n{\/foreach}\n\n{if $isLastBatch}\n<\/table>\n\n<\/body>\n<\/html>\n{\/if}"},
		"export-type-ProgrammingLanguage":{"language":"JavaScript"},
		"export-type-SQL":{"tableName":table_name,
		"databaseType":"MySQL",
		"createTable":"0",
		"dropTable":"0",
		"encloseWithBackquotes":"1",
		"statementType":"insert",
		"insertBatchSize":"10",
		"primaryKey":"default"},
		"export-type-XML":{"rootNodeName":"records",
		"recordNodeName":"record",
		"useCustomExportFormat":"0",
		"customFormat":r"{if $isFirstBatch}\n<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n<records>\n{\/if}\n{foreach $rowData as $row}\n\t<record>\n{foreach from=$colData item=col name=c}\n\t\t<{$col}>{$row[$smarty.foreach.c.index]}<\/{$col}>\n{\/foreach}\n\t<\/record>\n{\/foreach}\n{if $isLastBatch}\n<\/records>\n{\/if}"}},
		"selectedExportType":"HTML"
	}

def generatedata_json_header(generate_rows):
	return '{"exportTarget":"inPage","numResults":"'+str(generate_rows)+'","dataTypes":['

def generatedata_json_footer():
	return r'],"exportTypes":{"export-type-CSV":{"delimiter":"|","eol":"Windows"},"export-type-JSON":{"stripWhitespace":"0"},"export-type-HTML":{"dataFormat":"table","useCustomExportFormat":"0","customExportSmartyContent":"{if $isFirstBatch}\n<!DOCTYPE html>\n<html>\n<head>\n\t<meta charset=\"utf-8\">\n\t<style type=\"text\/css\">\n\tbody { margin: 10px; }\n\ttable, th, td, li, dl { font-family: \"lucida grande\", arial; font-size: 8pt; }\n\tdt { font-weight: bold; }\n\ttable { background-color: #efefef; border: 2px solid #dddddd; width: 100%; }\n\tth { background-color: #efefef; }\n\ttd { background-color: #ffffff; }\n\t<\/style>\n<\/head>\n<body>\n\n<table cellspacing=\"0\" cellpadding=\"1\">\n<tr>\n{foreach $colData as $col}\n\t<th>{$col}<\/th>\n{\/foreach}\n<\/tr>\n{\/if}\n{foreach $rowData as $row}\n<tr>\n{foreach $row as $r}\t<td>{$r}<\/td>\n{\/foreach}\n<\/tr>\n{\/foreach}\n\n{if $isLastBatch}\n<\/table>\n\n<\/body>\n<\/html>\n{\/if}"},"export-type-ProgrammingLanguage":{"language":"JavaScript"},"export-type-SQL":{"tableName":"myTable","databaseType":"MySQL","createTable":"1","dropTable":"1","encloseWithBackquotes":"1","statementType":"insert","insertBatchSize":"10","primaryKey":"default"},"export-type-XML":{"rootNodeName":"records","recordNodeName":"record","useCustomExportFormat":"0","customFormat":"{if $isFirstBatch}\n<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n<records>\n{\/if}\n{foreach $rowData as $row}\n\t<record>\n{foreach from=$colData item=col name=c}\n\t\t<{$col}>{$row[$smarty.foreach.c.index]}<\/{$col}>\n{\/foreach}\n\t<\/record>\n{\/foreach}\n{if $isLastBatch}\n<\/records>\n{\/if}"}},"selectedExportType":"HTML"}'


main()
