# Task 4.1

/etc/passwd and /etc/group files
--------------------------------

/etc/passwd and /etc/group contain information about users and groups respectfully.
They both contain data in a colon (and coma) separated values.

![](./images/passwd.png)

The format here is as follows

```
username:pasword?y/n:User ID:Group ID:User data(GECOS):homedir:shell binary
```

The system has several types of users, regular ones, system users, and root.
The root is just like the regular user, but obviously has the highest level of priviliges available.
The rest of them are pseudousers, or system users.
These are users that run certain programs that do not require elevated priviliges.
In other words, they essentilay run as daemons that perform miscellaneous tasks.
Some of them are standard, like a bunch of systemd-* users, rtkit, avahi for networking, as well as sound or pulseaudio, docker, etc.
These usually have UID of `< 1000` and `> 0`.

The group file has similar format, and looks like this:

![](./images/group.png)

```
groupname:password?:Group ID:users
```


UID ranges and definitions
--------------------------

UID is a number given to each user on the system to identify them.
UID ranges are ranges of those numbers that define priviliges and purpose of a specific account.
UID of 0 gives the user, whatever the name, full priviliges over the system.
UID above 0 and below 1000 are system users, that perform service of the OS and the programs that it runs.
UID above 1000 are regular users, that are usually confined to their home directory and don't need to do any heavy lifting, such as installing programs or accessing important system information.
Of course with exception of sudoers.

GID is the same idea as UID but applied to user groups identification.


Determining belonging of a user
-------------------------------

User may have a primary and secondary groups, both of which are valid groups.
One can either find all users of a specific group in /etc/group, in /etc/passwd (primary group), or via `id` command.

```shell
$ id ubuntu
```

Adding user
-----------

In order to add a user to the system, one can either use `adduser`, or a `useradd` command.

I to do so, I would use

```shell
# useradd -m newuser
```

All one needs to create a new user is root priviliges and a username.
The other parameters may be added if needed (`-r`, nologin shell, and no `-m` for system users; `-G` for additional groups, UID, GID, comments, password)

If using `adduser`, one may need to configure the defaults, or otherwise specify similar flags for a regular user.
Similarly, `--system` flag is required for adding system users.


Renaming user
-------------

First, one needs to log the user out.
Then, run `usermod -l newname oldname` and rename mail spool, home directory, and gecos.


skell_dir directory
-------------------

skell_dir is a directory located in `/etc/skel`.
Skel refers to "skeleton directory", where all the default files are located and are copied to the user's home directory after it's creation.
All files in this directory are owned by root.

Removing a user
---------------

To remove a user I would run

```shell
# userdel -r user
```

Lockingg a user account
-----------------------

To do so, I can expire it's password, which would lock it.


```shell
# chage -E0 user
```

or simply lock accessing with a password:

```
# usermod -L user
```

Removing user's password
------------------------

