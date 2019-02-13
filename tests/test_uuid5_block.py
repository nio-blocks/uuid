import uuid
from unittest.mock import Mock, patch
from nio import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..uuid5_block import UUID5


class TestUUID5(NIOBlockTestCase):

    @patch('uuid.uuid5')
    def test_new_uuid5(self, mock_uuid5):
        """A new UUID5 is added to every signal processed."""
        mock_uuid_obj = Mock()
        mock_uuid_obj.__str__ = Mock(return_value='foobarbaz')
        mock_uuid5.return_value = mock_uuid_obj
        blk = UUID5()
        config = {
            'domain': '{{ $domain_name }}',
            'output': '{{ $output }}'
        }
        self.configure_block(blk, config)
        blk.start()
        blk.process_signals([
            Signal({'domain_name': 'niolabs.com', 'output': 'foo'}),
        ])
        blk.stop()
        self.assert_num_signals_notified(1)
        self.assert_last_signal_notified(Signal({
            'foo': 'foobarbaz',
        }))
        mock_uuid5.assert_called_once_with(uuid.NAMESPACE_DNS, 'niolabs.com')

    @patch('uuid.uuid5')
    def test_signal_enrichment(self, mock_uuid5):
        """Signal Enrichment is implemented."""
        mock_uuid_obj = Mock()
        mock_uuid_obj.__str__ = Mock(return_value='foobarbaz')
        mock_uuid5.return_value = mock_uuid_obj
        config = {
            'enrich': {'exclude_existing': False},
            'domain': 'niolabs.com',
        }
        blk = UUID5()
        self.configure_block(blk, config)
        blk.start()
        blk.process_signals([Signal({'pi': 3.14})])
        blk.stop()
        self.assert_last_signal_notified(Signal({
            'pi': 3.14,
            'uuid': 'foobarbaz',
        }))

    @patch('uuid.uuid5')
    def test_binary_output(self, mock_uuid5):
        """Optinal binary output instead of canonical hex string."""
        mock_uuid_obj = Mock()
        mock_uuid_obj.bytes = b'foo'
        mock_uuid_obj.__str__ = Mock(side_effect=str)  # must return string
        mock_uuid5.return_value = mock_uuid_obj
        blk = UUID5()
        config = {
            'binary': True,
            'domain': 'niolabs.com',
        }
        self.configure_block(blk, config)
        blk.start()
        blk.process_signals([Signal()])
        blk.stop()
        self.assert_last_signal_notified(Signal({
            'uuid': b'foo',
        }))
        mock_uuid5.assert_called_once_with(uuid.NAMESPACE_DNS, 'niolabs.com')
        mock_uuid_obj.__str__.assert_not_called()
