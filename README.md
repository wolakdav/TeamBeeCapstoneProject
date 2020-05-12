# TeamBeeCapstoneProject

Repository for Portland State University Winter-Spring Team Bees capstone project.

## Setup

These are Linux instructions. It is recommended to adjust `assets/config.json`
as appropriate (for more, see below).

### Install and Activate Python Dependencies

1) `python3 -m pip install --user pipenv`: Install pipenv locally - Python 3.7 is required.
2) `cd TeamBeeCapstoneProject`
3) `pipenv shell`: Activate the virtual environment.
4) `pipenv install`: Install the dependencies specified by `Pipfile.lock` and `Pipefile.`
5) `exit`: Close the virtual environment.

### First Time Execution

If the output database has not been generated or used, then it is required to
first boot the CLI menu to build the output database's schema, and then
manually execute this program. This is possible via the same CLI menu or via
the command arguments (for more, see below).  

It is recommended to adjust `assets/config.json` for ease of use. For more, see
below.

## General Usage

1) `pipenv shell`: Activate the virtual environment.
2) Executing the program.  
  a. `python3 main.py`: Start the program's CLI menu.  
  b. `python3 main.py --help`: See the instructions for use as a command.  
3) `exit`: Close the virtual environment

### Setup Docker environment

To setup the docker environment you can do so using the script ```docker/build```. This bash script can be executed by the following command ```./build``` while in the docker directory. This script will simply build the image for future docker containers. If you wish to connect to a docker container with the ```stop_spot``` image and interact with it using a shell you can use the ```docker/connect``` script by running it in a similar fashion to the ```docker/build``` script. The ```docker/connect``` script will create a new container everytime, if you wish to connect an existing container you can do so with the following command.

```docker exec -it container_id bash```


### Setup Cron Job

To create a cron job, use the ```cron_job/create_cron_job``` script to create a cron job which will process new data every 24 hours. The script is a simple bash script which puts the contents of ```cron_job/cron_job_params``` into crontab. To run the script simply type ```./create_cron_job``` while in the ```cron_job``` directory. If you want to change the time interval for which the cron job runs you can edit the ```cron_job/cron_job_params``` file and rerun the ```cron_job/create_cron_job``` script. By default the script is set to start a container of the application and process the next days data at 4am.

Again, this does require the First Time Execution to have already occurred as the connection details within ```assets/config.json``` are necessary to process the next days data. Additionally, you must build the docker image using the script ```docker/build``` as the cron job will start a docker container to process the next days data.  

### Using the Client

The main program is handled by `client_instance`, a singleton client. To load
the basic CLI menu, use this line in the shell.

    $ python3 main.py

To access all of the members and methods described below via the Python
interpreter, as well as booting the CLI menu, use this line in the shell.

    $ python3 -i main.py

To see all of the available commands, use this line in the shell.

    $ python3 main.py --help

#### `client_instance.main(read_env_data=True)`

This method is called in main.py and it is the main control unit of the Client.
`read_env_data` determines if the program will read environment data to
determine where the Pipeline database credentials are (for more, see below).

#### `bool client_instance.process_data(start_date=None, end_date=None)`

This method will process C-Tran data between `start_date` and `end_date`,
**inclusive**. These parameters can be datetime or date instances, or strings
in the format of "YYYY/MM/DD". If no dates are supplied, this will prompt the
user for them. If `end_date` is not supplied, then it will be set to
`start_date`.

#### `bool client_instance.process_next_day()`

This method will process the day after the latest processed service day.  

Be aware that this will not work if First Time Execution has not occurred.

#### `bool client_instance.process_since_checkpoint()`

This method will process all unprocessed service dates after the latest
processed service date.  

Be aware that this will not work if First Time Execution has not occurred.

#### `bool client_instance.reprocess(start_date=None, end_date=None)`

Delete the data between the input dates and run
`client_instance.process_data(start_date, end_date)`.  

This method will process C-Tran data between `start_date` and `end_date`,
**inclusive**. These parameters can be datetime or date instances, or strings
in the format of "YYYY/MM/DD". If no dates are supplied, this will prompt the
user for them. If `end_date` is not supplied, then it will be set to
`start_date`.

#### `bool client_instance.create_all_views()`

Create all views for the Hive schema. Currently only create views for each
flags that queries all data rows with that flag.

#### `client_instance.create_hive()`

This method will create the Hive schema, which is the collection of tables
flags, flagged_data, and service_periods.

#### `CTran_Data client_instance.ctran`

This member is used to query the C-Tran database.  

For more, see `docs/db_ops.md`.

#### `Flagged_Data client_instance.flagged`

This member is used to work with the flagged_data table in Hive.  

For more, see `docs/db_ops.md`.

#### `Flags client_instance.flags`

This member is used to work with the flags table in Hive.  

For more, see `docs/db_ops.md`.

#### `Service_Periods client_instance.service_periods`

This member is used to work with the service_periods table in Hive.  

For more, see `docs/db_ops.md`.

#### `Config client_instance.config`

This member is the instance of Config.  

For more, see below in Adjusting and Utilizing Endpoints, and
`docs/config_readme.md`.

## Adjusting and Utilizing Endpoints

### `assets/config.json`

This configuration file controls various data about the Pipeline. Some notable
settings controlled here are as follows.

1) `user_emails`: The list of email(s) to send critical error messages to.
2) `pipeline_email_passwd`: The password to the Pipeline's email, used for
critical email notifications. For obvious reasons, this is not supplied by default.
3) `pipeline_*`: These are credentials for the Hive database.
4) `portal*`: These are credentials for the Portal database.
5) `notif_django_path`: The output of the Django file (see section
`output/notif.txt` for more).

For more, see `docs/config_readme.md`.

### `bin/env_data.sh`

This file is an alternate way to set the Hive database credentials by
configuring environment variables. These environment variables will take
priority over the corresponding data in `assets/config.json`.

To easily apply these variables, use the below from the root of this project.

     $ source bin/env_data.sh

### `output/`

##### `output/log.txt`

This is the general purpose log file.

##### `output/notif.txt`

This is the default output location for critical error messages capable of
being picked up by a Django application.