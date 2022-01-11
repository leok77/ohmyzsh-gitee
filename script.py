import hashlib
import datetime
import wget
import os.path


def hash_check(path: str) -> str:
    m = hashlib.md5()
    with open(path, 'rb') as src:
        while True:
            data = src.read(2048)
            if not data:
                break
            m.update(data)
    hash_sum = m.hexdigest()
    return hash_sum.upper()


def get_install_mirror(source_path: str, dest_path: str):
    with open(source_path, 'r', encoding='utf-8') as sh:
        source_data = ''.join(sh.readlines())
        default_settings = [
            "# Default settings",
            "ZSH=${ZSH:-~/.oh-my-zsh}",
            "REPO=${REPO:-ohmyzsh/ohmyzsh}",
            "REMOTE=${REMOTE:-https://github.com/${REPO}.git}",
            "BRANCH=${BRANCH:-master}"
        ]
        default = '\n'.join(default_settings)
        mirror_settings = [
            "# Mirror settings",
            "# https://gitee.com/mirrors/oh-my-zsh",
            "ZSH=${ZSH:-~/.oh-my-zsh}",
            "REPO=${REPO:-mirrors/oh-my-zsh}",
            "REMOTE=${REMOTE:-https://gitee.com/${REPO}.git}",
            "BRANCH=${BRANCH:-master}"
        ]
        mirror = '\n#'.join(default_settings) + '\n\n' + '\n'.join(mirror_settings)
        dest_data = source_data.replace(default, mirror)
        with open(dest_path, 'w', encoding='utf-8') as dest:
            dest.write(dest_data)


if __name__ == '__main__':
    install = 'install.sh'
    install_mirror = 'install.gitee.sh'
    install_new = 'install' + datetime.datetime.now().strftime('-%Y-%m-%d-%H-%M-%S') + '.sh'
    install_url = 'https://gitee.com/mirrors/oh-my-zsh/raw/master/tools/install.sh'
    wget.download(install_url, install_new)
    if os.path.exists(install) and hash_check(install) == hash_check(install_new):
        os.remove(install_new)
        print("install.sh is up to date, no need to check it")
    else:
        os.replace(install_new, install)
        print("install.sh has updated, please check it")
        get_install_mirror(install, install_mirror)
        print("install.gitee.sh has generated, please check it")
