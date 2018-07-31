#!/usr/bin/env python -tt
# -*- coding: utf-8 -*-

################################################################################
# This is the confidential unpublished intellectual property of Dell EMC Corporation,
# and includes without limitation exclusive copyright and trade secret rights
# of Dell EMC throughout the world.
################################################################################

"""This module manages the utms update"""
import requests
import os, time, datetime
from xml.etree import ElementTree
from xml.dom import minidom
import logging
import argparse
from textparser import *

class UTMSParserExection(Exception):
    """This class manages the execption of UTMS parser

    Attributes:
       None
    """
    pass

class UtmsReporter(object):
    """This class is used to create the test plan and test set for the case

    Attributes:
        basic_information (dict): Membership information regarding the location of the test plan
                                  and the team name.
              key:  the prefix of the case name
              value:
                  team : the team name of the case instead of the
        Example:
            {
                raid: { team : "storage management", test_plan_location: "Data Path/Storage Management"
            }
    """

    def __init__(self, http_server = "utmswebserver01.corp.emc.com:8082/UTMSWebService2", project = "Cyclone", domain = "USD"):
        """Initialize the object.

                Args:
                    http_server (str): the address of the UTMS web server
                    project(str): the project name, the default is Cyclone
                    domain(str): the domain name of the project
        """
        self.http_server = http_server
        self.project = project
        self.domain = domain
        self.basic_information = {
            "raid" : {
                "team" : "DP - Storage Management",
                "test_plan_location" : "Subject/Data Path/Storage Management"
            },
            "namespace": {
                "team": "DP - Namespace",
                "test_plan_location": "Subject/Data Path/Name Space"
            },
            "mapper": {
                "team": "DP - Mapper",
                "test_plan_location": "Subject/Data Path/Mapper"
            },
            "cache": {
                "team": "DP - Cache",
                "test_plan_location": "Subject/Data Path/Cache"
            },
        }
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(levelname)s]  %(filename)s %(message)s')
        self._logger = logging.getLogger(__name__)
        logging.getLogger("requests").setLevel(logging.WARNING)

    def _get_xml_node_from_url(self, request_url, params = None):
        """send get request to UTMS webserver.

                Args:
                    request_url (str): the URL of the request
                    params(dict): the hash list including below key and value:
                       key: query   specify the query request
                       value: name=[value1 [OR value2]] the name of the query
                Returns:
                    The xml format value from UTMS such as below:
                    <Entities TotalResults="<item_count>">
                       <Entity Type="<request_type>">
                           <Fields>
                               <Field name="xx"><Value>xxxx</Value></Field>
                               ...
                           </Fields>
                        </Entity>
                    </Entities>

        """
        # retry 5 times for request as sometimes the request will be failed
        retry = 5
        tree = None
        for i in range(0,retry):
            try:
                r = requests.get(request_url, params=params)
                tree = ElementTree.fromstring(r.content)
                break
            except Exception as e:
               self._logger.warn("Warnning: Failed to fetch {}".format(request_url))
               self._logger.warn(e)
               self._logger.debug("retry after sleeping 3 seconds")
               time.sleep(3)
        if(tree == None):
            raise UTMSParserExection("Warnning:Can't get the result from " + request_url)
        #if(self._logger.level == logging.DEBUG):
            #self._print_xml_node(tree)
        return tree

    def _post_xml_node_from_url(self, request_url, data=None):
        """send post request to UTMS webserver.

            Args:
                request_url (str): the URL of the request
                data(xml): the xml format data for posting the request such as below:
                   <Entity Type="test-instance">
                    <Fields>
                                    <Field Name="cycle-id">
                                                    <Value>1366</Value>
                                    </Field>
                                    <Field Name="status">
                                                    <Value>No Run</Value>
                                    </Field>
                                    <Field Name="test-id">
                                                    <Value>1140</Value>
                                    </Field>
                                    <Field Name="test-instance">
                                                    <Value>1</Value>
                                    </Field>
                                    <Field Name="subtype-id">
                                                    <Value>hp.qc.test-instance.MANUAL</Value>
                                    </Field>
                                    <Field Name="test-order">
                                                    <Value>1</Value>
                                    </Field>
                    </Fields>
                  </Entity>

                Returns:
                    The xml format value posted for the request:
                    <Entities TotalResults="<item_cout>">
                       <Entity Type="<request_type>">
                           <Fields>
                               <Field name="xx"><Value>xxxx</Value></Field>
                               ...
                           </Fields>
                        </Entity>
                    </Entities>
       """
        # retry 5 times for request as sometimes the request will be failed
        retry = 5
        tree = None
        headers = {'Content-Type': 'application/xml'}
        for i in range(0, retry):
            try:
                r = requests.post(request_url, data=data, headers=headers)
                tree = ElementTree.fromstring(r.content)
                break
            except Exception as e:
                self._logger.warn("Warnning: Failed to fetch {}".format(request_url))
                self._logger.warn(e)
                self._logger.debug("retry after sleeping 3 seconds")
                time.sleep(3)
        if (tree == None):
            raise UTMSParserExection("Error:Can't post the data to " + request_url)
        if(self._logger.level == logging.DEBUG):
            self._print_xml_node(tree)
        return tree

    def _put_xml_node_from_url(self, request_url, data=None):
        """send post request to UTMS webserver.

            Args:
                request_url (str): the URL of the request
                data(xml): the xml format data for posting the request such as below:
                   <Entity Type="test-instance">
                    <Fields>
                                    <Field Name="cycle-id">
                                                    <Value>1366</Value>
                                    </Field>
                                    <Field Name="status">
                                                    <Value>No Run</Value>
                                    </Field>
                                    <Field Name="test-id">
                                                    <Value>1140</Value>
                                    </Field>
                                    <Field Name="test-instance">
                                                    <Value>1</Value>
                                    </Field>
                                    <Field Name="subtype-id">
                                                    <Value>hp.qc.test-instance.MANUAL</Value>
                                    </Field>
                                    <Field Name="test-order">
                                                    <Value>1</Value>
                                    </Field>
                    </Fields>
                  </Entity>

                Returns:
                    The xml format value posted for the request:
                    <Entities TotalResults="<item_cout>">
                       <Entity Type="<request_type>">
                           <Fields>
                               <Field name="xx"><Value>xxxx</Value></Field>
                               ...
                           </Fields>
                        </Entity>
                    </Entities>
       """
        # retry 5 times for request as sometimes the request will be failed
        retry = 5
        tree = None
        headers = {'Content-Type': 'application/xml'}
        for i in range(0, retry):
            try:
                r = requests.put(request_url, data=data, headers=headers)
                tree = ElementTree.fromstring(r.content)
                break
            except Exception as e:
                self._logger.warn("Warnning: Failed to fetch {}".format(request_url))
                self._logger.warn(e)
                self._logger.debug("retry after sleeping 3 seconds")
                time.sleep(3)
        if (tree == None):
            raise UTMSParserExection("Error:Can't post the data to " + request_url)
        if (self._logger.level == logging.DEBUG):
            self._print_xml_node(tree)
        return tree
    def get_user_name(self, e_mail = "bob.yan@emc.com"):
        """get the user name according to the e-mail address.

                Args:
                    e_mail (str): the e-mail address

                Returns:
                    the user name of the e-mail

        """
        request_url = "http://" + self.http_server + "/users/" + self.domain + "/"  + self.project + "/" + e_mail
        node = self._get_xml_node_from_url(request_url)
        self._print_xml_node(node)
        name = node.attrib["Name"]
        return name

    def find_test_case_node(self, case_path):
        """get the test case node according to the case path.

                Args:
                    case_path (str): the case path defined in UTMS test plan
                                     such as Data Path/Storage Management/raid_degrad_with_io

                Returns:
                    the xml node of the case which including all basic information of the case in UTMS
                    or None if it has not found the case in the specified path.

        """
        request_url = "http://" + self.http_server + "/tests/" + self.domain + "/" + self.project
        basename = os.path.basename(case_path)
        params = {"query": "{name['" + basename + "']}"}
        root_node = self._get_xml_node_from_url(request_url, params)
        test_set_nodes = root_node.findall(".//Fields")
        case_node = None
        if (len(test_set_nodes) >= 1):
            parent_dir = os.path.dirname(case_path)
            for mached_node in reversed(test_set_nodes):
                parent_id = mached_node.find(".//Field[@Name='parent-id']/Value").text
                folder_ids = self.find_folder_id(parent_dir, folder_tag = "test-folders", current_folder_id=parent_id)
                if (folder_ids != None):
                    case_node = mached_node
                    break
        if (case_node != None):
            self._logger.debug( case_node.find(".//Field[@Name='parent-id']/Value").text \
                  + "->" + case_node.find(".//Field[@Name='id']/Value").text \
                  + ":" + case_node.find(".//Field[@Name='name']/Value").text)

        else:
            self._logger.debug("Can't find the node for {}".format(case_path))
        return case_node
    def find_test_case_node_by_id(self, case_id):
        """get the test case node according to the parent id.

                                Args:
                                    case_path (str): the case path defined in UTMS test plan
                                                     such as Data Path/Storage Management/raid_degrad_with_io

                                Returns:
                                    the xml node of the case which including all basic information of the case in UTMS
                                    or None if it has not found the case in the specified path.

                        """
        request_url = "http://" + self.http_server + "/tests/" + self.domain + "/" + self.project + "/" + case_id
        root_node = self._get_xml_node_from_url(request_url)
        test_set_nodes = root_node.findall(".//Fields")
        return test_set_nodes[0]
    def find_test_case_nodes_by_parent_id(self, parent_id):
        """get the test case node according to the parent id.

                        Args:
                            case_path (str): the case path defined in UTMS test plan
                                             such as Data Path/Storage Management/raid_degrad_with_io

                        Returns:
                            the xml node of the case which including all basic information of the case in UTMS
                            or None if it has not found the case in the specified path.

                """
        request_url = "http://" + self.http_server + "/tests/" + self.domain + "/" + self.project
        params = {"query": "{parent-id['" + parent_id + "']}"}
        root_node = self._get_xml_node_from_url(request_url, params)
        test_set_nodes = root_node.findall(".//Fields")
        return test_set_nodes
    def find_test_instance_node(self, test_set_id):
        """get the instance node according to the test set id

                Args:
                    test_set_id (str): the id of the test set in UTMS test lab

                Returns:
                    the xml node of the instance which including all basic information of the instance in UTMS
                    or None if it has not found the instance in the specified path.

        """
        request_url = "http://" + self.http_server + "/test-instances/" + self.domain + "/" + self.project
        params  = {"testsetid" : test_set_id}
        root_node = self._get_xml_node_from_url(request_url, params)
        instance_nodes = root_node.findall(".//Fields")
        for instance_node in instance_nodes:
            if (instance_node != None):
                self._logger.debug(instance_node.find(".//Field[@Name='status']/Value").text \
                      + "->" + instance_node.find(".//Field[@Name='id']/Value").text \
                      + ":" + instance_node.find(".//Field[@Name='test-order']/Value").text \
                      + ":" + instance_node.find(".//Field[@Name='test-id']/Value").text)
        if(len(instance_nodes) == 0):
            self._logger.debug("Can't find the node for {}".format(instance_nodes))
        return instance_nodes

    def find_config_node_by_id(self, test_config_id):

        request_url = "http://" + self.http_server + "/test-configs/" + self.domain + "/" + self.project
        params = {"query": "{id['" + test_config_id + "']}"}
        root_node = self._get_xml_node_from_url(request_url, params)
        test_node = root_node.find(".//Fields")
        return test_node

    def find_test_set_by_id(self, test_set_id):
        """get the instance node according to the test set id

                Args:
                    test_set_id (str): the id of the test set in UTMS test lab

                Returns:
                    the xml node of the instance which including all basic information of the instance in UTMS
                    or None if it has not found the instance in the specified path.

        """
        request_url = "http://" + self.http_server + "/test-sets/" + self.domain + "/" + self.project
        params  = {"query" : "{id['" + test_set_id + "']}"}
        root_node = self._get_xml_node_from_url(request_url, params)
        test_node = root_node.find(".//Fields")
        return test_node

    def find_test_set_patent_node(self, test_set_node):
        """get the instance node according to the test set id

                Args:
                    test_set_id (str): the id of the test set in UTMS test lab

                Returns:
                    the xml node of the instance which including all basic information of the instance in UTMS
                    or None if it has not found the instance in the specified path.

        """
        parent_id = test_set_node.find(".//Field[@Name='parent-id']/Value").text
        request_url = "http://" + self.http_server + "/test-set-folders/" + self.domain + "/" + self.project
        params  = {"query" : "{id['" + parent_id + "']}"}
        root_node = self._get_xml_node_from_url(request_url, params)
        parent_node = root_node.find(".//Fields")
        return parent_node


    def find_test_set_node(self, test_set_path):
        """get the test set node according to the test set path.

                Args:
                    test_set_path (str): the test set path defined in UTMS test lab
                                         such as PSI21/Data Path/F211/raid_degrad_with_io

                Returns:
                    the xml node of the test set which including all basic information of the test set in UTMS
                    or None if it has not found the test set in the specified path.

        """
        request_url = "http://" + self.http_server + "/test-sets/" + self.domain + "/" + self.project
        basename = os.path.basename(test_set_path)
        params = {"query" : "{name['" + basename + "']}"}
        root_node = self._get_xml_node_from_url(request_url, params)
        test_set_nodes = root_node.findall(".//Fields")
        test_set_node = None
        if(len(test_set_nodes) >= 1):
            parent_dir = os.path.dirname(test_set_path)
            for mached_node in reversed(test_set_nodes):
                parent_id = mached_node.find(".//Field[@Name='parent-id']/Value").text
                folder_ids = self.find_folder_id(parent_dir, folder_tag = "test-set-folders", current_folder_id = parent_id)
                if(folder_ids != None):
                    test_set_node = mached_node
                    break
        if (test_set_node != None):
            self._logger.debug( "test set info:" + test_set_node.find(".//Field[@Name='parent-id']/Value").text \
                  + "->" + test_set_node.find(".//Field[@Name='id']/Value").text \
                  + ":" + test_set_node.find(".//Field[@Name='name']/Value").text)

        else:
            self._logger.debug("Can't find the node for {}".format(test_set_path))
        return test_set_node

    def find_test_set_node_by_parent_id(self, parent_id):
        """get the test set node according to the test set path.

                        Args:
                            test_set_path (str): the test set path defined in UTMS test lab
                                                 such as PSI21/Data Path/F211/raid_degrad_with_io

                        Returns:
                            the xml node of the test set which including all basic information of the test set in UTMS
                            or None if it has not found the test set in the specified path.

                """
        request_url = "http://" + self.http_server + "/test-sets/" + self.domain + "/" + self.project
        params = {"query": "{parent-id['" + parent_id + "']}"}
        root_node = self._get_xml_node_from_url(request_url, params)
        test_set_nodes = root_node.findall(".//Fields")
        return test_set_nodes

    def find_test_set_by_path(self, path, folder_id = None):
        test_node_dict = {}
        if folder_id is None:
            folder_ids = self.find_folder_id(path, "test-set-folders")
            folder_id = os.path.basename(folder_ids)
        test_set_nodes = self.find_test_set_node_by_parent_id(folder_id)
        if test_set_nodes:
            test_node_dict[path] = test_set_nodes
        else:
            request_url = "http://" + self.http_server + "/" + "test-set-folders" + "/" + self.domain + "/" + self.project
            params = {"query": "{parent-id['" + folder_id + "']}"}
            root_node = self._get_xml_node_from_url(request_url, params)
            path_nodes = root_node.findall(".//Fields")
            for path_node in path_nodes:
                sub_path = path_node.find(".//Field[@Name='name']/Value").text
                sub_path_id = path_node.find(".//Field[@Name='id']/Value").text
                sub_nodes = self.find_test_set_by_path(path + "/" + sub_path, sub_path_id)
                if sub_nodes:
                    test_node_dict.update(sub_nodes)
        return test_node_dict

    def find_folder_id(self, folder_path, folder_tag = "test-folders", current_folder_id = None):
        """get the folder node according to the folder path

                Args:
                    folder_path (str): the folder path defined in UTMS
                                       such as PSI21/Data Path/F211
                    folder_tag (str): the folder tag
                                      test-folders is for test plan
                                      test-set-folders is for test lab
                    current_folder_id(str): if not None, which means to verify if the folder with the id has the
                                       expected folder path.

                Returns:
                    the id path of the id, if it's None which means it's not the correct path.
                    Example:
                        input: PSI21/Data Path/F211
                        output:
                               1112/1321/311   it means the path is existed and the full id path is found.
                               1112/1321       it means the PSI21/Data Path is existed but F211 is not existed
                               None            it means there is no such path

        """
        request_url = "http://" + self.http_server + "/" + folder_tag + "/" + self.domain + "/" + self.project
        folders = folder_path
        query_names = ""
        while(folders != "/" and folders != ""):
            basename = os.path.basename(folders)
            folders = os.path.dirname(folders)
            if(query_names != ""):
                query_names += " OR "
            query_names += "'" + basename + "'"
        params = {"query" : "{name[" + query_names + "]}"}
        root_node = self._get_xml_node_from_url(request_url, params)
        #it should be "parentid/subparentid/folderid"
        path_ids = None
        if(current_folder_id != None):
            path_ids = self._get_matched_id_path(root_node, folder_path, current_folder_id)
        else:
            path_ids = self._get_path_id(root_node, folder_path)
        return path_ids
    def _print_xml_node(self, node):
        """print the xml node information, it's used to debug the return information from UTMS

                Args:
                    node (xml.etree.Element): the xml element from UTMS

                Returns:
                    None
        """
        rough_string = ElementTree.tostring(node, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        self._logger.info(reparsed.toprettyxml(indent="\t"))

    def get_and_create_testcase(self, case_path, team_name, owner, script_name = None, description = None):
        """get the test case node, if it's not existed, it will create a new one and return the new node

                Args:
                    case_path (str): the case path defined in UTMS test plan
                                     such as Data Path/Storage Management/raid_degrad_with_io
                    team_name (str): the team name for the case such as DP - Storage Management
                    owner(str)     : the user name defined in UTMS
                    script_name(str): the script full path, if it's None, it will use the case name
                    description(str): the description for the case, the default it will be generated automatically

                Returns:
                    the xml node of the case which including all basic information of the test plan in UTMS

        """
        self._logger.debug("Fetching the case " + case_path)
        case_node = self.find_test_case_node(case_path)
        if(case_node == None):
            self._logger.debug("Creating test case :" + case_path)
            case_name = os.path.basename((case_path))
            if(script_name == None):
                script_name = case_name + ".json"
            if(description == None):
                description = "Generate " + case_name +" automatically by dpsmoke_automatos"
            folder_path = os.path.dirname(case_path)
            parent_id = self.get_and_create_folder_id(folder_path)
            xml_string = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>" \
                         + "<Entity Type=\"test\">" \
                         + "  <Fields>" \
                         + "    <Field Name=\"test-name\"><Value>" + case_name + "</Value></Field>" \
                         + "    <Field Name=\"execution-type\"><Value>MANUAL</Value></Field>" \
                         + "    <Field Name=\"parent-id\"><Value>" + parent_id + "</Value></Field>" \
                         + "    <Field Name=\"subtype-id\"><Value>MANUAL</Value></Field>" \
                         + "    <Field Name=\"team\"><Value>" + team_name + "</Value></Field>" \
                         + "    <Field Name=\"old-team\"><Value>" + team_name + "</Value></Field>" \
                         + "    <Field Name=\"status\"><Value>" + "Ready" + "</Value></Field>" \
                         + "    <Field Name=\"exclusive\"><Value>N</Value></Field>" \
                         + "    <Field Name=\"priority\"><Value>1-High</Value></Field>" \
                         + "    <Field Name=\"remotely-executable\"><Value>Yes</Value></Field>" \
                         + "    <Field Name=\"test-state\"><Value>Automated</Value></Field>" \
                         + "    <Field Name=\"automation-dev-framework\"><Value>Automatos-Python</Value></Field>" \
                         + "    <Field Name=\"script-name\"><Value>" + script_name  + "</Value></Field>" \
                         + "    <Field Name=\"execution-engine\"><Value>Automatos</Value></Field>" \
                         + "    <Field Name=\"automation-script-owner\"><Value>" + owner + "</Value></Field>" \
                         + "    <Field Name=\"description\"><Value>" + description + "</Value></Field>" \
                         + "  </Fields>" \
                         + "</Entity>"
            request_url = "http://" + self.http_server + "/tests/" + self.domain + "/" + self.project
            case_node = self._post_xml_node_from_url(request_url, xml_string)
            #self._print_xml_node(case_node)
        return case_node
    def get_and_create_test_set(self, test_set_path, team_name, owner, script_name = None, description = None, start_time = None, end_time = None):
        """get the test set node, if it's not existed, it will create a new case node and test set node
           and return the new test set node

                Args:
                    test_set_path (str): the test set path defined in UTMS test lab
                                         such as PSI21/Data Path/F211/raid_degrad_with_io
                    team_name (str): the team name for the case such as DP - Storage Management
                    owner(str)     : the user name defined in UTMS
                    script_name(str): the script full path, if it's None, it will use the case name
                    description(str): the description for the case, the default it will be generated automatically
                    start_time(str): the start time of the test set, the default is now
                    end_time(str):   the end time of the test set, the default is start_time + 2 weeks

                Returns:
                    the xml node of the test set which including all basic information of the test plan in UTMS

        """
        test_set_node = self.find_test_set_node(test_set_path)
        if(test_set_node == None):
            case_name = os.path.basename(test_set_path)
            case_full_path = self.get_case_path_by_team_name(team_name) + "/" + case_name
            case_node = self.get_and_create_testcase(case_full_path, team_name, owner, script_name, description)
            case_id = case_node.find(".//Field[@Name='id']/Value").text
            test_set_node = self.create_testset(test_set_path, owner, start_time, end_time)
            test_set_id = test_set_node.find(".//Field[@Name='id']/Value").text
            instance_node = self.create_instance_for_test_set(case_id, test_set_id)
            if(instance_node == None):
                raise UTMSParserExection("Error:Can't create test set node successfully")
        return test_set_node
    def create_testset(self, test_set_path, owner, start_time = None, end_time = None):
        """it creates a new test set node and return the new test set node

                Args:
                    test_set_path (str): the test set path defined in UTMS test lab
                                         such as PSI21/Data Path/F211/raid_degrad_with_io
                    owner(str)     : the user name defined in UTMS
                    start_time(str): the start time of the test set, the default is now
                    end_time(str):   the end time of the test set, the default is start_time + 2 weeks

                Returns:
                    the xml node of the test set which including all basic information of the test plan in UTMS

        """
        self._logger.debug("Creating test set :" + test_set_path)
        test_set_name = os.path.basename((test_set_path))
        folder_path = os.path.dirname(test_set_path)
        parent_id = self.get_and_create_folder_id(folder_path, folder_tag="test-set-folders")
        date_format = "%Y-%m-%d"
        interation_days = 14
        if (start_time == None):
            start_time = time.strftime(date_format)
        if (end_time == None):
            start_date = datetime.datetime.strptime(start_time, date_format)
            end_date = start_date + datetime.timedelta(days=interation_days)
            end_time = end_date.strftime(date_format)

        xml_string = "<Entity Type=\"test-set\">" \
                     + "  <Fields>" \
                     + "    <Field Name=\"name\"><Value>" + test_set_name + "</Value></Field>" \
                     + "    <Field Name=\"parent-id\"><Value>" + parent_id + "</Value></Field>" \
                     + "    <Field Name=\"subtype-id\"><Value>hp.qc.test-set.default</Value></Field>" \
                     + "    <Field Name=\"created-by\"><Value>" + owner + "</Value></Field>" \
                     + "    <Field Name=\"planned-end-date\"><Value>" + start_time + "</Value></Field>" \
                     + "    <Field Name=\"planned-start-date\"><Value>" + end_time + "</Value></Field>" \
                     + "    <Field Name=\"test-set-status\"><Value>Ready</Value></Field>" \
                     + "  </Fields>" \
                     + "</Entity>"
        request_url = "http://" + self.http_server + "/test-sets/" + self.domain + "/" + self.project
        test_set_node = self._post_xml_node_from_url(request_url, xml_string)
        return test_set_node

    def create_instance_for_test_set(self, case_id, test_set_id):
        """it creates a new test instance node and return the new test instance node
                Args:
                    case_id (str): the test case id for the test instance
                    test_set_id(str) : the test set id for the instance

                Returns:
                    the new xml node of the test intance
        """
        self._logger.debug("Creating test instance for test case:{} and test set:{}".format(case_id, test_set_id))
        xml_string = "<Entity Type=\"test-instance\">" \
                     + "  <Fields>" \
                     + "    <Field Name=\"cycle-id\"><Value>" + test_set_id + "</Value></Field>" \
                     + "    <Field Name=\"status\"><Value>No Run</Value></Field>" \
                     + "    <Field Name=\"test-id\"><Value>" + case_id + "</Value></Field>" \
                     + "    <Field Name=\"test-instance\"><Value>1</Value></Field>" \
                     + "    <Field Name=\"subtype-id\"><Value>hp.qc.test-instance.MANUAL</Value></Field>" \
                     + "    <Field Name=\"test-order\"><Value>1</Value></Field>" \
                     + "    <Field Name=\"owner\"><Value>yanb</Value></Field>" \
                     + "  </Fields>" \
                     + "</Entity>"
        request_url = "http://" + self.http_server + "/test-instances/" + self.domain + "/" + self.project
        test_set_node = self._post_xml_node_from_url(request_url, xml_string)
        #self._print_xml_node(test_set_node)
        return test_set_node

    def get_and_create_folder_id(self, path, folder_tag="test-folders"):
        """it find the folder nodes, it there is no such folder it will create it and return the folder node
            Args:
                path (str): the folder path such as Data Path/Storage Management
                folder_tag(str) : the folder tag
                                  test-folders is for test plan
                                  test-set-folders is for test lab

            Returns:
                the folder node of xml format
        """
        path_ids = self.find_folder_id(path, folder_tag)
        folder_id = None
        if(path_ids == None):
            self._logger.debug("can't find the root path for " + path)
        else:
            id_list = path_ids.split("/")
            path_list = path.split("/")
            if(len(id_list) == len(path_list)):
                self._logger.debug("folder[{}] is existed id path is {}, skip creation".format(path, path_ids))
                folder_id = id_list[-1]
            else:
                index = len(id_list) - 1
                parent_id = id_list[index]
                new_node = None
                while (index < len(path_list) - 1):
                    child_folder = path_list[index + 1]
                    new_node = self._create_folder_under_parent(parent_id, child_folder, folder_tag)
                    #self._print_xml_node(new_node)
                    index = index + 1
                    parent_id = new_node.find(".//Field[@Name='id']/Value").text
                if(new_node != None):
                    folder_id = new_node.find(".//Field[@Name='id']/Value").text
        return folder_id

    def _create_folder_under_parent(self, parent_id, folder_name, folder_tag="test-folders"):
        """it finds the folder nodes, it there is no such folder it will create it and return the folder node
            Args:
                path (str): the folder path such as Data Path/Storage Management
                folder_tag(str) : the folder tag
                                  test-folders is for test plan
                                  test-set-folders is for test lab

            Returns:
                the folder node of xml format
        """
        entity_name = folder_tag[:-1]
        field_names = {
            "test-folders" : "test-folder-name",
            "test-set-folders" : "name"
        }
        xml_string = "<Entity Type=\"" + entity_name + "\">"\
                     + "<Fields>" \
                     + "<Field Name=\"parent-id\"><Value>" + str(parent_id) + "</Value></Field>" \
                     + "<Field Name=\"" + field_names[folder_tag] + "\"><Value>" + folder_name + "</Value></Field>"  \
                     +"</Fields>" \
                     +"</Entity>"
        request_url = "http://" + self.http_server + "/" + folder_tag + "/" + self.domain + "/" + self.project
        result = self._post_xml_node_from_url(request_url, xml_string)
        #self._print_xml_node(result)
        return result

    def _get_path_id(self, root_node, path):
        """Get the id path under the root_node
            Args:
                root_node: the xml root node of the folder information
                path (str): the folder path such as Data Path/Storage Management

            Returns:
                the folder node of xml format
                Example:
                        input: PSI21/Data Path/F211
                        output:
                               1112/1321/311   it means the path is existed and the full id path is found.
                               1112/1321       it means the PSI21/Data Path is existed but F211 is not existed
                               None            it means there is no such path
        """
        folder_id_paths = []
        current_path = path
        while(current_path != ""):
            basename = os.path.basename(current_path)
            matchedNodes = root_node.findall(".//Field[@Name='name'][Value='{}']/..".format(basename))
            for matchedNode in matchedNodes:
                folder_id = matchedNode.find(".//Field[@Name='id']/Value").text
                path_id = self._get_matched_id_path(root_node, current_path, folder_id)
                #if path_id is None, which means the parent path of current folder is not matched with expecting path
                if(path_id != None):
                    folder_id_paths.append(path_id)
            if(len(folder_id_paths) > 0):
                break
            current_path = os.path.dirname(current_path)
        if(len(folder_id_paths) > 1):
            raise UTMSParserExection("There are multiple folders found")
        id_path = None
        if(len(folder_id_paths) == 1):
            id_path = folder_id_paths[0]
        return id_path
    def _get_matched_id_path(self, root_node, path, id):
        """Get the id path for the specified path id,
           if all parent folder of the current folder id is matched with the path, then it will return
           the id path or it will return None
            Args:
                root_node: the xml root node of the folder information
                path (str): the folder path such as Data Path/Storage Management
                id (str):  the id of the current folder id

            Returns:
                the folder node of xml format
                Example:
                        input: PSI21/Data Path/F211
                        output:
                               1112/1321/311   it means the path is matched and the id path is found
                               None            it means current path is not matched
        """
        basename = os.path.basename(path)
        parent_dir = os.path.dirname(path)
        expected_node = root_node.find(".//Field[@Name='id'][Value='{}']/..".format(id))
        parent_id_path = None
        if( expected_node != None and expected_node.find(".//Field[@Name='name']/Value").text == basename):
            parent_id = expected_node.find(".//Field[@Name='parent-id']/Value").text
            if(os.path.basename(parent_dir) != ""):
                parent_id_path = self._get_matched_id_path(root_node, parent_dir, parent_id)
                if(parent_id_path != None):
                    parent_id_path += "/" + id
            else:
                parent_id_path = parent_dir + id
        return parent_id_path


    def get_utms_info_by_path_and_scriptname(self, utms_testset_path, script_name):
        """Get the test set id, intance count and instance order
           return testsetid_instancecount_instanceorder
           such as 383_2_1 means testset id is 383, 2 instances the order of the script_name is 1
        """
        test_set_info = None
        test_set_node = self.find_test_set_node(utms_testset_path)
        if test_set_node is None:
            folder_ids = self.find_folder_id(utms_testset_path, "test-set-folders")
            folder_id = os.path.basename(folder_ids)
            testset_nodes = self.find_test_set_node_by_parent_id(folder_id)
            for testset_node in testset_nodes:
                test_set_id = testset_node.find(".//Field[@Name='id']/Value").text
                instance_info = self.get_instance_by_scriptname(test_set_id, script_name)
                if instance_info:
                    test_set_info = {"test_set_id": test_set_id}
                    test_set_info.update(instance_info)
                    break
        else:
            test_set_id = test_set_node.find(".//Field[@Name='id']/Value").text
            instance_info = self.get_instance_by_scriptname(test_set_id, script_name)
            if instance_info:
                test_set_info = {"test_set_id": test_set_id}
                test_set_info.update(instance_info)
        return test_set_info

    def get_instance_by_scriptname(self, testset_id, script_name):
        instance_nodes = self.find_test_instance_node(testset_id)
        instance_info = None
        i = 0
        script_base_name = os.path.basename(script_name)
        if script_base_name.rfind(".") > 0:
            script_base_name = script_base_name[0:script_base_name.rindex(".")]
        for instance_node in instance_nodes:
            i += 1
            case_id = instance_node.find(".//Field[@Name='test-id']/Value").text
            case_node = self.find_test_case_node_by_id(case_id)
            script_full_name = case_node.find(".//Field[@Name='user-template-05']/Value").text
            if script_full_name:
                def_script_name = os.path.basename(script_full_name)
                #self._logger.info("full name " + script_full_name)
                #self._logger.info("script :" + def_script_name)
                if def_script_name.rfind(".") > 0 :
                    def_script_name = def_script_name[0:def_script_name.rindex(".")]
                if def_script_name.lower() == script_base_name.lower() :
                    instance_info = {
                        "instance_count" : len(instance_nodes),
                        "instance_order" : i
                    }
                    break
        return instance_info


    def get_case_path_by_team_name(self, team_name):
        """Get the case path according to the team name
            Args:
                team_name: the team name such as DP - Storage Management
            Returns:
                the case path defined in UTMS test plan
        """
        case_path = None
        for team_info_key in self.basic_information.keys():
            team_info = self.basic_information[team_info_key]
            if(team_info["team"] == team_name):
                case_path = team_info["test_plan_location"]
                break
        return case_path

    def get_team_name_by_case_name(self, case_name):
        """Get the team name according to case name
           the case name should be use the team name as the prefix of the case
            Args:
                case_name: the case name, it should use team name as prefix such as
                           raid_xxxx
                           namespace_xxxx
                           cache_xxx
                           mapper_xxx
            Returns:
                the team name
        """
        team_name = None
        prefix_case = case_name[:case_name.index["_"]]
        for team_info_key in self.basic_information.keys():
            team_info = self.basic_information[team_info_key]
            if (team_info_key == prefix_case):
                team_name = team_info["team"]
                break
        return team_name

    def create_run_for_utms_path(self, utms_testset_path, ibid = "0", status = "Passed", email = "bob.yan@emc.com",
                                 script_name = None, instance_order = None, howrun="MANUAL", team="ST-Xichang",
                                 ar_number=None):
        test_set_info = None
        test_set_node = self.find_test_set_node(utms_testset_path)
        instance_nodes = []
        uname = self.get_user_name(email)
        if test_set_node is None:
            folder_ids = self.find_folder_id(utms_testset_path, "test-set-folders")
            folder_id = os.path.basename(folder_ids)
            testset_nodes = self.find_test_set_node_by_parent_id(folder_id)
            for testset_node in testset_nodes:
                test_set_id = testset_node.find(".//Field[@Name='id']/Value").text
                test_instance_nodes = self.find_test_instance_node(test_set_id)
                if script_name:
                    instance_info = self.get_instance_by_scriptname(test_set_id, script_name)
                    if instance_info:
                        index = int(instance_info["instance_order"])
                        instance_nodes.append(test_instance_nodes[index])
                elif instance_order is not None:
                    if type(instance_order) is list:
                        for order in instance_order:
                            instance_nodes.append(test_instance_nodes[order - 1])
                    else:
                        instance_nodes.append(test_instance_nodes[instance_order - 1])
                else:
                    instance_nodes.extend(test_instance_nodes)
        else:
            test_set_id = test_set_node.find(".//Field[@Name='id']/Value").text
            test_instance_nodes = self.find_test_instance_node(test_set_id)
            if script_name:
                instance_info = self.get_instance_by_scriptname(test_set_id, script_name)
                if instance_info:
                    index = int(instance_info["instance_order"])
                    instance_nodes.append(test_instance_nodes[index])
            elif instance_order is not None:
                if type(instance_order) is list:
                    for order in instance_order:
                        instance_nodes.append(test_instance_nodes[order - 1])
                else:
                    instance_nodes.append(test_instance_nodes[instance_order - 1])
            else:
                instance_nodes.extend(test_instance_nodes)
        link_info = []
        for instance_node in instance_nodes:
            test_set_id = instance_node.find(".//Field[@Name='cycle-id']/Value").text
            test_id = instance_node.find(".//Field[@Name='test-id']/Value").text
            instance_id = instance_node.find(".//Field[@Name='id']/Value").text
            self._logger.info("create run instance for test_set_id={}, test_id = {}, instance_id = {}".format(test_set_id, test_id, instance_id))
            running_node = self.create_test_run( test_set_id=test_set_id, test_id=test_id, test_instance_id=instance_id, owner=uname, ibid=ibid, status=status, howrun=howrun, team=team, ar_id=ar_number)
            running_id = running_node.find(".//Field[@Name='id']/Value").text
            link_info.append("_".join([test_set_id, test_id, instance_id, running_id]))
        return link_info

    def create_test_run(self, test_set_id, test_id, test_instance_id, owner, ibid, status = "Passed", howrun="MANUAL", team="ST-Xichang",
                        ar_id=None):
        date_format = "%m-%d_%H-%M-%S"
        create_time = time.strftime(date_format)
        run_name = "Run_" + create_time
        self._logger.debug("Creating test defect for test ar:{} ".format(ar_id))
        xml_string = "<Entity Type=\"run\">" \
                     + "  <Fields>" \
                     + "    <Field Name=\"test-set-id\"><Value>" + test_set_id + "</Value></Field>" \
                     + "    <Field Name=\"test-id\"><Value>" + test_id + "</Value></Field>" \
                     + "    <Field Name=\"test-instance-id\"><Value>" + test_instance_id + "</Value></Field>" \
                     + "    <Field Name=\"name\"><Value>" + run_name + "</Value></Field>" \
                     + "    <Field Name=\"owner\"><Value>" + owner + "</Value></Field>" \
                     + "    <Field Name=\"subtype-id\"><Value>hp.qc.run.MANUAL</Value></Field>" \
                     + "    <Field Name=\"status\"><Value>" + status + "</Value></Field>" \
                     + "    <Field Name=\"build-id\"><Value>" + ibid + "</Value></Field>" \
                     + "    <Field Name=\"team\"><Value>" + team + "</Value></Field>" \
                     + "    <Field Name=\"how-run\"><Value>" + howrun + "</Value></Field>" \
                     + "  </Fields>" \
                     + "</Entity>"

        self._logger.info(xml_string)
        request_url = "http://" + self.http_server + "/test-runs/" + self.domain + "/" + self.project
        test_run_node = self._post_xml_node_from_url(request_url, xml_string)
        #self._print_xml_node(test_run_node)
        if ar_id:
            run_id = test_run_node.find(".//Field[@Name='id']/Value").text
            xml_string = "<Entity Type=\"run\">" \
                     + "  <Fields>" \
                     + "    <Field Name=\"ticket-id\"><Value>" + ar_id + "</Value></Field>" \
                     + "    <Field Name=\"ticket-classification\"><Value>JIRA</Value></Field>" \
                     + "    <Field Name=\"owner\"><Value>" + owner + "</Value></Field>" \
                     + "  </Fields>" \
                     + "</Entity>"
            request_url = "http://" + self.http_server + "/test-runs/" + self.domain + "/" + self.project + "/" + run_id
            test_run_node = self._put_xml_node_from_url(request_url, xml_string)
            #self._print_xml_node(test_run_node)
        return test_run_node

    def update_run_instance_status(self, running_id, status = "Passed", howrun = None, duration = None, host = None, ar_number = None, email = "bob.yan@emc.com"):
        xml_string = "<Entity Type=\"run\">" + "  <Fields>"
        if status is not None :
            xml_string += "    <Field Name=\"status\"><Value>" + status + "</Value></Field>"
        if howrun is not None :
            xml_string += "    <Field Name=\"how-run\"><Value>" + howrun + "</Value></Field>"
        if duration is not None:
            xml_string += "    <Field Name=\"duration\"><Value>" + duration + "</Value></Field>"
        if host is not None:
            xml_string += "    <Field Name=\"host\"><Value>" + host + "</Value></Field>"
        if ar_number :
            owner = self.get_user_name(email)
            xml_string += "    <Field Name=\"ticket-id\"><Value>" + ar_number + "</Value></Field>" \
                     + "    <Field Name=\"ticket-classification\"><Value>JIRA</Value></Field>" \
                     + "    <Field Name=\"owner\"><Value>" + owner + "</Value></Field>"
        xml_string += "  </Fields>" + "</Entity>"

        request_url = "http://" + self.http_server + "/test-runs/" + self.domain + "/" + self.project + "/" + running_id
        test_run_node = self._put_xml_node_from_url(request_url, xml_string)
        return test_run_node

    def get_and_create_defect(self, ar_id, owner, priority="1-High", project="Cyclone", ar_status="Open"):
        request_url = "http://" + self.http_server + "/defects/" + self.domain + "/" + self.project
        params = {"query": "{ticket-id['" + ar_id + "']}"}
        root_node = self._get_xml_node_from_url(request_url, params)
        defect_nodes = root_node.findall(".//Fields")
        defect_node = None
        if not defect_nodes:
            defect_node = self._create_defect(ar_id, owner, priority, project, ar_status)
        else:
            defect_node = defect_nodes[-1]
        return defect_node

    def _create_defect(self, ar_id, owner, priority="1-High", project="Cyclone", ar_status="Open"):
        date_format = "%Y-%m-%d"
        create_time = time.strftime(date_format)
        self._logger.debug("Creating test defect for test ar:{} ".format(ar_id))
        xml_string = "<Entity Type=\"defect\">" \
                     + "  <Fields>" \
                     + "    <Field Name=\"ticket-id\"><Value>" + ar_id + "</Value></Field>" \
                     + "    <Field Name=\"ticket-classification\"><Value>AR</Value></Field>" \
                     + "    <Field Name=\"detected-on-date\"><Value>" + create_time + "</Value></Field>" \
                     + "    <Field Name=\"detected-by\"><Value>" + owner + "</Value></Field>" \
                     + "    <Field Name=\"priority\"><Value>" + priority + "</Value></Field>" \
                     + "    <Field Name=\"user-template-09\"><Value>" + project + "</Value></Field>" \
                     + "    <Field Name=\"status\"><Value>" + ar_status + "</Value></Field>" \
                     + "  </Fields>" \
                     + "</Entity>"
        # self._logger.info(xml_string)
        request_url = "http://" + self.http_server + "/defects/" + self.domain + "/" + self.project
        test_defect_node = self._post_xml_node_from_url(request_url, xml_string)
        # self._print_xml_node(test_set_node)
        return test_defect_node

    def main(self):
        parser = argparse.ArgumentParser(description="Fetch the test set id from UTMS and if there is no such case, "\
                                                     "it will create the test case and test set automatically")
        parser.add_argument('-t','--team', type=str, default=None,
                            help='Specify the team name of the case')
        parser.add_argument('-n', '--name', type=str,default=None,
                            help='Specify the test set name(full path) such as PSI21/Data Path/F221/raid_degrade_with_io_test ')
        parser.add_argument('-e', '--email', type=str,default=None,
                            help='Specify e-mail address of the owner')
        parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False,
                            help='Specify the debug mode')
        args = parser.parse_args()
        team = args.team
        test_set_full_path = args.name
        email = args.email
        if(test_set_full_path == None):
            return
        if(args.debug == True):
            self._logger.debug("setting log level to debug")
            self._logger.setLevel(logging.DEBUG)
        if(team == None):
            case_name = os.path.basename(test_set_full_path)
            team = self.get_team_name_by_case_name(case_name)
        if(team == None):
            raise UTMSParserExection("Can't get the team name of the test case({})".format(test_set_full_path))
        if(email == None):
            raise UTMSParserExection("e-mail address is not specified")
        user = self.get_user_name(email)
        if(user == None):
            raise UTMSParserExection("There is no user defined for e-mail:" + email)
        test_set_node = self.get_and_create_test_set(test_set_full_path, team, user)
        test_set_id = test_set_node.find(".//Field[@Name='id']/Value").text
        self._logger.info("Test_Set_Id:{}".format(test_set_id))

    def _get_instances_status_for_itag(self, test_node_info):
        search_params = ""
        node_info = {}
        for key, values in test_node_info.items():
            for test_node in values:
                test_set_name = test_node.find(".//Field[@Name='name']/Value").text
                itag_name = os.path.basename(key)
                stage_name = "Stage_1"
                if test_set_name.startswith("Stage_"):
                    stage_name = test_set_name[0:len("Stage_x")]
                test_set_id = test_node.find(".//Field[@Name='id']/Value").text
                node_info[test_set_id] = {"itage_name":itag_name, "stage_name":stage_name, "test_name":test_set_name}
                instance_nodes = self.find_test_instance_node(test_set_id)
                if instance_nodes:
                    instance_node = instance_nodes[-1]
                    status = instance_node.find(".//Field[@Name='status']/Value").text
                    node_info[test_set_id]["status"] = status
                else:
                    node_info[test_set_id]["status"] = "No Instance"
        return node_info

    def build_report(self, file_name = "utms_report.csv"):
        root_folder = "0-Futures/I-Tag/Xian"
        testset_nodes = self.find_test_set_by_path(root_folder)
        csv_content = "Test,I-Tag,Stage,Status"
        node_info = self._get_instances_status_for_itag(testset_nodes)
        for node_value in node_info.values():
            csv_content += "\n{},{},{},{}".format(node_value["test_name"], node_value["itage_name"]
                                                  , node_value["stage_name"], node_value["status"])
        with open(file_name, "w") as csv_file:
            csv_file.write(csv_content)
        self._logger.info("UTMS fetcher has been completed, file path is {}".format(file_name))
        if file_name.startswith('/opt/CTEE_logs'):
            file_name = file_name.replace('/opt/CTEE_logs', 'https://easyjenkins.service.baas.darkside.cec.lab.emc.com/logs')
            self._logger.info("The result url is {}".format(file_name))

