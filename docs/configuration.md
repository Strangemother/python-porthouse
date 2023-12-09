# Configuring your Porthouse

Porthouse accepts configuration through the command line, or a `.porthouse` config file.

```bash
$> porthouse [config] run --param --param
```

### `.porthouse` File

You can execute porthouse on a local `.porthouse` file, and override with command-line arguments.
The contents of the config file is generic TOML:

_.porthouse_ file:
```ini
HOST=0.0.0.0
PORT=8001
```

Run a local `.porthouse` file and override the port:

```bash
$> porthouse . run --port 9010
# port = 9010
```

The period `.` is a local-directory to scan.  You can provide a file or directory. If no config is given the defaults are used.

To run the `root/configs/.porthouse` file:

```
+ root/
    + configs/
        - .porthouse
```

Provide the config file _before_ the `run` sub-command:

```bash
$> porthouse root/configs/.porthouse run
```

Alternatively given a directory, we can search and discover a `--config-file`:

```bash
$> porthouse root/configs/ run
# config = root/configs/.porthouse
```

You can choose any config filename with `--config-file`:

```bash
$> porthouse root/configs/ --config-file=my-config.txt run
# config = root/configs/my-config.txt
```


## Arguments

Options may be given as arguments. Command-line arguments override any file configurations:

_.porthouse_ file:
```ini
PORT=9001
```

Running without a config file:

```bash
$> porthouse run
# port = 0
```

Running with a config file:

```bash
$> porthouse root/configs/.porthouse run
# port = 9001
```

With the a config file and command-line argument:

```bash
$> porthouse root/configs/.porthouse run --port 8000
# port = 8000
```

