## About
This repo contains regression tests for all of the PROJECTS for which regression tests exist. It also contains some python tools which aid in the regression tests.


## Setup instructions for a developer / tester
### How to install on your local machine.

    gh repo clone loopup/ct-disaster-recovery-automation


### How to write regression tests
Writing regression tests is not trivial for more information visit (here)[1]


## Setup instructions for a build engineer
By convention it is assumed the file structure for regression tests will be as
follows:

    projectname-automation/
        Python/
            tests/
				config.py
                test_1.py
                test_2.py
                test_3.py
				
Here **config.py** is a config file which contains some default values such as request headers. The config file also pulls environment variables which are used in the bamboo test plan.
The RCS config file is shown below:

```python
	import os
	
	RCS_URL       = os.environ['RCS_TEST_URL']
	APP_TOKEN     = os.environ['RCS_TEST_APPTOKEN']
	PARTNER_URI   = os.environ['RCS_TEST_PARTNER_URI']
	AUTHORIZATION = os.getenv('RCS_TEST_AUTHORIZATION',         'R2Secure apptoken=%s' % (APP_TOKEN))
	
	HEADERS = {
		"Content-Type": "application/json",
		"Authorization": AUTHORIZATION,
		"Ring2-Partner-Uri": PARTNER_URI,
		"X-Ring2-TXID": "somerandomtxid"
	}
	
	RCS_TEST_URI = "testing"
	RCS_TEST_SERVER = "test_server"
```

## Changelog

| Version | Comment
| ------: | :------
| 1.0.0   | First release
| 1.1.0   | Restructuring of regression suites.


## Layout


<!-- Describe the software and link to any detailed information, pages, etc. -->
**NOTE**

This repository has only the ``master`` branch. It *does not* have a
``development`` branch.  Create a topic branch from the ``master`` and when
you're done and approved, it will be merged into the master branch.


## References
[1]: https://confluence.loopup.com/pages/viewpage.action?pageId=50266280
