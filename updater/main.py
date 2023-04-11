import urllib.request
from os import path

import certificates
import git
from sources import ApkRelease, fdroid_recommended_release


def update_if_needed(module: str, release: ApkRelease):
    module_dir = path.abspath(path.join(path.dirname(__file__), '..', module))
    with open(path.join(module_dir, '.version_code'), 'r+') as version_code_file:
        version_code = int(version_code_file.read())
        if version_code < release.version_code:
            print(f'updating {module} to {release.version_name}')
            apk_filename = path.join(module_dir, f'{module}.apk')

            old_sig = certificates.get_apk_certificate(apk_filename)

            print(f'downloading {release.download_url} ...')
            urllib.request.urlretrieve(release.download_url, apk_filename)

            new_sig = certificates.get_apk_certificate(apk_filename)
            if old_sig != new_sig:
                raise Exception(
                    f'Signature mismatch for {module} old sig: {old_sig} new sig: {new_sig}'
                )

            version_code_file.seek(0)
            version_code_file.write(str(release.version_code))
            version_code_file.truncate()
            version_code_file.close()

            print('commit and push...')
            git.add_commit_push(module_dir, f'Update {module} to {release.version_name}')

        elif version_code > release.version_code:
            print(
                f'{module} ahead of suggested version ({version_code} > {release.version_code})'
            )
        elif version_code == release.version_code:
            print(f'{module} up to date.')

fdroid_main_repo = 'https://www.f-droid.org/repo'

update_if_needed('LocalGsmNlpBackend', fdroid_recommended_release(fdroid_main_repo, 'org.fitchfamily.android.gsmlocation'))
update_if_needed('AuroraDroid', fdroid_recommended_release(fdroid_main_repo, 'com.aurora.adroid'))
update_if_needed('AuroraStore', fdroid_recommended_release(fdroid_main_repo, 'com.aurora.store'))
