# dns-speedtest

Benchmarks public DNS resolvers and ranks them by failure rate, then median latency.

## Usage

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Edit `dns_servers`, `test_domains`, `rounds` and `timeout` at the top of `main.py` to customize the test.

## License

MIT
