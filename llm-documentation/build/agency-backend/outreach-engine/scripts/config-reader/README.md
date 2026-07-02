# config-reader

Reads tenant JSON config from `users/<tenant>/config.json`.

## Usage

```bash
python config_reader.py --tenant marin        # live
python config_reader.py --tenant marin --demo  # demo config
```

Returns `None` if config file not found.
