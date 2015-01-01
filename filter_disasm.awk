/^[0-9abcdef]*\ <.*>:$/ {
    print $0
}

$1 ~ /^[0-9abcdef]*:$/ {
    printf "%s%s\n", $3, $2
}
