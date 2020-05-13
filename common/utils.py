from urllib.parse import urlencode, urlparse, parse_qs


def merge_url_with_new_query_string(url: str, new_params: dict) -> str:
    url_components = urlparse(url)
    original_params = parse_qs(url_components.query)

    merged_params = {**original_params, **new_params}
    update_query = urlencode(merged_params, doseq=True)

    return url_components._replace(query=update_query).geturl()
