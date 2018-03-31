
   Create Bulk ICS
    Applications
   	  &
        Rules


Workflow of the program:

- The user modify ics-db.xlsx with the configuration of his own PLC

- The user execute ics-exec.cmd

- A new file called dbedit-input.txt will be created in the same directory

- The user copy that file to his management

- Close all opened smartDashboards

- The user import the new ICS applications and rules to his management executing:

	# dbedit -local -f dbedit-input.txt