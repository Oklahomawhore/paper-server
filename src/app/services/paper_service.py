import requests
from lxml import etree
from ..models import Paper

BASE_URL = "http://export.arxiv.org/oai2"

def fetch_and_store_papers_from_oai(db):
    """
    Fetch records from arXiv using the OAI-PMH API and store them in the database.
    """
    records = list_records(from_date="2023-08-01")  # Example: Replace with actual dates or logic

    for record in records:
        if Paper.query.filter_by(arxiv_id=record['id']).first():
            continue

        paper = Paper(
            title=record['title'],
            authors=", ".join(record['authors']),
            summary=record['abstract'],
            published=record['published'],
            arxiv_id=record['id'],
            link=f"http://arxiv.org/abs/{record['id']}"
        )

        db.session.add(paper)

    db.session.commit()

def list_records(metadata_prefix="arXiv", set_spec=None, from_date=None, until_date=None):
    """
    List records from arXiv using the OAI-PMH API.
    """
    params = {
        "verb": "ListRecords",
        "metadataPrefix": metadata_prefix,
    }

    if set_spec:
        params["set"] = set_spec
    if from_date:
        params["from"] = from_date
    if until_date:
        params["until"] = until_date

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    return parse_records(response.content)

def parse_records(xml_content):
    ns = {"oai": "http://www.openarchives.org/OAI/2.0/"}
    root = etree.fromstring(xml_content)
    records = []

    for record in root.findall(".//oai:record", namespaces=ns):
        metadata = record.find(".//oai:metadata", namespaces=ns)
        if metadata is not None:
            arxiv_metadata = metadata.find(".//arXiv:arXiv", namespaces={"arXiv": "http://arxiv.org/OAI/arXiv/"})
            if arxiv_metadata is not None:
                record_data = {
                    "id": arxiv_metadata.find(".//arXiv:id", namespaces={"arXiv": "http://arxiv.org/OAI/arXiv/"}).text,
                    "title": arxiv_metadata.find(".//arXiv:title", namespaces={"arXiv": "http://arxiv.org/OAI/arXiv/"}).text,
                    "authors": [author.text for author in arxiv_metadata.findall(".//arXiv:author/arXiv:name", namespaces={"arXiv": "http://arxiv.org/OAI/arXiv/"})],
                    "abstract": arxiv_metadata.find(".//arXiv:abstract", namespaces={"arXiv": "http://arxiv.org/OAI/arXiv/"}).text,
                    "categories": arxiv_metadata.find(".//arXiv:categories", namespaces={"arXiv": "http://arxiv.org/OAI/arXiv/"}).text,
                    "comments": arxiv_metadata.find(".//arXiv:comments", namespaces={"arXiv": "http://arxiv.org/OAI/arXiv/"}).text if arxiv_metadata.find(".//arXiv:comments", namespaces={"arXiv": "http://arxiv.org/OAI/arXiv/"}) is not None else None,
                    "doi": arxiv_metadata.find(".//arXiv:doi", namespaces={"arXiv": "http://arxiv.org/OAI/arXiv/"}).text if arxiv_metadata.find(".//arXiv:doi", namespaces={"arXiv": "http://arxiv.org/OAI/arXiv/"}) is not None else None,
                    "journal_ref": arxiv_metadata.find(".//arXiv:journal-ref", namespaces={"arXiv": "http://arxiv.org/OAI/arXiv/"}).text if arxiv_metadata.find(".//arXiv:journal-ref", namespaces={"arXiv": "http://arxiv.org/OAI/arXiv/"}) is not None else None,
                    "report_no": arxiv_metadata.find(".//arXiv:report-no", namespaces={"arXiv": "http://arxiv.org/OAI/arXiv/"}).text if arxiv_metadata.find(".//arXiv:report-no", namespaces={"arXiv": "http://arxiv.org/OAI/arXiv/"}) is not None else None,
                    "submission_history": arxiv_metadata.find(".//arXiv:versions", namespaces={"arXiv": "http://arxiv.org/OAI/arXiv/"}).text,  # Customize as needed
                    "created": arxiv_metadata.find(".//arXiv:created", namespaces={"arXiv": "http://arxiv.org/OAI/arXiv/"}).text,
                    "updated": arxiv_metadata.find(".//arXiv:updated", namespaces={"arXiv": "http://arxiv.org/OAI/arXiv/"}).text if arxiv_metadata.find(".//arXiv:updated", namespaces={"arXiv": "http://arxiv.org/OAI/arXiv/"}) is not None else None,
                    "license": arxiv_metadata.find(".//arXiv:license", namespaces={"arXiv": "http://arxiv.org/OAI/arXiv/"}).text if arxiv_metadata.find(".//arXiv:license", namespaces={"arXiv": "http://arxiv.org/OAI/arXiv/"}) is not None else None,
                }
                records.append(record_data)

    return records
