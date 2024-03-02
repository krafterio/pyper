Pyper Dynamic DBFilter
----------------------

# Installation

To install this module, you only need to load it as a server-wide module. This can be done with the
`server_wide_modules` parameter in config file or with the `--load` command-line option:

```
server_wide_modules = base,web,pyper_dynamic_dbfilter
```

# HTTP Server Configuration

**For Nginx:**
```
proxy_set_header X-Pyper-Db-Filter <filter_regex>;
```

**For Apache2:**
```
RequestHeader set X-Pyper-Db-Filter <filter_regex>
```

And make sure that proxy mode is enabled in Odoo's configuration file:

```
proxy_mode = True
```

> **Note:**
> Please keep in mind that the standard 0doo dbfilter configuration is still applied before looking at the regular
> expression in the HTTP Header.
