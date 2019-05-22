import os, argparse, shutil
from sonar_runner import SonarScanner
from script_fetcher import ScriptFetcher

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Sonar Qube report generator from ServiceNow git repository.')
    parser.add_argument('-s', help = 'Host IP where Sonar qube is configured', default = '10.0.1.58')
    parser.add_argument('-u', help = 'Username of provided Sonar Qube configured instance', default = 'sonar')
    parser.add_argument('-p', help = 'Password of provided Sonar Qube configured instance', default = 'sonar')
    parser.add_argument('-n', help = 'Name of project to be displayed on sonar Qube dashboard')
    parser.add_argument('-i', help = 'Unique project id for Sonar Qube')
    parser.add_argument('-g', help = 'Location of git repository to fetch code files from')
    parser.add_argument('-l', help = 'Location of code directory to be placed in Sonar instance', default = '/home/sonar/servicenow')

    arguments = parser.parse_args()

    project_name = arguments.n
    proj_id = arguments.i
    git_loc = 'C:\\Users\\Aspire5\\Desktop\\Sonar Uploader\\trustar-app-for-servicenow'
    target_dir_loc = '.'
    prop_loc = os.path.join(target_dir_loc, project_name)
    remote_loc = arguments.l

    x = ScriptFetcher(project_name, git_loc)
    x.generate_script_files(target_dir_loc)

    scanner = SonarScanner(arguments.s, arguments.u, arguments.p)
    scanner.generate_props(prop_loc, proj_id, project_name)
    scanner.upload_dir(remote_loc)

    shutil.rmtree(prop_loc)