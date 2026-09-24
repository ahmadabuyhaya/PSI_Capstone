import requests


def get_uuid():
    response = requests.get("https://httpbin.org/uuid")
    data = response.json()
    return data["uuid"]


if __name__ == "__main__":
    print("Exercise 1 — UUID from httpbin:")
    print(get_uuid())
    print()

    import csv
    from collections import Counter

    exercise_connections_csv = """timestamp,src_ip,dst_port,protocol,bytes
2026-03-02T11:00:01,10.2.0.5,443,tcp,4000
2026-03-02T11:00:04,10.2.0.6,53,udp,120
2026-03-02T11:00:09,10.2.0.5,443,tcp,6500
2026-03-02T11:00:15,10.2.0.7,8080,tcp,300
2026-03-02T11:00:22,10.2.0.6,53,udp,90
2026-03-02T11:00:30,10.2.0.5,443,tcp,2200
"""

    with open("exercise_connections.csv", "w") as f:
        f.write(exercise_connections_csv)

    byte_totals = Counter()

    with open("exercise_connections.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            byte_totals[row["src_ip"]] += int(row["bytes"])

    top_ip, top_bytes = byte_totals.most_common(1)[0]

    print("Exercise 2 — Top talker by bytes:")
    print(f"{top_ip} -> {top_bytes} bytes")
    print("All totals:", dict(byte_totals))
    print()

    import hashlib
    import socket

    def quick_check(path, host, port):
        sha256 = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        file_hash = sha256.hexdigest()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            sock.connect((host, port))
            status = "open"
        except (socket.timeout, ConnectionRefusedError, OSError):
            status = "closed"
        finally:
            sock.close()

        return {"sha256": file_hash, "port_status": status}

    with open("sample_file.txt", "w") as f:
        f.write("This is a sample file used for hashing and port-check practice.\n")

    result = quick_check("sample_file.txt", "127.0.0.1", 22)

    print("Exercise 3 — quick_check result:")
    print(result)
