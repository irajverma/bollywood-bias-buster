import requests
import json
import pandas as pd
from typing import Dict, List, Any
import re
import time
import os

class BollywoodDataProcessor:
    """
    Python script to process the real Bollywood dataset for bias analysis
    """
    
    def __init__(self):
        self.github_api_base = "https://api.github.com/repos/BollywoodData/Bollywood-Data"
        self.raw_base = "https://raw.githubusercontent.com/BollywoodData/Bollywood-Data/master"
        self.session = requests.Session()
        
        # Add headers to avoid rate limiting
        self.session.headers.update({
            'User-Agent': 'Bollywood-Bias-Buster/1.0',
            'Accept': 'application/vnd.github.v3+json'
        })
        
    def test_repository_access(self) -> bool:
        """Test if we can access the repository"""
        try:
            print("Testing repository access...")
            response = self.session.get(f"{self.github_api_base}")
            
            if response.status_code == 200:
                repo_info = response.json()
                print(f"✓ Repository accessible: {repo_info['full_name']}")
                print(f"✓ Description: {repo_info.get('description', 'No description')}")
                print(f"✓ Last updated: {repo_info.get('updated_at', 'Unknown')}")
                return True
            else:
                print(f"✗ Repository access failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Error accessing repository: {e}")
            return False
    
    def fetch_dataset_structure(self) -> Dict[str, Any]:
        """Fetch the overall structure of the dataset"""
        try:
            print("Fetching dataset structure...")
            response = self.session.get(f"{self.github_api_base}/contents")
            
            if response.status_code != 200:
                print(f"Failed to fetch contents: {response.status_code}")
                print(f"Response: {response.text}")
                return {}
            
            data = response.json()
            print(f"Found {len(data)} items in repository root")
            
            structure = {}
            for item in data:
                print(f"- {item['name']} ({item['type']})")
                if item['type'] == 'dir':
                    structure[item['name']] = {
                        'path': item['path'],
                        'url': item['url']
                    }
            
            return structure
            
        except Exception as e:
            print(f"Error fetching dataset structure: {e}")
            return {}
    
    def fetch_folder_contents(self, folder_path: str) -> List[Dict[str, Any]]:
        """Fetch contents of a specific folder"""
        try:
            print(f"Fetching contents of {folder_path}...")
            response = self.session.get(f"{self.github_api_base}/contents/{folder_path}")
            
            if response.status_code != 200:
                print(f"Failed to fetch folder contents: {response.status_code}")
                if response.status_code == 403:
                    print("Rate limit exceeded. Waiting 60 seconds...")
                    time.sleep(60)
                    response = self.session.get(f"{self.github_api_base}/contents/{folder_path}")
                
                if response.status_code != 200:
                    print(f"Still failed: {response.text}")
                    return []
            
            contents = response.json()
            print(f"Found {len(contents)} files in {folder_path}")
            
            # Show first few files
            for i, item in enumerate(contents[:5]):
                print(f"  {i+1}. {item['name']} ({item.get('size', 0)} bytes)")
            
            if len(contents) > 5:
                print(f"  ... and {len(contents) - 5} more files")
            
            return contents
            
        except Exception as e:
            print(f"Error fetching folder contents for {folder_path}: {e}")
            return []
    
    def fetch_file_content(self, file_path: str, max_size: int = 100000) -> str:
        """Fetch content of a specific file with size limit"""
        try:
            print(f"Fetching content of {file_path}...")
            response = self.session.get(f"{self.raw_base}/{file_path}")
            
            if response.status_code != 200:
                print(f"Failed to fetch file: {response.status_code}")
                return ""
            
            content = response.text
            
            # Limit content size to avoid memory issues
            if len(content) > max_size:
                print(f"File too large ({len(content)} chars), truncating to {max_size}")
                content = content[:max_size]
            
            print(f"Successfully fetched {len(content)} characters")
            return content
            
        except Exception as e:
            print(f"Error fetching file content for {file_path}: {e}")
            return ""
    
    def process_sample_data(self) -> pd.DataFrame:
        """Process a small sample of data to test the pipeline"""
        print("\n=== PROCESSING SAMPLE DATA ===")
        
        # Try to get some sample files from each category
        processed_data = []
        
        # Check each data folder
        folders_to_check = ['scripts-data', 'wikipedia-data', 'trailer-data']
        
        for folder in folders_to_check:
            print(f"\n--- Processing {folder} ---")
            files = self.fetch_folder_contents(folder)
            
            if not files:
                print(f"No files found in {folder}")
                continue
            
            # Process first 2 files from each folder
            for file_info in files[:2]:
                if file_info['name'].endswith(('.txt', '.json', '.csv')):
                    print(f"\nProcessing: {file_info['name']}")
                    
                    content = self.fetch_file_content(file_info['path'])
                    if content:
                        analysis = self.analyze_content_for_bias(content, file_info['name'], folder)
                        if analysis:
                            processed_data.append(analysis)
                    
                    # Add delay to avoid rate limiting
                    time.sleep(1)
        
        if processed_data:
            print(f"\n✓ Successfully processed {len(processed_data)} files")
            return pd.DataFrame(processed_data)
        else:
            print("\n✗ No data was successfully processed")
            return pd.DataFrame()
    
    def analyze_content_for_bias(self, content: str, filename: str, data_type: str) -> Dict[str, Any]:
        """Analyze content for gender bias patterns"""
        
        print(f"Analyzing {filename} ({len(content)} characters)")
        
        # Extract basic information
        movie_title = self.extract_movie_title(filename)
        year = self.extract_year(filename, content)
        
        # Character analysis
        characters = self.extract_characters_simple(content)
        
        # Basic bias indicators
        bias_indicators = self.detect_bias_patterns(content)
        
        analysis = {
            'filename': filename,
            'data_type': data_type,
            'movie_title': movie_title,
            'year': year,
            'content_length': len(content),
            'total_characters_found': len(characters),
            'male_characters': len([c for c in characters if c.get('gender') == 'male']),
            'female_characters': len([c for c in characters if c.get('gender') == 'female']),
            'unknown_gender': len([c for c in characters if c.get('gender') == 'unknown']),
            'occupation_mentions': bias_indicators['occupation_mentions'],
            'relationship_mentions': bias_indicators['relationship_mentions'],
            'appearance_mentions': bias_indicators['appearance_mentions'],
            'agency_indicators': bias_indicators['agency_indicators'],
            'sample_characters': characters[:3]  # First 3 characters as sample
        }
        
        print(f"  Found {len(characters)} characters")
        print(f"  Bias indicators: {sum(bias_indicators.values())} total mentions")
        
        return analysis
    
    def extract_movie_title(self, filename: str) -> str:
        """Extract movie title from filename"""
        # Remove file extension and clean up
        title = filename.replace('.txt', '').replace('.json', '').replace('.csv', '')
        title = re.sub(r'[_-]', ' ', title)
        title = re.sub(r'\d{4}', '', title)  # Remove years
        return title.strip()
    
    def extract_year(self, filename: str, content: str) -> int:
        """Extract year from filename or content"""
        # Try filename first
        year_match = re.search(r'(19|20)\d{2}', filename)
        if year_match:
            return int(year_match.group())
        
        # Try content
        year_matches = re.findall(r'(19|20)\d{2}', content[:1000])  # Check first 1000 chars
        if year_matches:
            years = [int(y) for y in year_matches if 1970 <= int(y) <= 2017]
            if years:
                return min(years)  # Return earliest year found
        
        return None
    
    def extract_characters_simple(self, content: str) -> List[Dict[str, Any]]:
        """Simple character extraction"""
        characters = []
        
        # Look for character introduction patterns
        patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+is\s+(?:a|an)\s+([^.!?]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+works?\s+as\s+([^.!?]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),?\s+(?:the\s+)?(?:daughter|son)\s+of\s+([^,!?]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:who|that)\s+([^.!?]+)'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                name = match.group(1).strip()
                description = match.group(2).strip() if len(match.groups()) > 1 else ""
                
                # Skip if name is too common/generic
                if name.lower() in ['the', 'and', 'but', 'when', 'where', 'what', 'how']:
                    continue
                
                gender = self.detect_gender_simple(name, description, content)
                
                characters.append({
                    'name': name,
                    'description': description,
                    'gender': gender,
                    'context': match.group(0)
                })
        
        # Remove duplicates
        seen_names = set()
        unique_characters = []
        for char in characters:
            if char['name'] not in seen_names:
                seen_names.add(char['name'])
                unique_characters.append(char)
        
        return unique_characters[:10]  # Limit to first 10 unique characters
    
    def detect_gender_simple(self, name: str, description: str, full_content: str) -> str:
        """Simple gender detection"""
        text = (name + " " + description + " " + full_content[:2000]).lower()
        
        male_indicators = ['he ', 'his ', 'him ', 'son', 'brother', 'father', 'husband', 'boyfriend', 'man', 'boy']
        female_indicators = ['she ', 'her ', 'hers', 'daughter', 'sister', 'mother', 'wife', 'girlfriend', 'woman', 'girl']
        
        male_count = sum(text.count(indicator) for indicator in male_indicators)
        female_count = sum(text.count(indicator) for indicator in female_indicators)
        
        if male_count > female_count:
            return 'male'
        elif female_count > male_count:
            return 'female'
        else:
            return 'unknown'
    
    def detect_bias_patterns(self, content: str) -> Dict[str, int]:
        """Detect various bias patterns in content"""
        content_lower = content.lower()
        
        # Occupation-related terms
        occupation_words = ['job', 'work', 'career', 'profession', 'doctor', 'engineer', 'teacher', 'lawyer', 'business']
        occupation_mentions = sum(content_lower.count(word) for word in occupation_words)
        
        # Relationship-defining terms
        relationship_words = ['daughter of', 'son of', 'wife of', 'husband of', 'girlfriend', 'boyfriend']
        relationship_mentions = sum(content_lower.count(word) for word in relationship_words)
        
        # Appearance-focused terms
        appearance_words = ['beautiful', 'pretty', 'gorgeous', 'handsome', 'attractive', 'stunning', 'lovely']
        appearance_mentions = sum(content_lower.count(word) for word in appearance_words)
        
        # Agency indicators
        agency_words = ['decides', 'chooses', 'leads', 'creates', 'fights', 'wins', 'achieves']
        agency_indicators = sum(content_lower.count(word) for word in agency_words)
        
        return {
            'occupation_mentions': occupation_mentions,
            'relationship_mentions': relationship_mentions,
            'appearance_mentions': appearance_mentions,
            'agency_indicators': agency_indicators
        }
    
    def create_sample_report(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Create a sample bias report"""
        if df.empty:
            return {'error': 'No data to analyze'}
        
        report = {
            'summary': {
                'total_files_processed': len(df),
                'data_types': df['data_type'].value_counts().to_dict(),
                'year_range': f"{df['year'].min()}-{df['year'].max()}" if df['year'].notna().any() else "Unknown",
                'total_characters': df['total_characters_found'].sum(),
                'gender_distribution': {
                    'male': df['male_characters'].sum(),
                    'female': df['female_characters'].sum(),
                    'unknown': df['unknown_gender'].sum()
                }
            },
            'bias_indicators': {
                'occupation_focus': df['occupation_mentions'].sum(),
                'relationship_defining': df['relationship_mentions'].sum(),
                'appearance_focus': df['appearance_mentions'].sum(),
                'agency_indicators': df['agency_indicators'].sum()
            },
            'sample_findings': df[['movie_title', 'male_characters', 'female_characters', 'sample_characters']].head().to_dict('records')
        }
        
        return report

# Main execution with better error handling
if __name__ == "__main__":
    print("=== BOLLYWOOD BIAS BUSTER - DATA PROCESSOR ===\n")
    
    processor = BollywoodDataProcessor()
    
    # Step 1: Test repository access
    if not processor.test_repository_access():
        print("\n❌ Cannot access the repository. Possible issues:")
        print("1. Internet connection problems")
        print("2. GitHub API rate limits")
        print("3. Repository might be private or moved")
        print("4. GitHub API might be down")
        exit(1)
    
    # Step 2: Check dataset structure
    print("\n" + "="*50)
    structure = processor.fetch_dataset_structure()
    
    if not structure:
        print("❌ Could not fetch dataset structure")
        exit(1)
    
    print(f"✓ Found {len(structure)} data folders")
    
    # Step 3: Process sample data
    print("\n" + "="*50)
    analysis_df = processor.process_sample_data()
    
    if analysis_df.empty:
        print("\n❌ No data was processed successfully")
        print("\nTroubleshooting tips:")
        print("1. Check your internet connection")
        print("2. Try running the script again (GitHub API has rate limits)")
        print("3. The repository structure might have changed")
        exit(1)
    
    # Step 4: Generate report
    print("\n" + "="*50)
    print("GENERATING BIAS ANALYSIS REPORT")
    
    report = processor.create_sample_report(analysis_df)
    
    # Save results
    try:
        analysis_df.to_csv('bollywood_sample_analysis.csv', index=False)
        print("✓ Saved analysis data to: bollywood_sample_analysis.csv")
        
        with open('sample_bias_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        print("✓ Saved bias report to: sample_bias_report.json")
        
        # Display summary
        print("\n" + "="*50)
        print("ANALYSIS SUMMARY")
        print("="*50)
        print(f"Files processed: {len(analysis_df)}")
        print(f"Characters found: {analysis_df['total_characters_found'].sum()}")
        print(f"Male characters: {analysis_df['male_characters'].sum()}")
        print(f"Female characters: {analysis_df['female_characters'].sum()}")
        print(f"Gender ratio (M:F): {analysis_df['male_characters'].sum()}:{analysis_df['female_characters'].sum()}")
        
        print(f"\nBias Indicators:")
        print(f"- Occupation mentions: {analysis_df['occupation_mentions'].sum()}")
        print(f"- Relationship defining: {analysis_df['relationship_mentions'].sum()}")
        print(f"- Appearance focus: {analysis_df['appearance_mentions'].sum()}")
        print(f"- Agency indicators: {analysis_df['agency_indicators'].sum()}")
        
        print(f"\nSample movies analyzed:")
        for _, row in analysis_df.head().iterrows():
            print(f"- {row['movie_title']} ({row['year']}) - {row['total_characters_found']} characters")
        
        print("\n✅ Analysis complete!")
        
    except Exception as e:
        print(f"❌ Error saving results: {e}")
