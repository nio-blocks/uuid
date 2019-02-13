import uuid
from nio import Block
from nio.block.mixins import EnrichSignals 
from nio.properties import BoolProperty, StringProperty, VersionProperty


class UUID5(EnrichSignals, Block):

    domain = StringProperty(title="Domain Name")
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
        new_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, self.domain(signal))
        if not self.binary():
            new_uuid = str(new_uuid)
        else:
            new_uuid = new_uuid.bytes
        new_signal = {self.output(signal): new_uuid}
        return self.get_output_signal(new_signal, signal)
