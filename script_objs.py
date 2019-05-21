class Scripts(object):
      
      def get_scripts(self):
          return [{
                'table': 'sys_script',
                'script_field': 'script',
                'name_field': 'name'
            },
            {
                'table': 'sys_script_include',
                'script_field': 'script',
                'name_field': 'name'
            },
            {
                'table': 'sysauto_script',
                'script_field': 'script',
                'name_field': 'name'
            },
            {
                'table': 'sys_ui_action',
                'script_field': 'script',
                'name_field': 'name'
            },
            {
                'table': 'ecc_agent_script_file',
                'script_field': 'script',
                'name_field': 'name'
            },
            {
                'table': 'sys_script_client',
                'script_field': 'script',
                'name_field': 'name'
            }]