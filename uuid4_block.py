import uuid
from nio import Block
from nio.block.mixins import EnrichSignals 
from nio.properties import StringProperty, VersionProperty


class UUID4(EnrichSignals, Block):

    output = StringProperty(
        title='Output Attribute',
        default='uuid',
        advanced=True)
    version = VersionProperty('0.1.0')

    def process_signal(self, signal, input_id=None):
        new_signal = {self.output(signal): str(uuid.uuid4())}
        return self.get_output_signal(new_signal, signal)
