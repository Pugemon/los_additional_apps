import subprocess


user_name = 'Updater Robot'
user_email = 'robot@nowhere.invalid'


def add_commit_push(directory: str, message: str):
    diff = subprocess.run(['git', 'diff', '--cached', '--exit-code'], capture_output=True, text=True)
    if diff.returncode != 0:
        status = subprocess.run(['git', 'status'], capture_output=True, text=True)
        raise Exception(f'Unknown staged changes found: {status.stdout}')

    subprocess.run(['git', 'add', '--all', directory], check=True)
    subprocess.run(
        [
            'git',
            '-c',
            f'user.name={user_name}',
            '-c',
            f'user.email={user_email}',
            'commit',
            '--message',
            message,
        ]
    )
    subprocess.run(['git', 'push'])