if __name__ == "__main__":
    utms_reporter = UtmsReporter()
    #utms_reporter.main()
    #uname = utms_reporter.get_user_name("William_Sharos@Dell.com")
    #folder_id = utms_reporter.get_and_create_folder_id("Appliance/Data Path")
    #in_nodes = utms_reporter.find_test_instance_node("1467")
    #print "instance_count:" + str(len(in_nodes))
    # folder_ids = utms_reporter.find_folder_id("Beta3/Regression/SL1", "test-set-folders")
    # print folder_ids
    # folder_id = os.path.basename(folder_ids)
    # print folder_id
    # case_nodes = utms_reporter.find_test_set_node_by_parent_id(folder_id)
    # #utms_reporter._print_xml_node(case_nodes[0])
    # test_set_id = case_nodes[0].find(".//Field[@Name='id']/Value").text
    # instance_nodes = utms_reporter.find_test_instance_node(test_set_id)
    # #utms_reporter._print_xml_node(instance_nodes[0])
    # case_id = instance_nodes[0].find(".//Field[@Name='test-id']/Value").text
    # case_node = utms_reporter.find_test_case_node_by_id(case_id)
    # script_name = case_node.find(".//Field[@Name='user-template-05']/Value").text
    # print script_name
    #info = utms_reporter.get_utms_info_by_path_and_scriptname("Beta2/C323", "spbm_basic_operations.py")
    #print info
    #utms_reporter.create_run_for_utms_path("Beta3/C234/Massive_Fragement_For_Dedupe", ibid="78150", ar_number="914597")
    #running_info = utms_reporter.create_run_for_utms_path("Beta3/C234/Large_IO_Create_Delete_For_Expand_Shrink", instance_order=2, ibid="79454", status = "Failed", ar_number="915369")
    # running_info = utms_reporter.create_run_for_utms_path("Beta3/C235/Massive_IO_With_Dedupe_Compression", ibid="90831", status="Failed",instance_order=2,
    #                                                        ar_number="99776", email="bob.yan@emc.com")
    #running_info = utms_reporter.create_run_for_utms_path("Beta4/DM - Remote Protection for Volume and CG/Remote_Protection_With_Snapshot_Operations", ibid="170360", ar_number="MDT-28126",
    #                                                      status="Failed", email="bob.yan@emc.com")
    # running_info = utms_reporter.create_run_for_utms_path("Beta4/Regression/SL2_C234_C235_Regression", ibid="184440", instance_order=3,  #ar_number="MDT-28580",
    #                                                       status="Passed", email="bob.yan@emc.com")

    #running_info = utms_reporter.create_run_for_utms_path("I164_I39_I167/stage_1_massive_operataions_with_dedupe_comression_IO", ibid="0.5.0.348903",
    #                                                     ar_number="MDT-37187",
    #                                                     status="Running", email="bob.yan@emc.com")
    #test_run_node = utms_reporter.update_run_instance_status(running_id="282657",
    #                                                     ar_number="MDT-40125",
     #                                                   status="Failed", email="bob.yan@emc.com")
    #utms_reporter._print_xml_node(test_run_node)

    #Wenjing.Li@emc.com
    #utms_reporter._logger.info(running_info)
    #test_node = utms_reporter.find_test_set_by_id("5968")
    #parent_node = utms_reporter.find_test_set_patent_node(test_node)
    #utms_reporter._print_xml_node(parent_node)
    #test_set_id = test_node.find(".//Field[@Name='id']/Value").text

    #instance_nodes = utms_reporter.find_test_instance_node("5968")
    #test_config_node = utms_reporter.find_config_node_by_id("35996")
    #utms_reporter._print_xml_node(test_config_node)
    #running_node = utms_reporter.update_run_instance_status("40928", status="Not Completed", host = "CNENLIW27L2C")
    #utms_reporter._print_xml_node(running_node)
    #print uname
    #utms_reporter.build_report()

    #test_id = "5968"
    #test_instances = utms_reporter.find_test_instance_node(test_id)
    #utms_reporter._print_xml_node(test_instances[0])

    #running_info = utms_reporter.create_run_for_utms_path("PSI28/I-Tag/28.2/I167/IO on volume and clone for thin provisioning", ibid="0.5.0.317092",
    #                                                       ar_number="MDT-37187",
    #                                                      status="Failed", email="helen.yan@emc.com")
    #Wenjing.Li@emc.com
    #utms_reporter._logger.info(running_info)
    #running_node = utms_reporter.update_run_instance_status("40928", status="Not Completed", host = "CNENLIW27L2C")
    #utms_reporter._print_xml_node(running_node)
    #print uname
    file_path = '/opt/CTEE_logs/mrqe/DEBUG/ST_Xichang/utms_data'
    csv_file = os.path.join(file_path, 'utms_report_{}.csv'.format(datetime.datetime.now().strftime('%Y%m%d-%H%M%S')))
    # DO_WORK_DIR = os.path.abspath(__file__ + "../../../../")
    utms_reporter.build_report(file_name=csv_file)
    report = textparser()
    report.sumbyITag(csv_file)
    report.sumbyStage(csv_file)



