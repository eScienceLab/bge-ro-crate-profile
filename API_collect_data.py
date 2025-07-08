import requests

# Define the accession
accession = "SAMEA114402095"
url = f"https://www.ebi.ac.uk/biosamples/samples/{accession}"

# Request JSON data
headers = {"Accept": "application/hal+json"}
response = requests.get(url, headers=headers)
response.raise_for_status()  # raises error if not 200 OK

data = response.json()

# Print some key fields
print(f"Name: {data.get('name')}")
print(f"Accession: {data.get('accession')}")
print(f"Status: {data.get('status')}")
print(f"Release date: {data.get('release')}")
print(f"Updated date: {data.get('update')}")

# Characteristics is a dict of lists
print("Characteristics:")
for key, vals in data.get("characteristics", {}).items():
    texts = [v.get("text") for v in vals]
    print(f"  {key}: {', '.join(texts)}")

# Optional: print all _links
print("\nLinks:")
for rel, info in data.get("_links", {}).items():
    href = info.get("href")
    print(f"  {rel}: {href}")
