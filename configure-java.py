from pathlib import Path
import os
import sys
import subprocess


# jdk_priority = int(major) * 10000 + int(minor) * 1000 + int(update) * 2
# jdk_alternatives_cmd = create_cmd(jdk_path, 'javac', jdk_priority, jre_path)
# jdk_alternatives_cmd += ' --slave /etc/profile.d/jdk_env.sh jdk_env.sh ' + java_root + '/jdk_env.sh'
# subprocess.Popen(jdk_alternatives_cmd.split())

# jre_priority = jdk_priority - 1
# jre_alternatives_cmd = create_cmd(jre_path, 'java', jre_priority)
# subprocess.Popen(jre_alternatives_cmd.split())

# def create_cmd(bin_path, master, priority, exclusion_path=None):
#     path = Path(bin_path)
#     cmd = ['update-alternatives --install ' +
#            dest_bin_path + '/' + master + ' ' + master + ' ' + bin_path + '/' + master + ' ' + str(priority)]
#     for file in path.iterdir():
#         *ignore, name = str(file).rpartition('/')
#         if (name != master) and \
#                 (exclusion_path is None or not os.path.isfile(exclusion_path + '/' + name)):
#             cmd.append('--slave ' +
#                        dest_bin_path + '/' + name + ' ' + name + ' ' + bin_path + '/' + name)
#
#             if os.path.isfile(man_path + '/' + name + '.1'):
#                 cmd.append('--slave ' +
#                            dest_man_path + '/' + name + '.1 ' + name + '.1 ' + man_path + '/' + name + '.1')
#
#     return ' '.join(cmd)


def install_alternatives(bin_path, priority, exclusion_path=None):
    path = Path(bin_path)
    for file in path.iterdir():
        *ignore, name = str(file).rpartition('/')
        if exclusion_path is None or not os.path.isfile(exclusion_path + '/' + name):
            cmd = 'update-alternatives --install ' \
                  + dest_bin_path + '/' + name + ' ' + name + ' ' + bin_path + '/' + name + ' ' \
                  + str(priority)

            if os.path.isfile(man_path + '/' + name + '.1'):
                cmd += ' --slave ' \
                       + dest_man_path + '/' + name + '.1 ' + name + '.1 ' + man_path + '/' + name + '.1'

                subprocess.Popen(cmd.split())


def remove_alternatives(bin_path):
    path = Path(bin_path)
    for file in path.iterdir():
        *ignore, name = str(file).rpartition('/')
        cmd = 'update-alternatives --remove ' + name + ' ' + bin_path + '/' + name

        subprocess.Popen(cmd.split())


java_root, major, minor, update = sys.argv[2:6]

jdk_path = java_root + '/bin'
if not os.path.isdir(jdk_path):
    print('\'bin\' directory not found.')
    exit(1)
if not os.path.isfile(jdk_path + '/javac'):
    print('\'bin/javac\' not found.')
    exit(1)

jre_path = java_root + '/jre/bin'
if not os.path.isdir(jre_path):
    print('\'jre/bin\' directory not found.')
    exit(1)
if not os.path.isfile(jre_path + '/java'):
    print('\'jre/bin/java\' not found.')
    exit(1)

man_path = java_root + '/man/man1'
if not os.path.isdir(man_path):
    print('\'man/man1\' directory not found.')
    exit(1)


dest_bin_path = '/usr/bin'
dest_man_path = '/usr/share/man/man1'


if sys.argv[1] == 'add':
    with open(java_root + '/java.sh', 'w') as env_file:
        env_file.write('export JAVA_HOME="' + java_root + '"\n')
        env_file.write('export JDK_HOME="' + java_root + '"\n')
        env_file.write('export JRE_HOME="' + java_root + '/jre"\n')

    alt_priority = int(major) * 10000 + int(minor) * 1000 + int(update) * 2
    install_alternatives(jre_path, alt_priority)
    install_alternatives(jdk_path, alt_priority, jre_path)

    cmd = 'update-alternatives --install ' \
          + '/usr/lib/mozilla/plugins/libjavaplugin.so mozilla-javaplugin.so ' + java_root + '/jre/lib/amd64/libnpjp2.so ' + str(alt_priority)
    subprocess.Popen(cmd.split())

    cmd = 'update-alternatives --install ' \
          + '/etc/profile.d/java.sh java.sh ' + java_root + '/java.sh ' + str(alt_priority)
    subprocess.Popen(cmd.split())

if sys.argv[1] == 'remove':
    remove_alternatives(jre_path)
    remove_alternatives(jdk_path)

    cmd = 'update-alternatives --remove java.sh ' + java_root + '/java.sh'
    subprocess.Popen(cmd.split())
