import re


DEFAULT_FORMAT = (
    '{ip} -- [{date}] "{method} {path} {protocol}" {status} {size} {agent}'
)


def increment_count(storage, key):
    if key in storage:
        storage[key] += 1
    else:
        storage[key] = 1


def format_to_regex(format_string):
    placeholders = {
        "ip": r"(?P<ip>\S+)",
        "date": r"(?P<date>.*?)",
        "method": r"(?P<method>[A-Z]+)",
        "path": r"(?P<path>\S+)",
        "protocol": r'(?P<protocol>[^"]+)',
        "status": r"(?P<status>\d{3})",
        "size": r"(?P<size>\d+)",
        "agent": r"(?P<agent>.*)",
    }

    regex_parts = []
    i = 0

    while i < len(format_string):
        if format_string[i] == "{":
            j = format_string.find("}", i)
            if j == -1:
                raise ValueError("Ошибка в шаблоне: не закрыта фигурная скобка")

            field_name = format_string[i + 1:j]

            if field_name not in placeholders:
                raise ValueError(f"Неизвестное поле в шаблоне: {field_name}")

            regex_parts.append(placeholders[field_name])
            i = j + 1
        else:
            regex_parts.append(re.escape(format_string[i]))
            i += 1

    return re.compile("".join(regex_parts))


def parse_line(line, pattern):
    match = pattern.search(line)
    if not match:
        return None

    data = match.groupdict()

    if "size" in data and data["size"] is not None:
        data["size"] = int(data["size"])

    return data


def analyze_logs(lines, pattern):
    ip_count = {}
    status_count = {}
    path_count = {}
    total_size = 0
    total_requests = 0

    for line in lines:
        parsed = parse_line(line, pattern)
        if parsed is None:
            continue

        increment_count(ip_count, parsed["ip"])
        increment_count(status_count, parsed["status"])
        increment_count(path_count, parsed["path"])

        total_size += parsed["size"]
        total_requests += 1

    return {
        "ip_count": ip_count,
        "status_count": status_count,
        "path_count": path_count,
        "total_size": total_size,
        "total_requests": total_requests,
    }


def get_top_items(data, limit):
    return sorted(data.items(), key=lambda item: item[1], reverse=True)[:limit]


def print_top_ips(ip_count, total_requests):
    print("Топ-5 IP-адресов:")
    top_ips = get_top_items(ip_count, 5)

    for ip, count in top_ips:
        percent = (count / total_requests * 100) if total_requests else 0
        print(f"{ip} - {count} запросов ({percent:.1f}%)")


def print_status_codes(status_count, total_requests):
    print("\nСтатус-коды:")
    for status, count in sorted(status_count.items()):
        percent = (count / total_requests * 100) if total_requests else 0
        print(f"{status} - {count} запросов ({percent:.1f}%)")


def print_top_paths(path_count):
    print("\nСамые популярные пути:")
    top_paths = get_top_items(path_count, 3)

    for path, count in top_paths:
        print(f"{path} - {count} запросов")


def print_total_size(total_size):
    print(f"\nОбщий размер ответов: {total_size}")


def read_logs_from_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.readlines()


def main():
    filename = "logs.txt"

    print("Стандартный формат логов:")
    print(DEFAULT_FORMAT)
    print()

    user_format = input(
        "Введите шаблон формата логов или нажмите Enter для стандартного: "
    ).strip()

    if not user_format:
        user_format = DEFAULT_FORMAT

    pattern = format_to_regex(user_format)
    lines = read_logs_from_file(filename)
    result = analyze_logs(lines, pattern)

    print_top_ips(result["ip_count"], result["total_requests"])
    print_status_codes(result["status_count"], result["total_requests"])
    print_top_paths(result["path_count"])
    print_total_size(result["total_size"])


if __name__ == "__main__":
    main()