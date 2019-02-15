from enum import Enum
import uuid
from nio import Block
from nio.block.mixins import EnrichSignals 
from nio.properties import BoolProperty, SelectProperty, StringProperty, \
    VersionProperty


class UUIDnamespace(Enum):

    DNS = 'DNS'
    URL = 'URL'
    OID = 'OID'
    X500 = 'X500'

class UUIDversions(Enum):

    one = 1
    three = 3
    four = 4
    five = 5

class UUID(EnrichSignals, Block):

    name_string = StringProperty(
        title='Name (versions 3 and 5 only)',
        allow_none=True,
        order=1)
    name_space = SelectProperty(
        UUIDnamespace,
        title='Namespace (versions 3 and 5 only)',
        default=UUIDnamespace.DNS,
        order=2)
    uuid_version = SelectProperty(
        UUIDversions,
        title='UUID Version',
        default=UUIDversions.four,
        order=0)
    output = StringProperty(
        title='Output Attribute',
        default='uuid',
        advanced=True)
    binary = BoolProperty(
        title='Binary Output',
        default=False,
        advanced=True)
    version = VersionProperty('0.1.0')

    def process_signal(self, signal, input_id=None):
        new_uuid = self._get_uuid(signal)
        if not self.binary():
            new_uuid = str(new_uuid)
        else:
            new_uuid = new_uuid.bytes
        new_signal = {self.output(signal): new_uuid}
        return self.get_output_signal(new_signal, signal)

    def _get_uuid(self, signal):
        version = self.uuid_version(signal).value
        version_string = 'uuid{}'.format(version)
        if version in [1, 4]:
            return getattr(uuid, version_string)()
        name = self.name_string(signal)
        namespace = self.name_space(signal).value
        namespace_uuid = getattr(uuid, 'NAMESPACE_{}'.format(namespace))
        return getattr(uuid, version_string)(namespace_uuid, name)
