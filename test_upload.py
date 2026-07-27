"""
Test script to verify the /documents/upload endpoint works with different auth methods.

This script tests 3 authentication methods:
1. Authorization: Bearer <token> header
2. 'token' form field (for file uploads via FormData)
3. 'token' query parameter
"""

import requests
import json
import sys
import uuid

BASE_URL = "http://127.0.0.1:8000"

# Use unique identifiers to avoid conflicts
UNIQUE_ID = str(uuid.uuid4())[:8]
TEST_EMAIL = f"testuser_{UNIQUE_ID}@example.com"
TEST_MOBILE = f"9999{UNIQUE_ID}"[:10]
TEST_PASSWORD = "testpassword123"


def test_register():
    """Register a test user."""
    url = f"{BASE_URL}/auth/register"
    payload = {
        "fullname": "Test User",
        "email": TEST_EMAIL,
        "mobile": TEST_MOBILE,
        "password": TEST_PASSWORD,
        "role": "USER"
    }
    print("\n" + "="*60)
    print("Testing: POST /auth/register")
    print("="*60)
    try:
        resp = requests.post(url, json=payload)
        print(f"Status: {resp.status_code}")
        try:
            print(f"Response: {resp.json()}")
        except Exception:
            print(f"Response (raw): {resp.text[:200]}")
        if resp.status_code == 200:
            print("✅ Registration successful!")
        else:
            print("⚠️  May already exist, continuing...")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return True


