# Copyright 2017 Canonical Ltd
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

from charms.reactive import Endpoint


class KeystoneFIDServiceProvides(Endpoint):
    def publish(self, restart_nonce, protocol_name,
                remote_id_attribute):
        # get the first relation object as we only have one relation
        # to a primary as a subordinate
        rel = self.relations[0]
        # can have multiple dashboard charms in general, therefore,
        # all relation objects and all units must be handled
        # to_publish/relation_set work on a per-relation basis
        rel.to_publish['restart-nonce'] = restart_nonce
        rel.to_publish['protocol-name'] = protocol_name
        rel.to_publish['remote-id-attribute'] = remote_id_attribute
