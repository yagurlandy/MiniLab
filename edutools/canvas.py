import os
import requests


class CanvasLMS:
    def __init__(self):
        token = os.getenv("CANVAS_API_TOKEN")

        if not token:
            raise ValueError("CANVAS_API_TOKEN is missing. Add it to your .env file.")

        self.endpoint = "https://boisestatecanvas.instructure.com/api/v1"
        self.headers = {"Authorization": f"Bearer {token}"}

    def _get_paginated(self, url, params=None):
        results = []

        while url:
            response = requests.get(url, headers=self.headers, params=params)

            if not response.ok:
                raise RuntimeError(f"Canvas API error {response.status_code}: {response.text}")

            data = response.json()
            if isinstance(data, list):
                results.extend(data)
            else:
                results.append(data)

            link_header = response.headers.get("Link", "")
            next_url = None

            if link_header:
                links = link_header.split(",")
                for link in links:
                    if 'rel="next"' in link:
                        next_url = link[link.find("<") + 1:link.find(">")]
                        break

            url = next_url
            params = None

        return results

    def get_courses(self):
        url = f"{self.endpoint}/courses"
        params = {
            "enrollment_state": "active",
            "state[]": "available",
            "per_page": 100,
        }
        return self._get_paginated(url, params)

    def get_assignments(self, course_id):
        url = f"{self.endpoint}/courses/{course_id}/assignments"
        params = {
            "per_page": 100,
        }
        return self._get_paginated(url, params)