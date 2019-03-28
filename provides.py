# Copyright 2019 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from charms.reactive import (
    all_flags_set,
    clear_flag,
    Endpoint,
    set_flag,
    when,
    when_not,
)

import uuid


class KeystoneFIDServiceProvides(Endpoint):

    @property
    def hostname(self):
        return self.all_joined_units.received['hostname']

    @property
    def port(self):
        return self.all_joined_units.received['port']

    @property
    def tls_enabled(self):
        return self.all_joined_units.received['tls-enabled']

    @property
    def base_url(self):
        scheme = 'https' if self.tls_enabled else 'http'
        return ('{}://{}:{}'.format(scheme, self.hostname,
                                    self.port))

    @when('endpoint.{endpoint_name}.joined')
    def joined(self):
        set_flag(self.expand_name('{endpoint_name}.connected'))

    @when('endpoint.{endpoint_name}.changed')
    def changed(self):
        flags = (
            self.expand_name(
                'endpoint.{endpoint_name}.changed.hostname'),
            self.expand_name(
                'endpoint.{endpoint_name}.changed.port'),
            self.expand_name(
                'endpoint.{endpoint_name}.changed.tls-enabled'),
        )
        if all_flags_set(*flags):
            for flag in flags:
                clear_flag(flag)
            set_flag(self.expand_name('{endpoint_name}.available'))

    @when_not('endpoint.{endpoint_name}.joined')
    def departed(self):
        flags = (
            self.expand_name('{endpoint_name}.connected'),
            self.expand_name('{endpoint_name}.available'),
        )
        for flag in flags:
            clear_flag(flag)

    def publish(self, protocol_name, remote_id_attribute):
        # get the first relation object as we only have one relation
        # to a primary as a subordinate
        rel = self.relations[0]
        # can have multiple dashboard charms in general, therefore,
        # all relation objects and all units must be handled
        # to_publish/relation_set work on a per-relation basis
        rel.to_publish['protocol-name'] = protocol_name
        rel.to_publish['remote-id-attribute'] = remote_id_attribute

    def request_restart(self, service_type=None):
        """Request a restart of a set of remote services
        :param service_type: string Service types to be restarted eg 'neutron'.
                                    If ommitted a request to restart all
                                    services is sent
        """
        if service_type:
            key = 'restart-nonce-{}'.format(service_type)
        else:
            key = 'restart-nonce'
        # get the first relation object as we only have one relation
        # to a primary as a subordinate
        rel = self.relations[0]
        # can have multiple dashboard charms in general, therefore,
        # all relation objects and all units must be handled
        # to_publish/relation_set work on a per-relation basis
        rel.to_publish[key] = str(uuid.uuid4())
