# Datapumps *isolated*

Isolated library for datapumps creation and testing.

## Installation ##

```bash
pip install --upgrade git+git://github.com/radeksvarz/datapumps_isolated.git#egg=dataviso_sequencer
```

## Create new sequence ###

See `example/vendor_sequences/acme.py` for API usage.


## Package tests ##

Install requirements:

```bash
pip install -r requirements.txt --upgrade
```

and simply use `tox`:

```bash
tox
```