# Overview

This interface layer handles the communication with Keystone via the
'keystone-federated-backend' interface protocol.

# Usage

## Provides

The interface layer will set the following state:

  * `{relation_name}.connected`  The relation is established.

For example:


```python
from charms.reactive import when


@when(federated-backend.connected')
@when('configuration.complete')
def configure_federation(federation):
    domain.wsgi_config_fragment('wsgi_fragment_path')
    domain.trigger_restart()
```
