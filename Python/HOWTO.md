# How to write a Regression Test in Python
For regression tests, it has been decided that they will be written in Python.
For simplicity we will use Python's standard unit testing framework. Below are
brief explanations of how one should write a regression test.


## What a Basic Regression Test Looks Like
Below is what a minimal regression test should look like:


    #!/usr/bin/env python
    import unittest

    class SomeTest(unittest.TestCase):
        def setUp(self):
            # test setup code goes here

        def tearDown(self):
            # test tear down code goes here

        def test_something(self):
            # test code here
            self.assertEqual(1 + 1, 2)


To use the above file as a test we run the script using [pytest](http://pytest.org/).

Pytest will attempt to find all tests in `SomeTest` and find methods starting
with the word `test_*`, in this case it will find `test_something` and execute
the test code there.

The reason we choose to use pytest is it's ease of use and extended feature set. We can initiate pytest over an entire test directory with the simple command line prompt:
 
```
"py.test".
```

This will find all test scripts in the current directory with format "test_*.py". We can additionally request pytest to produce an xml output of the tests using:

```
py.test --junitxml=LOGPATH.xml
```

**NOTE**: it is important to note the tests are not ran in the order they are
written. The Python test runner sorts the tests alphabetically and runs them
one by one. Therefore DO NOT WRITE A TEST THAT DEPENDS ON ANOTHER TEST.

From that method `test_something` you can see that Python provides
standard assertions one can use to pass/fail a test.


## How do I write a RESTFul test?
Ater you understand how a basic regression test works, the rest is quite
straight forward, in the following we will go through different ways to test a
RESTFul endpoint with code.


    #!/usr/bin/env python
    import unittest
    import rtp.rest as R2RestClient  # <-- THIS LINE IS VERY IMPORTANT!
                                   # imports R2RestClient for testing


    class RCSGetTest(unittest.TestCase):
        def setUp(self):
            self.rest = R2RestClient("localhost/syscfg/1.0")
            # create an instance of rest client for us to
            # test RCS RESTFul end-points

        def test_get(self):
            # get com_ring2_aquarius_xo_altair server configuration
            response = self.rest.get("/com_ring2_aquarius_xo_altair")

            # check response status code is 200
            self.assertEquals(response.status_code(), 200)

            # make sure the JSON return is not 'None'
            # NOTE: None is Python's equivalent of null or NULL
            # in other programming languages
            self.assertIsNotNone(response.json())

            # you can inspect the contents of the response JSON like so:
            self.assertEquals(response.json()["VERSION"], "1.0.0")
            # the above assertion will expect response.json() to be
            # like this: { "VERSION": "1.0.0", ... }

            # if you are not sure if response.json() will contain the key
            # you can do something like this:
            self.assertIsNotNone(response.json().get("VERSION"))

        # For other RESTFul VERBS such as DELETE and PUT it is essentially the
        # same as the above. This is how you would generally approach to
        # writing a regression test.


## Reference
### What are the different asserts I can use?

    self.assertEqual(a, b)          a == b
    self.assertNotEqual(a, b)       a != b
    self.assertTrue(x)              bool(x) is True
    self.assertFalse(x)             bool(x) is False
    self.assertIs(a, b)             a is b
    self.assertIsNot(a, b)          a is not b
    self.assertIsNone(x)            x is None
    self.assertIsNotNone(x)         x is not None
    self.assertIn(a, b)             a in b
    self.assertNotIn(a, b)          a not in b
    self.assertIsInstance(a, b)     isinstance(a, b)
    self.assertNotIsInstance(a, b)  not isinstance(a, b)


### How do I create a RESTFul client?

    self.rest = R2RestClient("localhost:8080/api/v1.0")

    # when you create a rest client you MUST* provide the
    # base url. The base url in this example is:
    # localhost:8080/api/v1.0
    # this is so that subsequent requests such as calls to
    # `localhost:8080/api/v1.0/data` will be as simple as
    self.rest.get("data")
    # instead of
    self.rest.get("localhost:8080/api/v1.0/data")


### How do I perform a GET, PUT, POST, or DELETE request?

    self.rest = R2RestClient("localhost:8080/api/v1.0")
    self.rest.get("api/1.0/route")
    self.rest.put("api/1.0/route")
    self.rest.post("api/1.0/route")
    self.rest.delete("api/1.0/route")


### How to I send JSON data in a request?

    my_data = { "key": "value" }
    self.rest.post("/data", data=my_data)
    # where data is the JSON you wish to send
    # you can also substitute self.rest.post with any other request
    # method such as put or delete or get...


### How to I set the HEADER in a request?

    my_headers = { "Authentication": "some app token" }
    self.rest.post("/data", headers=my_headers)
    # where header is the HEADER fields you wish to send
    # you can also substitute self.rest.post with any other request
    # method such as put or delete or get...


### How do I set both the HEADER and JSON data in a request?

    my_headers = { "Authentication": "some app token" }
    my_data = { "key": "value" }
    self.rest.post("/data", data=my_data, headers=my_headers)


### How do I check the response status code?

    response = self.rest.get("/data")
    print response.status_code


### How do I get the response JSON?

    response = self.rest.get("/data")
    print response.json()


### How do I check the response headers?

    response = self.rest.get("/data")
    print response.headers["Content-Type"]


### How do I get the response body?

    response = self.rest.get("/data")
    print response.text
