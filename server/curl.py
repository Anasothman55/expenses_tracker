import asyncio
from rich import print
import httpx

from src.shared.utils.fastcrud_filter import FilterType

api = "http://127.0.0.1:8001/api/v1"

bearer = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIwMWEwMTVhMi05NTUyLTc0ZDEtOTVkYi1kYTBmOTZlOTdkN2YiLCJzZXNzaW9uX2lkIjoiMDFhMDIwNmQtMjgyZS03MDZjLWI1MjEtMzQ1MmQ4MTIzZTA1IiwianRpIjoiMDFhMDIwNmQtMjgyZS03MDZjLWI1MjEtMzQ1NDBiMjBlYjQ3IiwidHlwZSI6ImFjY2VzcyIsImFpdCI6MTc4NzI1MDQxOSwiZXhwIjoxNzg3MjU3NjE5fQ.xlH5uKcQ1UwS-qWERvXf-_Hc4c9qtmo9OxLV8SnNUng"

headers = {
  "Authorization": f"Bearer {bearer}",
  "Content-Type": "application/json",
}

group_list: list = [
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
  print(True)

if __name__ == "__main__":
  asyncio.run(main())


