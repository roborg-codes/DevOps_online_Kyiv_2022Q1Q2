#!/bin/env bash

set -e

PROGNAME="${0#./}"
DESC=$(cat <<EOF
    --all    display the IP addresses and symbolic names of all hosts in the current subnet.
    --target display a list of open system TCP ports.
EOF
)


print_usage() {
    printf "Name: %s\nUsage:\n%s\n" "$PROGNAME" "$DESC"
    return 0
}

arg_all() {
    IP_O=$(ip -o -4 addr show)
    SUBNET=$(echo "$IP_O" | awk '/scope global/ {print $4}')
    BRD_ADDR=$(echo "$IP_O" | awk '/scope global/ {print $6}')
    ping -c2 -b $BRD_ADDR &> /dev/null
    RES=$(arp -a | tr -d '()' | awk '{print "Symname: " $1 " -> " $2}')

    printf "Current subnet: %s\n%s\n" "$SUBNET" "$RES"
    return 0
}

arg_target() {
    CONNS=$(ss -lt | awk '{print $1 " " $4 " -> " $5}' | sed '1d')
    printf "Open TCP ports:\n\n%s\n" "$CONNS"
    return 0
}


[[ ($# -eq 0) ]] && {
    print_usage
    exit 1
}

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
