# Copyright (c) 2012 Brocade Communications Systems, Inc.
# All Rights Reserved.
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

"""
Brocade NOS Driver implements NETCONF over SSHv2 for
Quantum network life-cycle management
"""

import logging

from ncclient import manager

from quantum.plugins.brocade.nos import nctemplates as template

LOG = logging.getLogger(__name__)

SSH_PORT = 22


def nos_unknown_host_cb(host, fingerprint):
    """
    An unknown host callback returns `True` if it finds the key acceptable,
    and `False` if not. This default callback for NOS always returns 'True'
    (i.e. trusts all hosts for now)
    """
    return True


class NOSdriver():
    """
    NOS NETCONF interface driver for Quantum network
    life-cycle management (leverages AMPP on NOS)
    """

    def __init__(self):
        pass

    def connect(self, host, username, password):
        """
        Connect via SSH and initialize the NETCONF session.
        """
        mgr = manager.connect(host=host, port=SSH_PORT,
                              username=username, password=password,
                              unknown_host_cb=nos_unknown_host_cb)
        return mgr

    def create_network(self, host, username, password, id):
        """
        Creates a new virtual network
        """
        name = template.OS_PORT_PROFILE_NAME.format(id=id)
        with self.connect(host, username, password) as mgr:
            self.create_vlan_interface(mgr, id)
            self.create_port_profile(mgr, name)
            self.create_vlan_profile_for_port_profile(mgr, name)
            self.configure_l2_mode_for_vlan_profile(mgr, name)
            self.configure_trunk_mode_for_vlan_profile(mgr, name)
            self.configure_allowed_vlans_for_vlan_profile(mgr, name, id)
            self.activate_port_profile(mgr, name)

    def delete_network(self, host, username, password, id):
        """
        Deletes a virtual network
        """
        name = template.OS_PORT_PROFILE_NAME.format(id=id)
        with self.connect(host, username, password) as mgr:
            self.deactivate_port_profile(mgr, name)
            self.delete_port_profile(mgr, name)
            self.delete_vlan_interface(mgr, id)

    def associate_mac_to_network(self, host, username, password, id, mac):
        """
        Associates a MAC address to virtual network
        """
        name = template.OS_PORT_PROFILE_NAME.format(id=id)
        with self.connect(host, username, password) as mgr:
            self.associate_mac_to_port_profile(mgr, name, mac)

    def dissociate_mac_from_network(self, host, username, password, id, mac):
        """
        Dissociates a MAC address from virtual network
        """
        name = template.OS_PORT_PROFILE_NAME.format(id=id)
        with self.connect(host, username, password) as mgr:
            self.dissociate_mac_from_port_profile(mgr, name, mac)

    def create_vlan_interface(self, mgr, vlan_id):
        """
        Configures a VLAN interface
        """
        confstr = template.CREATE_VLAN_INTERFACE.format(vlan_id=vlan_id)
        mgr.edit_config(target='running', config=confstr)

    def delete_vlan_interface(self, mgr, vlan_id):
        """
        Deletes a VLAN interface
        """
        confstr = template.DELETE_VLAN_INTERFACE.format(vlan_id=vlan_id)
        mgr.edit_config(target='running', config=confstr)

    def get_port_profiles(self, mgr):
        """
        Retrieves all port profiles
        """
        filterstr = template.PORT_PROFILE_XPATH_FILTER
        response = mgr.get_config(source='running',
                                  filter=('xpath', filterstr)).data_xml
        return response

    def get_port_profile(self, mgr, name):
        """
        Retrieves a port profile
        """
        filterstr = template.PORT_PROFILE_NAME_XPATH_FILTER.format(name=name)
        response = mgr.get_config(source='running',
                                  filter=('xpath', filterstr)).data_xml
        return response

    def create_port_profile(self, mgr, name):
        """
        Creates a port profile
        """
        confstr = template.CREATE_PORT_PROFILE.format(name=name)
        mgr.edit_config(target='running', config=confstr)

    def delete_port_profile(self, mgr, name):
        """
        Deletes a port profile
        """
        confstr = template.DELETE_PORT_PROFILE.format(name=name)
        mgr.edit_config(target='running', config=confstr)

    def activate_port_profile(self, mgr, name):
        """
        Activates a port profile
        """
        confstr = template.ACTIVATE_PORT_PROFILE.format(name=name)
        mgr.edit_config(target='running', config=confstr)

    def deactivate_port_profile(self, mgr, name):
        """
        Deactivates a port profile
        """
        confstr = template.DEACTIVATE_PORT_PROFILE.format(name=name)
        mgr.edit_config(target='running', config=confstr)

    def associate_mac_to_port_profile(self, mgr, name, mac_address):
        """
        Associates a MAC address to a port profile
        """
        confstr = template.ASSOCIATE_MAC_TO_PORT_PROFILE.format(
            name=name, mac_address=mac_address)
        mgr.edit_config(target='running', config=confstr)

    def dissociate_mac_from_port_profile(self, mgr, name, mac_address):
        """
        Dissociates a MAC address from a port profile
        """
        confstr = template.DISSOCIATE_MAC_FROM_PORT_PROFILE.format(
            name=name, mac_address=mac_address)
        mgr.edit_config(target='running', config=confstr)

    def create_vlan_profile_for_port_profile(self, mgr, name):
        """
        Creates VLAN sub-profile for port profile
        """
        confstr = template.CREATE_VLAN_PROFILE_FOR_PORT_PROFILE.format(
            name=name)
        mgr.edit_config(target='running', config=confstr)

    def configure_l2_mode_for_vlan_profile(self, mgr, name):
        """
        Configures L2 mode for VLAN sub-profile
        """
        confstr = template.CONFIGURE_L2_MODE_FOR_VLAN_PROFILE.format(
            name=name)
        mgr.edit_config(target='running', config=confstr)

    def configure_trunk_mode_for_vlan_profile(self, mgr, name):
        """
        Configures trunk mode for VLAN sub-profile
        """
        confstr = template.CONFIGURE_TRUNK_MODE_FOR_VLAN_PROFILE.format(
            name=name)
        mgr.edit_config(target='running', config=confstr)

    def configure_allowed_vlans_for_vlan_profile(self, mgr, name, vlan_id):
        """
        Configures allowed VLANs for VLAN sub-profile
        """
        confstr = template.CONFIGURE_ALLOWED_VLANS_FOR_VLAN_PROFILE.format(
            name=name, vlan_id=vlan_id)
        mgr.edit_config(target='running', config=confstr)