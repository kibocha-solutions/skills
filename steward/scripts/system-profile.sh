#!/usr/bin/env bash
# Writes the machine capacity profile to ~/.agents/system-profile.md and prints a summary.
# Usage: system-profile.sh          write the profile and print the summary block
#        system-profile.sh --brief  print one summary line without writing the profile
# Records no hostname, user name, or home path. Works on Linux, macOS, and WSL.
set -uo pipefail
[ -t 0 ] || cat >/dev/null 2>&1 || true

OUT="$HOME/.agents/system-profile.md"
os="$(uname -s)"
gib() { awk -v k="$1" 'BEGIN { printf "%.1f", k / 1048576 }'; }

if [ "$os" = "Darwin" ]; then
  os_name="macOS $(sw_vers -productVersion 2>/dev/null)"
  cpu="$(sysctl -n machdep.cpu.brand_string 2>/dev/null)"
  threads="$(sysctl -n hw.logicalcpu 2>/dev/null)"
  mem_total_kb=$(( $(sysctl -n hw.memsize 2>/dev/null || echo 0) / 1024 ))
  page=$(sysctl -n hw.pagesize 2>/dev/null || echo 4096)
  free_pages=$(vm_stat 2>/dev/null | awk '/Pages (free|inactive|speculative)/ { gsub("\\.", "", $NF); s += $NF } END { print s + 0 }')
  mem_avail_kb=$(( free_pages * page / 1024 ))
  swap_line="$(sysctl -n vm.swapusage 2>/dev/null)"
  swap="${swap_line:-unknown}"
  temp="unavailable without a sensor tool"
  battery="$(pmset -g batt 2>/dev/null | awk -F'; ' 'NR==2 { print $1 "; " $2 }' | sed 's/.*\t//')"
  load="$(sysctl -n vm.loadavg 2>/dev/null | tr -d '{}' | awk '{ print $1, $2, $3 }')"
  gpu="$(system_profiler SPDisplaysDataType 2>/dev/null | awk -F': ' '/Chipset Model/ { print $2; exit }')"
else
  os_name="$(. /etc/os-release 2>/dev/null && echo "${PRETTY_NAME:-Linux}")"
  grep -qi microsoft /proc/version 2>/dev/null && os_name="$os_name (WSL)"
  cpu="$(awk -F': ' '/model name/ { print $2; exit }' /proc/cpuinfo)"
  threads="$(nproc 2>/dev/null)"
  mem_total_kb="$(awk '/^MemTotal/ { print $2 }' /proc/meminfo)"
  mem_avail_kb="$(awk '/^MemAvailable/ { print $2 }' /proc/meminfo)"
  swap="$(awk '/^SwapTotal/ { t = $2 } /^SwapFree/ { f = $2 } END { if (t > 0) printf "%.1f GiB total, %.0f%% used", t / 1048576, (t - f) * 100 / t; else print "none" }' /proc/meminfo)"
  temp="$(for z in /sys/class/thermal/thermal_zone*/temp; do [ -r "$z" ] && cat "$z"; done 2>/dev/null | awk '$1 > 0 { if ($1 > m) m = $1 } END { if (m) printf "%d °C highest sensor", m / 1000; else print "unavailable" }')"
  battery="$(for b in /sys/class/power_supply/BAT*; do [ -d "$b" ] && echo "$(cat "$b/capacity" 2>/dev/null)% $(cat "$b/status" 2>/dev/null)"; done | head -1)"
  load="$(awk '{ print $1, $2, $3 }' /proc/loadavg)"
  gpu="$(lspci 2>/dev/null | awk -F': ' '/VGA|3D|Display/ { print $2; exit }')"
fi

mem_line="$(gib "$mem_avail_kb") GiB available of $(gib "$mem_total_kb") GiB"
mem_pct=$(( mem_total_kb > 0 ? mem_avail_kb * 100 / mem_total_kb : 0 ))
disks="$(df -kP 2>/dev/null | awk 'NR > 1 && $1 !~ /^(tmpfs|devtmpfs|overlay|squashfs|efivarfs|none|map)/ && $6 !~ /^\/(snap|boot|run|sys|proc|dev|System\/Volumes\/(VM|Preboot|Update|xarts|iSCPreboot|Hardware))/ { printf "| %s | %.0f GiB | %.0f GiB | %s |\n", $6, $4 / 1048576, $2 / 1048576, $5 }' | sed "s#| $HOME#| ~#")"
root_free="$(df -kP / 2>/dev/null | awk 'NR == 2 { printf "%.0f GiB free on /", $4 / 1048576 }')"
engine_line="none"
command -v podman >/dev/null 2>&1 && engine_line="podman $(podman --version 2>/dev/null | awk '{ print $3 }')"
[ "$engine_line" = "none" ] && command -v docker >/dev/null 2>&1 && engine_line="docker $(docker --version 2>/dev/null | awk '{ print $3 }' | tr -d ,)"

summary="System: ${os_name}; ${threads} threads; memory ${mem_line} (${mem_pct}%); swap ${swap}; ${root_free}; temperature ${temp}; load ${load}; battery ${battery:-none}."

if [ "${1:-}" = "--brief" ]; then
  echo "$summary"
  exit 0
fi

mkdir -p "$(dirname "$OUT")"
{
  echo "# System profile"
  echo
  echo "Recorded: $(date '+%Y-%m-%d %H:%M %z')"
  echo
  echo "| Item | Value |"
  echo "| :--- | :--- |"
  echo "| Operating system | ${os_name} ($(uname -m)) |"
  echo "| Processor | ${cpu:-unknown}, ${threads} threads |"
  echo "| Graphics | ${gpu:-unknown} |"
  echo "| Memory | ${mem_line} |"
  echo "| Swap | ${swap} |"
  echo "| Temperature | ${temp} |"
  echo "| Load average | ${load} |"
  echo "| Battery | ${battery:-none} |"
  echo "| Container engine | ${engine_line} |"
  echo
  echo "| Mount | Free | Size | Used |"
  echo "| :--- | :--- | :--- | :--- |"
  echo "$disks"
} > "$OUT"

echo "$summary"
echo "Profile: ~/.agents/system-profile.md. Apply the steward capacity budgets before heavy work."
