#!/usr/bin/env python3
# Copyright (c) 2017-2021 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Assignment
    getting node 1 to mine another block, sending it to node 2, 
    and checking that node 2 receives it.

    I've tried to make changes in run_test
"""
# Imports should be in PEP8 ordering (std library first, then third party
# libraries then local imports).
from collections import defaultdict

# Avoid wildcard * imports
from test_framework.blocktools import (create_block, create_coinbase)
from test_framework.messages import CInv, MSG_BLOCK
from test_framework.p2p import (
    P2PInterface,
    msg_block,
    msg_getdata,
    p2p_lock,
)
from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import (
    assert_equal,
)

# P2PInterface is a class containing callbacks to be executed when a P2P
# message is received from the node-under-test. Subclass P2PInterface and
# override the on_*() methods if you need custom behaviour.
class BaseNode(P2PInterface):
    def __init__(self):
        """Initialize the P2PInterface

        Used to initialize custom properties for the Node that aren't
        included by default in the base class. Be aware that the P2PInterface
        base class already stores a counter for each P2P message type and the
        last received message of each type, which should be sufficient for the
        needs of most tests.

        Call super().__init__() first for standard initialization and then
        initialize custom properties."""
        super().__init__()
        # Stores a dictionary of all blocks received
        self.block_receive_map = defaultdict(int)


class ExampleTest(BitcoinTestFramework):
    # Each functional test is a subclass of the BitcoinTestFramework class.

    # Override the set_test_params(), skip_test_if_missing_module(), add_options(), setup_chain(), setup_network()
    # and setup_nodes() methods to customize the test setup as required.
    def set_test_params(self):
        """Override test parameters for your individual test.
        This method must be overridden and num_nodes must be explicitly set."""
        # By default every test loads a pre-mined chain of 200 blocks from cache.
        # Set setup_clean_chain to True to skip this and start from the Genesis
        # block.
        self.setup_clean_chain = True
        self.num_nodes = 3
        # Use self.extra_args to change command-line arguments for the nodes
        self.extra_args = [[], ["-logips"], []]

    def run_test(self):
        """Main test logic"""
        
        # Create P2P connections will wait for a verack to make sure the connection is fully up
        peer_messaging = self.nodes[0].add_p2p_connection(BaseNode())

        # Generating a block on one of the nodes will get us out of IBD
        # blocks = [int(self.generate(self.nodes[0], sync_fun=lambda: self.sync_all(self.nodes[0:2]), nblocks=1)[0], 16)]
        # Logs are nice. Do plenty of them. They can be used in place of comments for
        # breaking the test into sub-sections.
        self.log.info("Starting test!")

        self.generate(self.nodes[1],nblocks=1)
        self.sync_blocks()
        with p2p_lock:
            assert_equal(self.nodes[1].getbestblockhash(), self.nodes[2].getbestblockhash())

if __name__ == '__main__':
    ExampleTest().main()
