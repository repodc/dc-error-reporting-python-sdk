import json
import http.client
import traceback

class DcErrorReportingSdk:
    _api_url = "https://dc-error-reporting.dctec.dev"
    _hostname = "dc-error-reporting.dctec.dev"

    def __init__(self, system_name, environment, token) -> None:
        self._system_name = system_name
        self._environment = environment
        self._token = token

    def send(self, error, url=None):
        try:
            path = "/api/error_report"

            error_traceback = traceback.format_exc()

            payload = json.dumps({
                "system_name": self._system_name,
                "environment": self._environment,
                "requested_url": url,
                "error": {
                    "message": str(error),
                    "stack": error_traceback
                }
            })

            connection = http.client.HTTPSConnection(self._hostname)

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._token}"
            }

            connection.request("POST", path, body=payload, headers=headers)

            response = connection.getresponse()

            if response.status != 200:
                print(f'Error sending notification. Status code: {response.status}')

        except Exception as e:
            print(f'Error sending notification: {str(e)}')

        finally:
            connection.close()