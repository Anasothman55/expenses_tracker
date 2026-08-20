import asyncio
from rich import print
import httpx

api = "http://127.0.0.1:8001/api/v1"

bearer = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIwMWEwMTkxMy1jMjI2LTcwOTMtYTcwZS04Y2I0ZDdjMjQ1MTMiLCJzZXNzaW9uX2lkIjoiMDFhMDFkZWMtYWRhMC03MzljLWEzMmEtNmMwYWVhYTk0ZjhmIiwianRpIjoiMDFhMDFkZjgtMzljZi03NTVlLTljZGUtYzJjN2IyYzdlNTZjIiwidHlwZSI6ImFjY2VzcyIsImFpdCI6MTc4NzIwOTIwMiwiZXhwIjoxNzg3MjE2NDAyfQ.gzKByOQwcA7HrrprMkkKYbvcbE2s249WrPPcH86LEGQ"

headers = {
  "Authorization": f"Bearer {bearer}",
  "Content-Type": "application/json",
}

group_list: list = [
  {
    "name": "Housing",
    "rgb_color": "64748B",
    "icons": None
  },
  {
    "name": "Utilities",
    "rgb_color": "64748B",
    "icons": None
  },
  {
    "name": "Transportation",
    "rgb_color": "64748B",
    "icons": None
  },
  {
    "name": "Food",
    "rgb_color": "64748B",
    "icons": None
  },
  {
    "name": "Entertainment",
    "rgb_color": "64748B",
    "icons": None
  },
  {
    "name": "Health & Fitness",
    "rgb_color": "64748B",
    "icons": None
  },
  {
    "name": "Income",
    "rgb_color": "64748B",
    "icons": None
  },
  {
    "name": "Transfer",
    "rgb_color": "64748B",
    "icons": None
  },
  {
    "name": "Other",
    "rgb_color": "64748B",
    "icons": None
  }
]


# async def main():
#   async with httpx.AsyncClient() as client:
#     for group in group_list:
#       res = await client.post(
#         url=f"{api}/category-group/",
#         headers=headers,
#         json=group,
#       )
#
#       print(group["name"], res.status_code)
#       print(res.json())

async def main():
  print(bearer)

if __name__ == "__main__":
  asyncio.run(main())


