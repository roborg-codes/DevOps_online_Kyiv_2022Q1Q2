#!/bin/env bash

set -e

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
printf "Most active time:\n%s\n\n" "$ACTIVE_TIME"

printf "Search bot access:\n%s\n\n" "$BOT_ACC"
#                                     ^ troubleshoot this
