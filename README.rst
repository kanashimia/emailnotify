emailnotify
===============================================================================
emailnotify is a program, that displays email message as a push potification,
upon its arrival, using imap idle.

run
-------------------------------------------------------------------------------
Then must first configure ``readme_renderer`` either by placing config
in the default folder, ``~/.config/emailnotify/config.ini`` on linux,
or provide path to your config file like this::

    python -m emailnotify -c PATH_TO_CONFIG

Default file structure looks like this (``folder`` field is optional)::

    [mail]
    host = imap.coolmail.com
    username = coolguy@coolmail.com
    folder = INBOX

On the first login you must pass ``-p`` flag to prompt for a password 
interactively::

    python -m emailnotify -p

emailnotify saves password in the credential store,
so you mush have it installed (mostly for systemd/LinuX users).

After that can just run it as::

    python -m emailnotify
