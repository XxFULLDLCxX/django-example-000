[ "$1" == "--all" ] && (
    echo "Your Project url: " & read url
    git init
    git add .
    git commit -m ""
    git branch -M main
    git remote add origin $url
    git push -u origin main
)

AR=($@)
list=( )

for i in $(seq 0 $#); do
    echo "${AR[$i]}"
    list+="$i"
done

echo $list

exit 0


a="$@"
strindex() {
  x="${1%%$2*}"
  [[ "$x" = "$1" ]] && echo -1 || echo "${#x}"
}

AR=('foo' 'bar' 'baz' 'bat')
args=($@)

echo ${!args[@]} list
echo ${args[10]}

echo ${#AR[@]}
echo ${AR[*]}
echo ${!args[*]}
echo ${!AR[@]}

exit 0


length=${#AR[@]}
for (( i = 0; i < length; i++ )); do
  echo "$i"
done

for i in ${AR[*]}; do
  echo $i
done

strindex "$a" "6"

echo $x

# [[ "$x" = "$a" ]] && echo -1 || echo "${#x}"

exit 0

for i in $(seq 1 $#); do
    echo ${@: $i:1} == ${@: $i+1}
    [ ${@: $i:1} == '-i' ] && echo ${@: $i+1}
    [ ${@: $i:1} == '-a' ] && echo ${@: $i+1}
    [ ${@: $i:1} == '-c' ] && echo ${@: $i+1}
    [ ${@: $i:1} == '-b' ] && echo ${@: $i+1}
    [ ${@: $i:1} == '-r' ] && echo ${@: $i+1}
    [ ${@: $i:1} == '-p' ] && echo ${@: $i+1}
done

exit 0

for i in {1..10}; do
    [ "${@: $i:1}" == '-i' ] && git init "${@: $i+1}"
    [ "${@: $i:1}" == '-a' ] && git add "${@: $i+1}"
    [ "${@: $i:1}" == '-c' ] && git commit -m "${@: $i+1}"
    [ "${@: $i:1}" == '-b' ] && git branch -M "${@: $i+1}"
    [ "${@: $i:1}" == '-r' ] && git remote add origin "${@: $i+1}"
    [ "${@: $i:1}" == '-p' ] && git push -u origin "${@: $i+1}"
done
