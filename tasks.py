import os
import re
import invoke


@invoke.task
def hello(c):
    invoke.run('echo "hello invoke!"')


@invoke.task
def new_exp(c):
    def get_version_num(dir_name: str):
        match = re.match(r'v(\d{2})\d{3}', dir_name)
        if match:
            return int(match.groups()[0])
        else:
            return 0

    top_dirs = os.listdir()
    versions = [get_version_num(d) for d in top_dirs]
    next_version = str(max(versions) + 1)
    new_exp_path = 'v' + next_version.zfill(2) + '000'

    try:
        os.mkdir(new_exp_path)
        os.mkdir(os.path.join(new_exp_path, 'notebook'))
        invoke.run(f'echo "Create {new_exp_path} Experiment Directory"')
    except FileExistsError as err:
        invoke.run(f'echo "{err}"')
