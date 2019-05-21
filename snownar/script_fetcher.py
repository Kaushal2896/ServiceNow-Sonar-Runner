from script_objs import Scripts
import os, re

class ScriptFetcher(object):

    file_ext = '.js'
    duplication_regex = r'.*?\((\d+)\)\.js'

    def __init__(self, project_name, git_repo_loc):
        self.scripts = Scripts().get_scripts()
        self.git_repo_loc = git_repo_loc
        self.update_dir = os.path.join(self.git_repo_loc, 'update')
        self.project_name = project_name

    def generate_script_files(self, target_dir_loc):
        if not os.path.exists(os.path.join(target_dir_loc, self.project_name)):
            os.mkdir(os.path.join(target_dir_loc, self.project_name))
            target_dir_loc = os.path.join(target_dir_loc, self.project_name)
        for each_table in self.scripts:
            script_files = self.get_script_files(**each_table)
            for each_script_file in script_files:
                xml_content = self.get_xml_content(each_script_file)
                script = self.get_code(xml_content, each_table['script_field'])
                self.save_as_file(script, self.get_file_name(xml_content, each_table['name_field']), target_dir_loc, each_table['table'])

    def get_file_name(self, xml_content, name_field):
        try:
            return re.compile(r'<{0}>(.*)<\/{0}>'.format(name_field)).search(xml_content).group(1)
        except(Exception):
            return ''

    def save_as_file(self, script, name_of_file, target_dir_loc, table):
        if not os.path.exists(os.path.join(target_dir_loc, table)):
            os.mkdir(os.path.join(target_dir_loc, table))

        new_file_path = os.path.join(target_dir_loc, table, name_of_file.replace('/', '-')) + self.file_ext

        if os.path.isfile(new_file_path):
            regex_match_res = re.search(self.duplication_regex, new_file_path)
            if regex_match_res:
                name_of_file = name_of_file.replace(self.duplication_regex, int(regex_match_res)+1)
            else:
                name_of_file = name_of_file.replace('.js', '(1).js')

        with open(os.path.join(new_file_path, 'w+') as target_file:
            target_file.write(script)  

    def get_script_files(self, table, script_field, name_field):
        script_files = []
        for filename in os.listdir(self.update_dir):
            if re.search(r'{0}_[0-9a-f]{{1}}'.format(table), filename):
                script_files.append(filename)
        return script_files 

    def get_xml_content(self, file):
        with open(os.path.join(self.update_dir, file)) as target_file:
            return target_file.read()

    def get_code(self, xml_content, script_field):
        try:
            return re.compile(r'<{0}><!\[CDATA\[([\s\S]*)\]\]><\/{0}>'.format(script_field)).search(xml_content).group(1)
        except(Exception):
            return ''