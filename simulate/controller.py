"""
@project: SDN-SR-TE
@author: sam
@file controller.py
@ide: PyCharm
@time: 2019-03-13 15:49:24
@blog: https://jiahaoplus.com
"""
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls


class TestController(app_manager.RyuApp):

    def __init__(self, *args, **kwargs):
        super(TestController, self).__init__(*args, **kwargs)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofp = datapath.ofproto
        ofp_parser = datapath.ofproto_parser

        actions = [ofp_parser.OFPActionOutput(ofp.OFPP_FLOOD)]
        out = ofp_parser.OFPActionOutput(
            datapath=datapath, buffer_id=msg.buffer_id,
            in_port=msg.in_port, actions=actions
        )

        datapath.send_msg(out)


