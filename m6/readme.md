# Shell scripting

## Script A

[For this script](./scriptA.sh) I first check for arguments.
If none are passed, then we can just call a function that will print usage information, and simply exit.

```shell
[[ ($# -eq 0) ]] && {
    print_usage
    exit 1
}
```

Then, we consider the first argument (others are ignored) in a case statement

```shell
case "$1" in
    "--target")
        arg_target
        exit 0
        ;;
    "--all")
        arg_all
        exit 0
        ;;
    *)
        print_usage
        exit 1
        ;;
esac
```

In case of `--target` argument, we:
1. call `ss` utility on `-t` tcp sockets `-l` that we are listening to.
2. pipe into awk to get status, port number and connection address.

```shell
arg_target() {
    CONNS=$(ss -lt | awk '{print $1 " " $4 " -> " $5}' | sed '1d')
    printf "Open TCP ports:\n\n%s\n" "$CONNS"
    return 0
}
```

In case of `--all` argument, we:
1. look up subnet address, and a broadcast address via `ip` utility.
2. make an icmp request on boadcast address
3. consider arp table to see all the hosts that responded

```shell
arg_all() {
    IP_O=$(ip -o -4 addr show)
    SUBNET=$(echo "$IP_O" | awk '/scope global/ {print $4}')
    BRD_ADDR=$(echo "$IP_O" | awk '/scope global/ {print $6}')
    ping -c2 -b $BRD_ADDR &> /dev/null
    RES=$(arp -a | tr -d '()' | awk '{print "Symname: " $1 " -> " $2}')

    printf "Current subnet: %s\n%s\n" "$SUBNET" "$RES"
    return 0
}
```
This is not perfect solution, but I it does work.

## ScriptB

[For this script](./scriptB.sh) I had to first consult the apache documentation to find out the meaning of each value in logs.
After that it was a matter of combining fields picked out by `awk` and other shell utilities like `sort`, `uniq`, `head`, etc.

```shell
#!/bin/env bash

FNAME="./apache_logs.txt"

MOST_IP_REQ=$(awk '{print $1}' "$FNAME" | sort | uniq -c | sort -nr | head -1 | awk '{print $1 " requests from " $2}')
MOST_PAGE_REQ=$(awk '{print $7}' "$FNAME" | sort | uniq -c | sort -nr | head -1 | awk '{print $2 " requested " $1 " times"}')
CNT_IP_REQS=$(awk '{print $1}' "$FNAME" | sort | uniq -c | sort -nr | awk '{print $1 " times from " $2}')
ERR_PAGES=$(awk '{if ($9 != 200) {print "ERR " $9 " -> " $7}}' "$FNAME" | sed '/^ERR [125]/d' | uniq)
ACTIVE_TIME=$(awk '{print $4, $5}' "$FNAME" | tr -d '[]' | sed 's|\(.*\):.*|\1|' | sort | uniq -c | sort -nr | head -3 | awk '{print $1 " requests at " $2}')
BOT_ACC=$(awk '{print $1, " -> ", $12, $13, $14, $15}' "$FNAME")

printf "IP with most requests:\n%s\n\n" "$MOST_IP_REQ"
printf "Most requested resource:\n%s\n\n" "$MOST_PAGE_REQ"
printf "Request stats per IP:\n%s\n\n" "$CNT_IP_REQS"
printf "Non-existent pages encounteres:\n%s\n\n" "$ERR_PAGES"
printf "Search bot access:\n%s\n\n" "$BOT_ACC"
printf "Most active time:\n%s\n\n" "$ACTIVE_TIME"
```

## ScriptC

[For this script](./scriptC.sh) I did the same manipulation as with scriptA to communicate with user that this script is hungry for arguments.
If all arguments were in place, it was a matter of running `rsync` together with `--tokenize-changes`, which added a semi-readable log output.
Then I ran this output through some commands to convert and expand the symbols used by rsync to communicate types of changes.
And then logging that into a predefined log file.
Then, add something like this into the crontab:

```cron
* * * * * /home/user/scriptC.sh /home/user/sync_dir/ user@remote.server:/home/user/backup_dir/
```
