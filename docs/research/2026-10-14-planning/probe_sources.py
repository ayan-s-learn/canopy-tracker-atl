"""Bounded public metadata checks for the initial plan; not an acquisition pipeline.

Run from any directory with Python 3 (stdlib only). Writes only a new output path.
No authentication, signing, raster download, scraping, or automatic retries.
"""
import argparse
import datetime as dt
import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://planetarycomputer.microsoft.com/api/stac/v1"
# Screening rectangle inherited from the archive, NOT an authoritative city boundary.
BBOX = "-84.552,33.647,-84.289,33.887"
LIMIT = 100
MAX_BYTES = 4 * 1024 * 1024


def probe(name, url):
    record = {"name": name, "url": url, "checked_at_utc": dt.datetime.now(dt.timezone.utc).isoformat()}
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "CanopyTrackerATL-planning/0.1", "Accept": "application/json,text/html"})
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read(MAX_BYTES + 1)
            record.update(status=response.status, final_url=response.url, content_type=response.headers.get("Content-Type"))
        record.update(bytes_read=len(body), sha256=hashlib.sha256(body).hexdigest(), truncated=len(body) > MAX_BYTES)
        if len(body) > MAX_BYTES:
            return record
        try:
            payload = json.loads(body)
        except (ValueError, UnicodeDecodeError):
            # Page availability alone is not proof of record access. Do not retain
            # HTML: public permit pages may contain unnecessary personal data.
            record["result"] = "non-JSON response; no data coverage established"
            return record
        if "features" in payload:
            record["returned_items"] = len(payload["features"])
            record["has_next_page"] = any(link.get("rel") == "next" for link in payload.get("links", []))
            record["items"] = [{"id": f.get("id"), "bbox": f.get("bbox"), "properties": f.get("properties"),
                                 "assets": {k: {p: a[p] for p in ("href", "type", "roles") if p in a}
                                            for k, a in f.get("assets", {}).items()}} for f in payload["features"]]
        else:
            record["metadata"] = payload
    except urllib.error.HTTPError as error:
        record.update(status=error.code, error=str(error))
    except (urllib.error.URLError, TimeoutError) as error:
        record["error"] = str(error)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="New JSON file; existing files are never overwritten")
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output already exists; choose a new dated filename")
    queries = [("pc_naip_collection", BASE + "/collections/naip")]
    for year in (2019, 2021, 2023, 2025):
        params = urllib.parse.urlencode({"collections": "naip", "bbox": BBOX, "datetime": f"{year}-01-01T00:00:00Z/{year}-12-31T23:59:59Z", "limit": LIMIT})
        queries.append((f"pc_atl_bbox_{year}", BASE + "/search?" + params))
    queries.extend([
        ("usda_direct_download_landing", "https://datagateway.nrcs.usda.gov/GDGHome_DirectDownLoad.aspx"),
        ("atlanta_accela_landing", "https://aca-prod.accela.com/ATLANTA_GA/Default.aspx"),
        ("arc_building_permit_metadata", "https://opendata.atlantaregional.com/api/v3/datasets/655f985f43cc40b4bf2ab7bc73d2169b_0"),
    ])
    results = [probe(name, url) for name, url in queries]
    args.output.write_text(json.dumps({"purpose": "bounded planning metadata screen", "bbox_is_not_city_boundary": True,
                                      "max_response_bytes": MAX_BYTES, "results": results}, indent=2) + "\n")
    for result in results:
        print(json.dumps({k: result[k] for k in ("name", "status", "bytes_read", "returned_items", "has_next_page", "error", "result") if k in result}))


if __name__ == "__main__":
    main()
