from email.policy import default
import os
import json
import mimetypes
import functools
import click
from ig_session import GenerateSession
from ig_bot_functions import ClearFollowers, AddFollowers, CreateSafelist, deleteComments

@click.group()
def cli():
    pass

def CheckPath(f):
    """
    Decorator to check if the config file is a valid json/path.
    """
    @functools.wraps(f)
    def new_func(*args, **kwarg):
        try:
            if os.path.exists(kwarg['config']) and mimetypes.MimeTypes().guess_type(kwarg['config'])[0] == 'application/json':
                return f(*args, **kwarg)
        except:
            pass
        print('Config path could not be found')
        return
    return new_func


@cli.command(name="addFollowers")
@click.argument('config')
@click.argument('users', default=100, type=int)
@click.argument('target', default=None, type=str)
@CheckPath
def addUsers(config, users, target):
    """
    Randomly adds users, can randomly add one from people *target
    """
    AddFollowers(GenerateSession(config).Session, users, target)

@cli.command(name="createSafelist")
@click.argument('config')
@click.argument('path', default='safelist.json', type=str)
@CheckPath
def createSafelsit(config, path):
    """
    Creates a safelist from the current people one is following
    """
    CreateSafelist(GenerateSession(config).Session, path)

@cli.command(name="deleteFollowing")
@click.argument('config')
@click.argument('users', default=100, type=int)
@click.argument('safelist_path', default=None, type=str)
@CheckPath
def deleteUsers(config, users, safelist_path):
    """
    Deletes people one is following, except those in the safelist if provided.
    """
    safe_users = []
    if safelist_path:
        with open(safelist_path) as file:
            safe_users = json.load(file)['safeUsers']
    ClearFollowers(GenerateSession(config).Session, safe_users, users)

@cli.command(name="cleanComments")
@click.argument('config')
@click.argument('lastposts', default=1, type=int)
@CheckPath
def cleanComment(config, lastposts):
    print('This feature is not yet complete.')
    #deleteComments(GenerateSession(config).Session, [], lastposts)


if __name__ == "__main__":
    cli()