#!/bin/bash
echo "🔍 Analyzing commits by Author"
git log --pretty=format:"%an" | sort | uniq -c | sort -rn

echo -e "\n"

echo "🔍 Analyzing contributions by authors..."
git log --format='%aN' | sort -u | while read name; do
  echo -n "$name: "
  git log --author="$name" --pretty=tformat: --numstat | \
  awk '{ add += $1; del += $2 } END { print "Added:", add, "Deleted:", del }'
done

echo -e "\n"

declare -A largest_added_file
declare -A largest_added_lines
declare -A largest_deleted_file
declare -A largest_deleted_lines

author=""

while IFS= read -r line; do
    if [[ "$line" == --* ]]; then
        author="${line:2}"
    elif [[ -n "$line" ]]; then
        added=$(echo "$line" | awk '{print $1}')
        deleted=$(echo "$line" | awk '{print $2}')
        file=$(echo "$line" | cut -f3-)

        # Skip if added or deleted is non-numeric
        if ! [[ "$added" =~ ^[0-9]+$ ]]; then added=0; fi
        if ! [[ "$deleted" =~ ^[0-9]+$ ]]; then deleted=0; fi

        # Track largest added file
        if (( added > ${largest_added_lines[$author]:-0} )); then
            largest_added_lines[$author]=$added
            largest_added_file[$author]=$file
        fi

        # Track largest deleted file
        if (( deleted > ${largest_deleted_lines[$author]:-0} )); then
            largest_deleted_lines[$author]=$deleted
            largest_deleted_file[$author]=$file
        fi
    fi
done < <(git log --pretty=format:"--%an" --numstat --diff-filter=ADM)

# Output result
echo -e "\n🔍 Largest Added and Deleted Files Per Author:"
for author in "${!largest_added_file[@]}"; do
    echo -e "\nAuthor: $author"
    echo "  ➕ Largest Added File:   ${largest_added_file[$author]} (${largest_added_lines[$author]} lines)"
    echo "  ➖ Largest Deleted File: ${largest_deleted_file[$author]} (${largest_deleted_lines[$author]} lines)"
done
