@rem
@rem   Create Bulk ICS
@rem    Applications
@rem         &
@rem       Rules
@rem
@rem   Parses a XLSX file to convert to CSV
@rem
%cd%\XlsToCsv.vbs %cd%\ics-db.xlsx %cd%\ics-db.csv
@rem
@rem   Parses a CSV file ics-app-properties.csv that has 19 columns 
@rem %1 = ICS APP Name
@rem %2 = Color
@rem %3 = Comments
@rem %4 = Function
@rem %5 = function:address_range_max
@rem %6 = function:address_range_min
@rem %7 = function:address_type
@rem %8 = function:function_range_max
@rem %9 = function:function_range_min
@rem %10 = function:function_type
@rem %11 = function:standard_function
@rem %12 = group
@rem %13 = unit
@rem %14 = unit:unit_id_range_max
@rem %15 = unit:unit_id_range_min
@rem %16 = unit:unit_type
@rem %17 = value
@rem %18 = value:value_range_max
@rem %19 = value:value_range_min
@rem %20 = rule index
@rem
del del dbedit-input.txt
@rem
FOR /F "skip=1 tokens=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20 delims=," %%a in (ics-db.csv) do (
	@rem Create the ICS Application
	@echo create modbus_application %%a>> dbedit-input.txt
	@rem Modify the ICS Application properties
	@echo modify appfw_objects %%a color %%b>> dbedit-input.txt
	@echo modify appfw_objects %%a comments %%c>> dbedit-input.txt
	@echo modify appfw_objects %%a function %%d>> dbedit-input.txt
	@echo modify appfw_objects %%a function:address_range_max %%e>> dbedit-input.txt
	@echo modify appfw_objects %%a function:address_range_min %%f>> dbedit-input.txt
	@echo modify appfw_objects %%a function:address_type %%g>> dbedit-input.txt
	@echo modify appfw_objects %%a function:function_range_max %%h>> dbedit-input.txt
	@echo modify appfw_objects %%a function:function_range_min %%i>> dbedit-input.txt
	@echo modify appfw_objects %%a function:function_type %%j>> dbedit-input.txt
	@echo modify appfw_objects %%a function:standard_function %%k>> dbedit-input.txt
	@echo modify appfw_objects %%a group %%l>> dbedit-input.txt
	@echo modify appfw_objects %%a unit %%m>> dbedit-input.txt
	@echo modify appfw_objects %%a unit:unit_id_range_max %%n>> dbedit-input.txt
	@echo modify appfw_objects %%a unit:unit_id_range_min %%o>> dbedit-input.txt
	@echo modify appfw_objects %%a unit:unit_type %%p>> dbedit-input.txt
	@echo modify appfw_objects %%a value %%q>> dbedit-input.txt
	@echo modify appfw_objects %%a value:value_range_max %%r>> dbedit-input.txt
	@echo modify appfw_objects %%a value:value_range_min %%s>> dbedit-input.txt
	@echo update appfw_objects %%a>> dbedit-input.txt
	@rem Create the rule
	@echo addelement appfw_misc ##Standard rulebase:rule appfw_rule>> dbedit-input.txt
	@rem Modify the rule
	@echo modify appfw_misc ##Standard rulebase:rule:%%t:rule_name %%a>> dbedit-input.txt
	@echo modify appfw_misc ##Standard rulebase:rule:%%t:src appfw_source>> dbedit-input.txt
	@echo modify appfw_misc ##Standard rulebase:rule:%%t:dst appfw_destination>> dbedit-input.txt
	@echo modify appfw_misc ##Standard rulebase:rule:%%t:services appfw_service>> dbedit-input.txt
	@echo modify appfw_misc ##Standard rulebase:rule:%%t:application appfw_applications>> dbedit-input.txt
	@echo modify appfw_misc ##Standard rulebase:rule:%%t:track rulebase_tracks:Complete_Log>> dbedit-input.txt
	@echo modify appfw_misc ##Standard rulebase:rule:%%t:user_notification user_notification>> dbedit-input.txt
	@echo modify appfw_misc ##Standard rulebase:rule:%%t:comment "POC_comments">> dbedit-input.txt
	@echo modify appfw_misc ##Standard rulebase:rule:%%t:action rulebase_actions:Allow>> dbedit-input.txt
	@rem Enable the Rule
	@echo modify appfw_misc ##Standard rulebase:rule:%%t:disabled false>> dbedit-input.txt
	@rem Update Policy
	@echo update appfw_misc ##Standard>> dbedit-input.txt
	@rem Add ICS App to Rule
	@echo addelement appfw_misc ##Standard rulebase:rule:%%t:application:ReferenceObject appfw_objects:%%a>> dbedit-input.txt
)
@rem
@echo update_all>> dbedit-input.txt
@rem
del %cd%\ics-db.csv
@rem
cls
@echo.
@echo Copy the file dbedit-input.txt to the Management Server and execute this command:
@echo.
@echo # dbedit -local -f dbedit-input.txt -r ics-app-import
@echo.
@echo.
@echo END
@echo.
@rem   
Pause
