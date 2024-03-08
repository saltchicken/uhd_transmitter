import argparse
from loguru import logger

from transceiver import Transceiver

from IPython import embed

import sys

def main():
    parser = argparse.ArgumentParser(description="A simple script to demonstrate argument parsing.")
    parser.add_argument('--tx_sample_rate', type=float, required=True, help="Sample rate for TX (Hz). Example: 2e6")
    parser.add_argument('--tx_center_freq', type=float, required=True, help="Center frequency for TX (Hz). Example: 434e6")
    parser.add_argument('--tx_channel_freq', type=float, required=True, help="Channel frequency for transmitter. Offset from center (Hz). Example: 25000")
    # parser.add_argument('--tx_antenna', type=str, required=True, help="")
    parser.add_argument('--tx_gain', type=int, required=True, help="Gain for TX. Example: 10")
    
    
    parser.add_argument('--rx_sample_rate', type=float, required=True, help="Sample rate for RX (Hz). Example: 2e6")
    parser.add_argument('--rx_center_freq', type=float, required=True, help="Center frequency for receiver (Hz). Example: 434e6")
    parser.add_argument('--rx_channel_freq', type=float, required=True, help="Channel frequency for receiver. Offset from center (Hz). Example: 40000")
    # parser.add_argument('--rx_antenna', type=str, required=True, help="")
    parser.add_argument('--rx_gain', type=int, required=True, help="Gain for RX. Example: 20")
    parser.add_argument('--verbose', '-v', action='store_true', help="Enable verbose mode")
    args = parser.parse_args()

    logger.remove()
    if args.verbose:
        logger.add(sys.stderr, level="DEBUG")
    else:
        logger.add(sys.stderr, level="INFO")
    

    transceiver = Transceiver(args)
    embed(quiet=True)


if __name__ == "__main__":
    main()