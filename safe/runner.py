__author__ = 'sumeet'

import cherrypy
import getopt
import sys
from safe_box import SafeBox
from cli import Cli

def usage(message=None):
    code = 0
    if message:
        print message
        code = 1

    print "usage: runner.py -s|--server -l|--location=<safe location> -m|--master=<master password>\n" \
          "       runner.py -c|--client -a|--app=<app name>\n" \
          "       runner.py -c|--client -a|--app=<app name> -u|--user=<username> -p|--password=<site password>\n" \
          "       runner.py -h|--help"
    sys.exit(code)


def check_arg(var, message):
    if var is None:
        usage(message)


def main(argv):
    opts = None
    try:
        opts, args = getopt.getopt(argv[1:],
                                   'hcsl:a:u:p:m:',
                                   ["help", "client", "server", "location=", "app=", "user=", "password=", "master="])
    except getopt.GetoptError as err:
        usage(err)

    client = None
    server = None
    location = None
    master = None
    app = None
    user = None
    password = None

    for option, argument in opts:
        if option in ('-s', '--server'):
            server = True
        elif option in ('-c', '--client'):
            client = True
        elif option in ('-l', '--location'):
            location = argument
        elif option in ('-m', '--master'):
            master = argument
        elif option in ('-a', '--app'):
            app = argument
        elif option in ('-u', '--user'):
            user = argument
        elif option in ('-p', '--password'):
            password = argument
        elif option == 'h':
            usage()
        else:
            assert False, "unhandled option"

    if server:
        check_arg(location, "location of safe required")
        check_arg(master, "master password of safe required")

        conf = {
            '/': {
                'tools.sessions.on': True
            }
        }

        cherrypy.quickstart(SafeBox(location, master), '/', conf)
    elif client:
        check_arg(app, "app is required")
        cli = Cli('http://localhost:8080')

        if user is None and password is None:
            cli.get(app)
        else:
            check_arg(user, "username of app required")
            check_arg(password, "password of app required")
            cli.save(app, user, password)


if __name__ == '__main__':
    main(sys.argv)
