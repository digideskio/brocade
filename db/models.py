# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2012 Brocade Communications System, Inc.
# All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging
import sqlalchemy as sa

from quantum.db import api as db
from quantum.db import model_base
from quantum.db import models_v2

LOG = logging.getLogger("BrocadeQuantumAgent")


class Brcd_Network(model_base.BASEV2):
    id = sa.Column(sa.String(36), primary_key=True, default="")
    vlan = sa.Column(sa.String(10))


def create_network(id, vlan):

    session = db.get_session()
    try:
        net = Brcd_Network(id=id, vlan=vlan)
        session.add(net)
        session.flush()
    except Exception as ex:
        raise
    return net


def delete_network(id):
    session = db.get_session()
    try:
        net = (session.query(Brcd_Network).filter_by(id=id).one())
        session.delete(net)
        session.flush()
    except sa.orm.exc.NoResultFound:
        LOG.warning("del_net(): NotFound net for "
                    "vlan_id: %s" % id)


def get_network(id):
    session = db.get_session()
    try:
        return (session.query(Brcd_Network).
                filter_by(id=id).
                one())
    except sa.orm.exc.NoResultFound:
        return None


def get_networks():
    session = db.get_session()
    try:
        nets = session.query(Brcd_Network).all()
        return nets
    except sa.orm.exc.NoResultFound:
        return None


class Brcd_Port(model_base.BASEV2):

    port_id = sa.Column(sa.String(36), primary_key=True, default="")
    network_id = sa.Column(sa.String(36))
    admin_state_up = sa.Column(sa.String(36))
    physical_interface = sa.Column(sa.String(36))
    vlan_id = sa.Column(sa.String(36))
    tenant_id = sa.Column(sa.String(36))


def create_port(port_id, network_id, physical_interface,
                vlan_id, tenant_id, admin_state_up):

    session = db.get_session()

    try:
        port = Brcd_Port(port_id=port_id,
                         network_id=network_id,
                         physical_interface=physical_interface,
                         vlan_id=vlan_id,
                         admin_state_up=admin_state_up,
                         tenant_id=tenant_id)
        session.add(port)
        session.flush()
    except Exception as ex:
        raise
    return port


def get_port(port_id):

    LOG.warning("get_port_from_device(port_id = %s) " % port_id)
    session = db.get_session()
    try:
        x = (session.query(Brcd_Port).
             filter_by(port_id=port_id).
             one())
        return (session.query(Brcd_Port).
                filter_by(port_id=port_id).
                one())
    except sa.orm.exc.NoResultFound:
        return None

    return None