import dns.resolver
import time
import statistics

dns_servers = {
    "Cloudflare": "1.1.1.1",
    "Google": "8.8.8.8",
    "Quad9": "9.9.9.9",
    "OpenDNS": "208.67.222.222",
    "Radar": "10.202.10.10",
    "Electro": "78.157.42.100",
    "NTT": "129.250.35.251",
    "Begzaar": "185.55.226.26",
    "UltraDNS": "64.6.64.6",
    "UltraDNS2": "156.154.70.2",
    "Hurricane Electric": "74.82.42.42",
    "DNSForge1": "49.12.222.213",
    "DNSForge2": "88.198.122.154",
    "Quad9_2": "149.112.112.112",
    "munchen":"5.1.66.255",
    "shelter":"87.107.206.15"
}

test_domains = ["google.com", "github.com", "wikipedia.org", "cloudflare.com", "speedtest.net", "digikala.com"]
rounds = 3
timeout = 2  # seconds per query


def query_ms(resolver, domain):
    start = time.perf_counter()
    try:
        resolver.resolve(domain)
        return (time.perf_counter() - start) * 1000
    except Exception:
        return None


def test_server(ip):
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = [ip]
    resolver.lifetime = timeout
    times = [query_ms(resolver, d) for _ in range(rounds) for d in test_domains]
    ok = [t for t in times if t is not None]
    return ok, len(times)


results = []
for name, ip in dns_servers.items():
    ok, total = test_server(ip)
    fail_rate = 1 - len(ok) / total
    median = statistics.median(ok) if ok else None
    results.append((name, ip, median, fail_rate))
    shown = f"{median:.1f} ms" if median is not None else "FAILED"
    print(f"{name:<20} {ip:<16} {shown:>10}  fail {fail_rate:.0%}")

# Rank: fewest failures first, then lowest median latency.
ranked = sorted((r for r in results if r[2] is not None), key=lambda r: (r[3], r[2]))

print(f"\nRanking (median of {rounds} x {len(test_domains)} queries):")
for i, (name, ip, median, fail_rate) in enumerate(ranked, 1):
    print(f"{i:>2}. {name:<20} {ip:<16} {median:>7.1f} ms  fail {fail_rate:.0%}")
for name, ip, median, _ in results:
    if median is None:
        print(f" -  {name:<20} {ip:<16} unreachable")
if ranked:
    print(f"\nBest: {ranked[0][0]} ({ranked[0][1]})")
