# Task 4.1

## Part 1

Logging as root.
----------------

In order to log in as root into a guest system, I can choose several ways to do so:

1. Simply use root credentials to log in to the system at startup.
2. Use root credentials via an ssh connection, if sshd is running on this machine.
3. Log in as regular user and use `$ sudo su` (or `doas`) command to elevate priviliges, only possible if the user is in `wheel` or `sudo` usergroups and sudoers group is allowed to do so.

![Logging in demo](./images/login_shell.png)

Use `passwd` utility.
---------------------

`passwd` utility can be used to change user's password or other users' passwords (as root).
Especially useful for administrators who may need to adjust password policy.
It also checks for basic password security.
For example, password `vagrant` would not be accepted if password is too similar, like `vagrant2`.
This kind of basic check would be [very nifty for some users](https://web.archive.org/web/20220422221426/https://twitter.com/kobzevvv/status/1420295444694028290).

`passwd` may modify the following system files:

1. `/etc/passwd` - basic information about users (including wether or not user has password set)
2. `/etc/shadow` - the passwords in question, encrypted
3. `/etc/pam.d/passwd` - `passwd` config for PAM. I believe this is not actually modified by the utility.

![Changing password for the currently logged in user.](./images/changing_password.png)

Determine registered users.
---------------------------

There are various utilities that can be used to determine registerd (and/or active) users.
For a basic list of all users, including system users, one can just inspect contents of `/etc/passwd`, where the first string before colon is the username.
Additionaly, the file contains information about their shells, uid(wether it's root/system/regular), password status.

For more information on what commands a user runs, one can use `$ w` command.

![Looking up users.](./images/user_lookup.png)

It displays username, `tty` (virtual display), origin host(if ssh'ing), login time, time used by processes attached to the tty and by the process in the adjacent filed(frankly, I have very little understanding of how this time is mearsured and what exactly it represents), and what command their shell is executing.
If GUI is being used, this will most likely be the graphical server (like `X11` or `Wayland`) with the graphical server then spawning all the other processes like on the screenshot.


Changing personal information.
------------------------------

Personal information could be useful for shared systems with multiple users.
One can use `chfn` utility to change personal data in the system.
Either by rinning a command with a flag.

Or by answering prompts.

![Changing personal info.](./images/chfn_finger.png)

Using help system.
------------------

Linux distributions offer a variety of "help" commands that can be used to inspect documentation for other programs present on the system, as well as some miscellaneous documentation (for example libstd C if documentation is present):

 - `man`
 - `help`
 - `info`
 - also `apropos`
 - as well as simply running `$ cmd --help | less`

`man` and `info` are more or less the same and provide documentation for most of the programs installed on the system.
`man` displays so called "man pages", generated or written by the creators of the program and denoted with *.1, *.2, etc. file extentions.

![Using man](./images/man_w.png)

To my knowledge, `info` sometimes offers a more extensive documentation (for example, it displays the same documentation as the official GNU website for GNU utils).

![Using info](./images/info_passwd.png)

`help` provides explanations for bash builtins (like `[]`, `if`, `case`, `disown`, etc.)

![Using help](./images/help_unit.png)

`apropos` is, in a way, a metasearch utility, that searches manpages for mentions of a keyword(technically a pattern) in the description. Has to be updated with `$ mandb`, which usualy run by installation hooks or cron.
Using it may be surprisingly fruitful, for example for navigating the `grep` strain diversity:

![Using apropos](./images/useful_apropos.png)

I am not entirely sure what the `two keys` means in the context of this task, but I would be glad to give examples, given I can get a clarification.
Will try to update this later.

The `less` and/or `more` commands.
----------------------------------

`Less` and `more` commands are more of a text readers, or so called pagers.
`less` is usually used by `man` utility to display text, but it can also be used to read `--help` output of programs that don't provide manpages.

`more` here is just another pager, that is more or less similar to `less`.

I took advantage of this, and made a little shell script that tries some of these methods for me:

```shell
function man() {
    command man "$@" && return 0

    command -v "$@" &>/dev/null && \
        "$@" --help 2>&1 | "$PAGER" && return

    {
        printf "Similar man pages:\n"
        printf "==================\n"
        command apropos "$@" 2>&1
    } | "$PAGER"
}
```

In order to inspect bash config files separately I ran:

```shell
$ less ~/.bashrc
$ less ~/.bash_profile
$ less ~/.bash_logout
... etc.
```

or all together:

```shell
$ less ~/.bash*
```

or even:

```shell
$ less ~/.bash{rc,_profile,_logout}
```

![Looking at bash rc using less](./images/less_bashrc.png)

Last logons.
------------

Displaying last logons is intuitive, with a simple `last` command.

![Running last](./images/last_cmd.png)

The command not only displays users and their login and out time, but also tty, host, and kernel.
The `lastb` is also a thing apparently, it displays bad login attempts. Which may be useful for security reasons in combination with `last`'s ability to display remote logins' hostname and IP address.

`finger` utility is also useful, as it's output is more human readable. It also displays only last logintime (and some additional personal info which is irrelevant for this task).

![Running last](./images/finger_cmd.png)

Listing contents of $HOME.
--------------------------

Looking at `pwd` is done via `ls` utility:

![Listing directories in $HOME](./images/listing_home.png)

Here I use `ls` together with `-l` `-A` and `-h` flags.
This outputs the contents of the home directory (which could be specified if I wasn't in it already), otherwise specified as `$HOME` variable or `~` shell expansion.
The format is as follows:

1. Size of files at the top
2. File permissions (x reqired for directories)
3. Number of files inside
4. Owner
5. Owner group
6. Size
7. Last modification date and time
8. Name

Additionaly `-A` flag lists hidden directories except `.` and `..`
`-l` lists all the additional info
`-h` displays sizes in human readable format instead of bytes.

## Part 2

The `tree` command
------------------

Tree outputs a tree of directory structure in a neat visual.
The command, through it's flags allows me to control the output.
For exampe, in order to get all the files that contain 'c' character I need to enter:

```shell
$ tree -P *[cC]*
```

or

```shell
$ tree --ignore-case -P *c*
```

And for listing subdirectories up to a specific (instead of all) level, I'd need to enter:

```shell
$ tree -L 2
```


Determining filetype
--------------------

General file type can be determined via `$ file` command with the filename passed as argument.
For example: a binary executable (and it's type), a tarball, other archives, directories, ascii files (csv too), xml files(office files too).


Navigating filesystem
----------------------

I am already familiar with absolute and relative paths, as well as using `cd` to navigate the filesystem.
Relative paths refer to paths not beginning with `/`, which refer to root directory.
Instead it signifies a path which uses current working directory as it's "root".
It can not only refer to files velow working directory, but also ones above through `..` special directory, as well as itself with `.`.
Absolute paths begin with `/` or root directory and give the full path from root to the file that is being refered to.

Shell expansion of `~` helps with creating short absolute paths.
But it may cause some problems because it expands to home directory of the current user running the command.

If i'd like to return to the home directory, i could either just type `cd` or `cd ~`, the result would be the same.


The `ls` command explanations
-----------------------------

For the ls `-l` and `-a` flags explanations please refer to the first part of this task.

The only thing to note here is that `-a` displays `.` and `..` directories, while `-A` displays the same output, but without these special directories.


Performing a sequence of operations 1
-------------------------------------

![Performing the task](./images/sequence_1.png)


Performing a sequence of operations 2
-------------------------------------

Here is the end result:

![Performing the task](./images/sequence_2.png)

As we can see on the screenshot, the changes made to the original file do not affect the hard link.
Since the hard link refers to the same inode, or a physical place rather than a filesystem, in storage as the original file, the data will still be accesible even if the original file is "deleted".

The soft link, on the other hand, only refers to the location of the original file.
Kind of like a pointer in C.
It could be a relative or an absolute path, nevertheless it will always refer to it.
Hence if the original file is in trouble, the link will break.
It will also break if the path of the file is changed or the link is moved (in case it points to a relative path), unless the original file is moved too.


Using the `locate` utility
--------------------------

Locate helps me find files in a local database.
With this utility installed I ran to find the necessary files:

![Using locate](./images/locate.png)


Mounted partitions
------------------

To determine which ones were mounted, I used `lsblk` command, which lists all block devices connected to the system.

![lsblk](./images/partitions.png)

Devices with non-empty MOUNTPOINT field are indeed mounted to their respective mountpoints.
Currently, there is only one vdi block device, but in case of another device, such as a flash drive being connected, I would see it as /dev/sdb, sdc, sde, etc.
The devices then contains the partitions in question (sdb1, sdb2, sdb3, sdc1, etc.).


Count the number of lines
--------------------------

Finding sequences in a file can be done through `grep` and counting the lines is done by `wc`:

```shell
$ grep "pattern" file.txt | wc -l
```

Since grep without additional flags outputs matched lines instead of words, this command should give accurate output.


Using the `find` command
------------------------

![Using find](./images/find_host.png)

And the result is available [here](./find_host_output.txt).


Listing objects containing sequence with grep
----------------------------------------------

This seems like a trick question, since those two utilities are used for different purposes.
`find` searches directories for files, and grep searches contents of a file.

Therefore, the correct thing to do would be to use:

```shell
# grep -r ss /etc
```

Task 12 skipped, hope to get back to it
---------------------------------------


Devices and their types
-----------------------

Block devices could be seen in task 8:

![Looking at partitions](./images/partitions.png)

Where type denotes a specific block device's type.
`lsblk` only lists block devices, meaning their main goal is simply transferring data in chunks (blocks) and usually refer to either disks or partitions.

Other devices can be seen in `/dev` directory, which contains not only block devices, but all of them (mice, cameras, tty, other virtual "devices") as files.

These can be seen with `$ ls -l /dev` command, where the character preceding permissions filed signifies what type of device is that.

![Looking at devices](./images/devices_ls.png)

- b for block
- c for character (which is like block, but work with less data, for example tty)
- p and s are pipes and sockets, which are helpful for interprocess communication.


File types
----------

File type can be seen via `file` command.
It can either give you general information of what kind of file it is, or a more detailed response.
For example, a binary, txt, and an archive are all regular files, but the command is inteligent enough to tell which one it is.
The other ones are devices(block, special), also sockets, pipes and directories.
