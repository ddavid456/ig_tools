# ig_tools
Set of cli tools to perform automated functions for research purposes using instagrams private api.

### Setup

Recommended creating a virtualenv `python -m venv env`
Windows
`env/Script/activate`
Others:
`source env/bin/activate`

`pip install -r requirements.txt`

[Install private api](https://github.com/ping/instagram_private_api) if unable from requirements.txt
`pip install git+https://git@github.com/ping/instagram_private_api.git@1.6.0`

Create a config.json file with credentials, this will be converted into a session file.
```json:
{
    "username": "ig_user",
    "password": "ig_password"
}
```

### Usage

Add Followers
`python ig_tools.py addFollowers <configpath> <amount_to_add> <user_to_target>`
`python ig_tools.py deleteFollowing <configpath> <amount_to_delete:default 100> <safelist:optional>`
`[not functional]python ig_tools.py cleanComments <configpath> <last_posts:default 1>`

### WIP

deleteComments is a work in progress to delete ig comments using regular expressions.
This is still not fully functional.

### Disclaimer
**Not responsible for your account being band, flagged as spam, or deleted.**
**Use at your own risk.**