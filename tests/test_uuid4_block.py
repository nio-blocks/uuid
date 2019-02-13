from unittest.mock import Mock, patch
from nio import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..uuid4_block import UUID4


class TestUUID4(NIOBlockTestCase):

    @patch('uuid.uuid4')
    def test_new_uuid4(self, mock_uuid4):
        """A new UUID4 is added to every signal processed."""
        mock_uuid_obj = Mock()
        mock_uuid_obj.__str__ = Mock(return_value='foobarbaz')
        mock_uuid4.return_value = mock_uuid_obj
        blk = UUID4()
        config = {
            'output': '{{ $output }}'
        }
        self.configure_block(blk, config)
        blk.start()
        blk.process_signals([Signal({'output': 'foo'})])
        blk.stop()
        self.assert_num_signals_notified(1)
        self.assert_last_signal_notified(Signal({
            'foo': 'foobarbaz',
        }))
        mock_uuid4.assert_called_once_with()

    @patch('uuid.uuid4')
    def test_signal_enrichment(self, mock_uuid4):
        """Signal Enrichment is implemented."""
        mock_uuid_obj = Mock()
        mock_uuid_obj.__str__ = Mock(return_value='foobarbaz')
        mock_uuid4.return_value = mock_uuid_obj
        config = {
            'enrich': {'exclude_existing': False},
        }
        blk = UUID4()
        self.configure_block(blk, config)
        blk.start()
        blk.process_signals([Signal({'pi': 3.14})])
        blk.stop()
        self.assert_last_signal_notified(Signal({
            'pi': 3.14,
            'uuid': 'foobarbaz',
        }))

    @patch('uuid.uuid4')
    def test_binary_output(self, mock_uuid4):
        """Optinal binary output instead of canonical hex string."""
        mock_uuid_obj = Mock()
        mock_uuid_obj.bytes = b'foo'
        mock_uuid_obj.__str__ = Mock(side_effect=str)  # must return string
        mock_uuid4.return_value = mock_uuid_obj
        blk = UUID4()
        config = {
            'binary': True,
        }
        self.configure_block(blk, config)
        blk.start()
        blk.process_signals([Signal()])
        blk.stop()
        self.assert_last_signal_notified(Signal({
            'uuid': b'foo',
        }))
        mock_uuid4.assert_called_once_with()
        mock_uuid_obj.__str__.assert_not_called()
