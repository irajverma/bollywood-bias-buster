import requests
import json

def test_bollywood_data_access():
    """Simple test to verify we can access the Bollywood dataset"""
    
    print("Testing Bollywood Dataset Access")
    print("=" * 40)
    
    # Test 1: Repository access
    print("1. Testing repository access...")
    try:
        repo_url = "https://api.github.com/repos/BollywoodData/Bollywood-Data"
        response = requests.get(repo_url)
        
        if response.status_code == 200:
            repo_info = response.json()
            print(f"   ✓ Repository found: {repo_info['full_name']}")
            print(f"   ✓ Stars: {repo_info['stargazers_count']}")
            print(f"   ✓ Last updated: {repo_info['updated_at']}")
        else:
            print(f"   ✗ Failed to access repository: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 2: Check root contents
    print("\n2. Checking repository contents...")
    try:
        contents_url = "https://api.github.com/repos/BollywoodData/Bollywood-Data/contents"
        response = requests.get(contents_url)
        
        if response.status_code == 200:
            contents = response.json()
            print(f"   ✓ Found {len(contents)} items in repository")
            
            folders = [item for item in contents if item['type'] == 'dir']
            files = [item for item in contents if item['type'] == 'file']
            
            print(f"   ✓ Folders: {len(folders)}")
            for folder in folders:
                print(f"     - {folder['name']}")
            
            print(f"   ✓ Files: {len(files)}")
            for file in files[:3]:  # Show first 3 files
                print(f"     - {file['name']}")
                
        else:
            print(f"   ✗ Failed to get contents: {response.status_code}")
            if response.status_code == 403:
                print("   ℹ This might be a rate limit issue. Try again in a few minutes.")
            return False
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 3: Check specific data folders
    print("\n3. Checking data folders...")
    data_folders = ['scripts-data', 'wikipedia-data', 'trailer-data', 'images-data']
    
    for folder in data_folders:
        try:
            folder_url = f"https://api.github.com/repos/BollywoodData/Bollywood-Data/contents/{folder}"
            response = requests.get(folder_url)
            
            if response.status_code == 200:
                folder_contents = response.json()
                print(f"   ✓ {folder}: {len(folder_contents)} files")
            else:
                print(f"   ✗ {folder}: Failed ({response.status_code})")
                
        except Exception as e:
            print(f"   ✗ {folder}: Error - {e}")
    
    # Test 4: Try to fetch a sample file
    print("\n4. Testing file content access...")
    try:
        # Try to get README file
        readme_url = "https://raw.githubusercontent.com/BollywoodData/Bollywood-Data/master/README.md"
        response = requests.get(readme_url)
        
        if response.status_code == 200:
            content = response.text
            print(f"   ✓ Successfully fetched README ({len(content)} characters)")
            print(f"   ✓ First 200 characters:")
            print(f"   {content[:200]}...")
        else:
            print(f"   ✗ Failed to fetch README: {response.status_code}")
            
    except Exception as e:
        print(f"   ✗ Error fetching file: {e}")
    
    print("\n" + "=" * 40)
    print("✅ Data access test completed!")
    print("\nIf you see errors above, try:")
    print("1. Check your internet connection")
    print("2. Wait a few minutes (GitHub API rate limits)")
    print("3. Try running the script again")
    
    return True

if __name__ == "__main__":
    test_bollywood_data_access()
