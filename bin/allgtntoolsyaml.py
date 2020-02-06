#!/usr/bin/env python

# Script to fetch all the tools needed to support all the tutorials on a galaxy instance in one tool.yaml file.
# Execute this script in the root directory of GTN: `python bin/allgtntoolsyaml.py`. A 'All_GTN_tools.yaml' file will be generated in the root directory.
# tool_panel_section_label of the tools is based on the topic.
# Dependency: Ephemeris

import glob
import yaml
import os

t = open("All_GTN_tools.yaml", "w")

baseyaml = { 'install_tool_dependencies': True, 'install_repository_dependencies': True, 'install_resolver_dependencies': True , 'tools':[]}

def toolyamltodict (yamlfile, baseyaml, topic):
    for i, tool in enumerate(yamlfile['tools']):
        yamlfile['tools'][i]['tool_panel_section_label'] = topic
        baseyaml['tools'].append(tool)
    return baseyaml

topicslist = [f.name for f in os.scandir("./topics/") if f.is_dir()]
topicslist.sort()

for topic in topicslist:
    for tutorial in [s.name for s in os.scandir("./topics/{}/tutorials".format(topic)) if s.is_dir()]:

        toolpath = "./topics/{}/tutorials/{}/tools.yaml".format(topic,tutorial)
        workflowpath = "./topics/{}/tutorials/{}/workflows".format(topic,tutorial)

        if os.path.exists(workflowpath) and glob.glob("{}/*.ga".format(workflowpath)):
            for workflow in glob.glob("{}/*.ga".format(workflowpath)):
                os.system("workflow-to-tools -w {} -o {}/temp_tool.yaml".format(workflow,workflowpath))
                worktools = yaml.load(open("{}/temp_tool.yaml".format(workflowpath)))
                baseyaml = toolyamltodict(worktools, baseyaml, topic.title())
                os.system("rm {}/temp_tool.yaml".format(workflowpath))
        else:
            if os.path.isfile(toolpath):
                tuttools = yaml.load(open(toolpath))
                baseyaml = toolyamltodict(tuttools, baseyaml, topic.title())


yaml.dump(baseyaml, t, default_flow_style=False)

t.close()