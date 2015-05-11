# Datapumps *isolated*

Isolated library for datapumps creation and testing.

[![Requirements Status](https://requires.io/github/radeksvarz/datapumps_isolated/requirements.svg?branch=master)](https://requires.io/github/radeksvarz/datapumps_isolated/requirements/?branch=master)
&nbsp;
[![Coverage Status](https://coveralls.io/repos/radeksvarz/datapumps_isolated/badge.svg)](https://coveralls.io/r/radeksvarz/datapumps_isolated)
&nbsp;
[![Build Status](https://travis-ci.org/radeksvarz/datapumps_isolated.svg?branch=master)](https://travis-ci.org/radeksvarz/datapumps_isolated)

## Installation ##

**This package is NOT published on PyPI.**

```bash
pip install --upgrade git+git://github.com/radeksvarz/datapumps_isolated.git#egg=dataviso_sequencer
```

## Create new sequence ###

**For complete example see `example/vendor_sequences/acme.py` for API usage.**

1) Create *Step*:

```python
from dataviso_sequencer.lib.core import Step


class MyFirstStep(Step):
    def run(self, previous_step_data=None, **kwargs):
        # Add some code

    def get_output(self):
        # Return (optionally) some data
```

2) Create *Sequence*:

```python
from dataviso_sequencer.lib.core import Sequence


class MyFirstSequence(Sequence):
    def get_flow(self):
        return [MyFirstStep()]

    def run(self):
        for step in self.get_flow():
			step.run()

    def run_step(self, step_key):
        # TODO
```

3) Register your Sequence (see `example/run.py`):

```python
from vendor_sequences.example import MyFirstSequence

SEQUENCE_REGISTER = (
	MyFirstSequence,
)

```

4) Test (run) your Sequence:

```bash
cd your/working/directory/...
cd example/
python run.py
Starting:  <class 'vendor_sequences.acme.MyFirstSequence'>
```


## Package tests ##

Install requirements:

```bash
pip install -r requirements.txt --upgrade
```

and simply use `tox`:

```bash
tox
```
