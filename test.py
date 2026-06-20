import requests

response = requests.post(
    "http://localhost:8000/consultation/start",
    json={"patient_id": "P001", "initial_complaint": "Toux et fièvre"}
)

print("Status code:", response.status_code)
print("Réponse:", response.json())