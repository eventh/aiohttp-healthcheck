Healthcheck
-----------

Based on https://github.com/Runscope/healthcheck.

aiohttp_healthcheck provides a set of simple aiohttp request handlers that make
it easy to write simple heathcheck functions that can be use to monitor your
application. It's useful for asserting that your dependencies are up and running
and your application can respond to HTTP requests. The Healthcheck functions are
exposed via a user defined aiohttp route so you can use an external monitoring
application (monit, nagios, Runscope, etc.) to check the status and uptime of
your application.

New in version 1.1: aiohttp_healthcheck also gives you a simple aiohttp route to
view information about your application's environment. By default, this includes
data about the operating system, the Python environment, and the current
process. You can customize which sections are included, or add your own sections
to the output.

## Installing

```
pip install aiohttp-healthcheck

```

## Usage

Here's an example of basic usage:

```python
from aiohttp import web
from aiohttp_healthcheck import HealthCheck, EnvironmentDump

app = web.Application()

# Bind the healthcheck to the app's router
health = HealthCheck()
envdump = EnvironmentDump()
app.router.add_get("/healthcheck", health)
app.router.add_get("/environment", envdump)

# add your own check function to the healthcheck
def redis_available():
    client = _redis_client()
    info = client.info()
    return True, "redis ok"

health.add_check(redis_available)

# add your own data to the environment dump
def application_data():
	return {"maintainer": "Brannon Jones",
	        "git_repo": "https://github.com/brannon/aiohttp-healthcheck"}

envdump.add_section("application", application_data)
```

To run all of your check functions, make a request to the healthcheck URL
you specified, like this:

```
curl "http://localhost:5000/healthcheck"
```

And to view the environment data, make a check to the URL you specified for
EnvironmentDump:

```
curl "http://localhost:5000/environment"
```

## The HealthCheck class

### Check Functions

Check functions take no arguments and should return a tuple of (bool, str).
The boolean is whether or not the check passed. The message is any string or
output that should be rendered for this check. Useful for error
messages/debugging.

```python
# add check functions
def addition_works():

	if 1 + 1 == 2:
		return True, "addition works"
	else:
		return False, "the universe is broken"
```

Any exceptions that get thrown by your code will be caught and handled as
errors in the healthcheck:

```python
# add check functions
def throws_exception():
	bad_var = None
	bad_var['explode']

```

Will output:

```json
{
	"status": "failure",
		"results": [
		{
			"output": "'NoneType' object has no attribute '__getitem__'",
			"checker": "throws_exception",
			"passed": false
		}
	]
}
```

Note, all checkers will get run and all failures will be reported. It's
intended that they are all separate checks and if any one fails the
healthcheck overall is failed.

### Caching

In a typical infrastructure, the /healthcheck endpoint can be hit surprisingly
often. If haproxy runs on every server, and each haproxy hits every healthcheck
twice a minute, with 30 servers that would be 60 healthchecks per minute to
every aiohttp service.

To avoid putting too much strain on backend services, health check results can
be cached in process memory. By default, health checks that succeed are cached
for 27 seconds, and failures are cached for 9 seconds. These can be overridden
with the `success_ttl` and `failed_ttl` parameters. If you don't want to use
the cache at all, initialize the Healthcheck object with `success_ttl=None,
failed_ttl=None`.

### Customizing

You can customize the status codes, headers, and output format for success and
failure responses.

## The EnvironmentDump class

### Built-in data sections

By default, EnvironmentDump data includes these 3 sections:

* `os`: information about your operating system.
* `python`: information about your Python executable, Python path, and
installed packages.
* `process`: information about the currently running Python process, including
the PID, command line arguments, and all environment variables.

Some of the data is scrubbed to avoid accidentally exposing passwords or access
keys/tokens. Config keys and environment variable names are scanned for `key`,
`token`, or `pass`. If those strings are present in the name of the variable,
the value is not included.

### Disabling built-in data sections

For security reasons, you may want to disable an entire section. You can
disable sections when you instantiate the `EnvironmentDump` object, like this:

```python
envdump = EnvironmentDump(include_python=False,
                          include_os=False,
                          include_process=False)
```

### Adding custom data sections

You can add a new section to the output by registering a function of your own.
Here's an example of how this would be used:

```python
def application_data():
	return {"maintainer": "Brannon Jones",
	        "git_repo": "https://github.com/brannon/aiohttp-healthcheck"}

envdump = EnvironmentDump()
app.router.add_get("/environment", envdump)
envdump.add_section("application", application_data)
```