def test_login():
    """Login and get JWT token."""
    url = f"{BASE_URL}/auth/login"
    payload = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    print("\n" + "="*60)
    print("Testing: POST /auth/login")
    print("="*60)
    try:
        resp = requests.post(url, json=payload)
        print(f"Status: {resp.status_code}")
        try:
            data = resp.json()
            print(f"Response: {data}")
            if resp.status_code == 200:
                token = data.get("access_token")
                print(f"Token: {token[:50]}...")
                print("✅ Login successful!")
                return token
            else:
                print(f"❌ Login failed: {data}")
                return None
        except Exception as e:
            print(f"❌ Failed to parse response: {e}")
            print(f"Raw response: {resp.text[:200]}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_upload_with_auth_header(token):
    """Method 1: Upload using Authorization: Bearer <token> header."""
    url = f"{BASE_URL}/documents/upload"
    
    files = {
        "file": ("test.txt", b"This is a test file content", "text/plain")
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print(f"\n  ┌─ Method 1: Authorization Header")
    print(f"  ├─ Header: Authorization: Bearer <token>")
    print(f"  └─ Sending...")
    
    try:
        resp = requests.post(url, files=files, headers=headers)
        print(f"     Status: {resp.status_code}")
        try:
            resp_data = resp.json()
        except Exception:
            resp_data = resp.text[:200]
        print(f"     Response: {resp_data}")
        if resp.status_code == 200:
            print("     ✅ SUCCESS!")
            return True
        else:
            print(f"     ❌ FAILED")
            return False
    except Exception as e:
        print(f"     ❌ Error: {e}")
        return False


def test_upload_with_form_token(token):
    """Method 2: Upload using 'token' form field."""
    url = f"{BASE_URL}/documents/upload"
    
    files = {
        "file": ("test_form.txt", b"This is form field token test", "text/plain")
    }
    data = {
        "token": token
    }
    
    print(f"\n  ┌─ Method 2: Form Field Token")
    print(f"  ├─ Form field: token=<token>")
    print(f"  └─ Sending...")
    
    try:
        resp = requests.post(url, files=files, data=data)
        print(f"     Status: {resp.status_code}")
        try:
            resp_data = resp.json()
        except Exception:
            resp_data = resp.text[:200]
        print(f"     Response: {resp_data}")
        if resp.status_code == 200:
            print("     ✅ SUCCESS!")
            return True
        else:
            print(f"     ❌ FAILED")
            return False
    except Exception as e:
        print(f"     ❌ Error: {e}")
        return False


def test_upload_with_query_token(token):
    """Method 3: Upload using 'token' query parameter."""
    url = f"{BASE_URL}/documents/upload?token={token}"
    
    files = {
        "file": ("test_query.txt", b"This is query param token test", "text/plain")
    }
    
    print(f"\n  ┌─ Method 3: Query Parameter Token")
    print(f"  ├─ Query param: ?token=<token>")
    print(f"  └─ Sending...")
    
    try:
        resp = requests.post(url, files=files)
        print(f"     Status: {resp.status_code}")
        try:
            resp_data = resp.json()
        except Exception:
            resp_data = resp.text[:200]
        print(f"     Response: {resp_data}")
        if resp.status_code == 200:
            print("     ✅ SUCCESS!")
            return True
        else:
            print(f"     ❌ FAILED")
            return False
    except Exception as e:
        print(f"     ❌ Error: {e}")
        return False


def test_upload_no_auth():
    """Test that upload fails without any authentication."""
    url = f"{BASE_URL}/documents/upload"
    
    files = {
        "file": ("test_unauth.txt", b"This should fail", "text/plain")
    }
    
    print(f"\n  ┌─ Negative Test: No Authentication")
    print(f"  ├─ No token provided at all")
    print(f"  └─ Sending...")
    
    try:
        resp = requests.post(url, files=files)
        print(f"     Status: {resp.status_code}")
        try:
            resp_data = resp.json()
        except Exception:
            resp_data = resp.text[:200]
        print(f"     Response: {resp_data}")
        if resp.status_code == 401:
            print("     ✅ CORRECTLY REJECTED (401 Unauthorized)")
            return True
        else:
            print(f"     ⚠️  Unexpected status")
            return False
    except Exception as e:
        print(f"     ❌ Error: {e}")
        return False


def main():
    print("\n" + "█"*60)
    print("  POLICY ASSISTANT AI - UPLOAD AUTH TEST")
    print("█"*60)
    print(f"  Server: {BASE_URL}")
    print(f"  Test Email: {TEST_EMAIL}")
    print(f"  Make sure the server is running! (python -m uvicorn app.main:app --reload)")
    
    # Step 1: Register
    if not test_register():
        print("\n❌ Registration failed. Aborting.")
        return
    
    # Step 2: Login
    token = test_login()
    if not token:
        print("\n❌ Login failed. Aborting.")
        return
    
    print("\n" + "="*60)
    print("  TESTING UPLOAD ENDPOINT AUTHENTICATION METHODS")
    print("="*60)
    
    results = []
    
    print("\n" + "─"*60)
    print("  Positive Tests (should succeed)")
    print("─"*60)
    
    s1 = test_upload_with_auth_header(token)
    results.append(("Method 1: Authorization Header", s1))
    
    s2 = test_upload_with_form_token(token)
    results.append(("Method 2: Form Field 'token'", s2))
    
    s3 = test_upload_with_query_token(token)
    results.append(("Method 3: Query Parameter 'token'", s3))
    
    print("\n" + "─"*60)
    print("  Negative Test (should fail with 401)")
    print("─"*60)
    
    s4 = test_upload_no_auth()
    results.append(("Negative: No Auth (expect 401)", s4))
    
    # Summary
    print("\n" + "="*60)
    print("  SUMMARY")
    print("="*60)
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        if not passed:
            all_passed = False
        print(f"  {status} - {name}")
    
    if all_passed:
        print("\n  🎉 ALL TESTS PASSED!")
        print("\n  The 401 authentication error should now be resolved.")
        print("\n  Your frontend can now pass the token via:")
        print("   1. Authorization: Bearer <token> header (recommended)")
        print("   2. 'token' form field in multipart/form-data")
        print("   3. 'token' query parameter")
    else:
        print("\n  ❌ Some tests failed. Check the output above.")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()

