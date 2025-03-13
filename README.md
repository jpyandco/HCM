### Prerequisites
Data for HCM Data is stored in a Oracle Databse.
Each technology has to have its own table.  
Tables can have additional fields only "userlabel" is used as unique identifier for error reporting and thus mandatory to have in table.  
All tables need to be entered into the config file.  
Delete the sample_ prefix for sample_configi.ini and fill file with your values.  

TODO: Default config should be able to be set/changed in the gui.   
Prefill values with default config.  

### Installation
Python 3.12 has to be installed on the machine that tries to run the code.  

Move to folder where requirements.txt is located.   
Then execute following command:  
`pip install -r requirements.txt`



### Usage
Move to folder where main.py is located and run following command:  
`python main.py`

HCM files will be created in the specified folder.   
If the folder does not exist, the program will create it.  
A report called Report.json will be generated which displays total entries/lines written and total errors.  

For every incorrect entry there will be an error object with unique identifier "userlabel" as key.  
The error/s will be displayed after the incorrect entry.  
For more information take a look at Sample_Report.json

After all files are written they are zipped.

TODO: Set and edit default header values, which will be displayed at the start of the program.
Run HCM file creation with given header values.
