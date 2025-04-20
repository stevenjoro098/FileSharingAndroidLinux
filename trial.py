import requests

def test_flask_server():
    url = "http://192.168.238.1:5000/share"  # ✅ Fixed double http
    file_path = "test.gif"  # Replace with your file path

    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f)}
            response = requests.post(url, files=files)  # ✅ POST request

        print(f"✅ Server responded with status: {response.status_code}")
        print("🔁 Response content:")
        print(response.text)

    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
    except requests.ConnectionError:
        print("❌ Failed to connect to Flask server. Is it running?")
    except Exception as e:
        print(f"⚠️ An error occurred: {e}")

if __name__ == "__main__":
    test_flask_server()
