# Environment Data

## Overview

This codebase can read environment variables to determine the username,
password, hostname, and database name it should work with. These are mapped to
a corresponding environment variable as seen below. To activate this
functionality, this can either be set in main.py or by creating environment
variable `$PIPELINE_ENV_DATA` with *any* value.

- username: `$PIPELINE_USER`
- password: `$PIPELINE_PASSWD`
- hostname: `$PIPELINE_HOSTNAME`
- db_name:  `$PIPELINE_DB_NAME`

## `bin/env_data.sh`

For ease of use, and if this is **not** a security flaw for the desired
environment, `bin/env_data.sh` can be source-ed to allow for easy
configuration and activation of this data. Be very sure **not** to
accidentally push sensitive data to the repo.
