import numpy as np

import uhd

from loguru import logger

class Transceiver():
    def __init__(self, args):
        self.tx_sample_rate = args.tx_sample_rate
        self.tx_center_freq = args.tx_center_freq
        self.tx_channel_freq = args.tx_channel_freq
        # self.tx_antenna = args.tx_antenna
        self.tx_gain = args.tx_gain
        
        self.rx_sample_rate = args.rx_sample_rate
        self.rx_center_freq = args.rx_center_freq
        self.rx_channel_freq = args.rx_channel_freq
        # self.rx_antenna = args.rx_antenna
        self.rx_gain = args.rx_gain
        
        
        self.usrp = uhd.usrp.MultiUSRP()
        self.stream_args = uhd.usrp.StreamArgs("fc32", "sc16")
        self.usrp.set_tx_rate(self.tx_sample_rate)
        self.usrp.set_tx_freq(self.tx_center_freq)
        self.usrp.set_tx_gain(self.tx_gain)
        # TODO: Add antenna selection with self.tx_antenna
        self.tx_streamer = self.usrp.get_tx_stream(self.stream_args)
        self.tx_metadata = uhd.types.TXMetadata()
        
        
        self.usrp.set_rx_rate(self.rx_sample_rate, 0)
        self.usrp.set_rx_freq(uhd.libpyuhd.types.tune_request(self.rx_center_freq), 0)
        self.usrp.set_rx_gain(self.rx_gain, 0)

        # Set up the stream and receive buffer
        st_args = uhd.usrp.StreamArgs("fc32", "sc16")
        st_args.channels = [0]
        self.rx_metadata = uhd.types.RXMetadata()
        self.rx_streamer = self.usrp.get_rx_stream(st_args)
        # recv_buffer = np.zeros((1, self.read_buffer_size), dtype=np.complex64)

        # Start Stream
        stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
        # stream_cmd.stream_now = True
        INIT_DELAY = 0.05
        stream_cmd.time_spec = uhd.types.TimeSpec(self.usrp.get_time_now().get_real_secs() + INIT_DELAY)
        # self.tx_metadata.has_time_spec = bool(self.tx_streamer.get_num_channels())
        self.rx_streamer.issue_stream_cmd(stream_cmd)
        
        buffer_size = 2000
        self.read_buffer = np.zeros(buffer_size, np.complex64)
    def read(self):
        # stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
        # stream_cmd.stream_now = True
        # self.rx_streamer.issue_stream_cmd(stream_cmd)
        
        # TODO: Possibly implement this for efficiency if larger buffer needed.
        # for i in range(num_samps//1000):
        #     self.rx_streamer.recv(recv_buffer, metadata)
        #     samples[i*1000:(i+1)*1000] = recv_buffer[0]
        
        self.rx_streamer.recv(self.read_buffer, self.rx_metadata)
        if not self.rx_metadata.error_code == uhd.types.RXMetadataErrorCode.none:
            logger.warning(self.rx_metadata.error_code)
        # self.read_buffer = np.copy(self.usrp.recv_num_samps(2000, self.frequency, self.sample_rate, [0], 0))
        # stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont)
        # self.rx_streamer.issue_stream_cmd(stream_cmd)
        return self.read_buffer
        
    def send(self, data):
        samps_sent = self.tx_streamer.send(data, self.tx_metadata)
        