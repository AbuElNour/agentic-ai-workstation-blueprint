from pathlib import Path
import ipaddress
import re


root = Path(__file__).resolve().parents[1]
text = "\n".join(
    path.read_text(errors="ignore")
    for path in root.rglob("*")
    if path.is_file() and ".git" not in path.parts and path.suffix not in {".pyc"}
)
for address in re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text):
    ip = ipaddress.ip_address(address)
    if not any(ip in ipaddress.ip_network(block) for block in ("192.0.2.0/24", "198.51.100.0/24", "203.0.113.0/24")):
        if not ip.is_loopback:
            raise SystemExit(f"non-reserved address detected: {address}")
for hostname in re.findall(r"\b[a-z0-9.-]+\.(?:ai|com|net|org)\b", text, flags=re.I):
    if not hostname.endswith("example.com"):
        raise SystemExit(f"non-example hostname detected: {hostname}")
if re.search(r"(?:TOKEN|SECRET|KEY)[A-Z0-9_]*[ \t]*=[ \t]*[^ \t\r\n#]+", text):
    raise SystemExit("non-empty secret-like configuration detected")
print("blueprint contains only reserved addresses, example domains, and empty credential placeholders")
