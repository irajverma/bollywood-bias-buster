import os
import json
import pandas as pd
import numpy as np
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BollywoodDatasetPreprocessor:
    """
    Comprehensive preprocessor for the entire Bollywood dataset
    """
    
    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)
        self.processed_data = []
        self.metadata = {}
        
        # Ensure output directories exist
        self.output_dir = Path("processed_data")
        self.output_dir.mkdir(exist_ok=True)
        
        # File type mappings
        self.file_extensions = {
            'scripts': ['.txt', '.json', '.csv'],
            'wikipedia': ['.txt', '.json', '.csv'],
            'trailers': ['.txt', '.json', '.csv'],
            'images': ['.jpg', '.jpeg', '.png', '.gif']
        }
        
    def scan_dataset_structure(self) -> Dict[str, Any]:
        """Scan and catalog the entire dataset structure"""
        logger.info("Scanning dataset structure...")
        
        structure = {
            'scripts-data': [],
            'wikipedia-data': [],
            'trailer-data': [],
            'images-data': []
        }
        
        for folder_name in structure.keys():
            folder_path = self.dataset_path / folder_name
            if folder_path.exists():
                files = []
                for file_path in folder_path.rglob('*'):
                    if file_path.is_file():
                        files.append({
                            'name': file_path.name,
                            'path': str(file_path),
                            'size': file_path.stat().st_size,
                            'extension': file_path.suffix.lower(),
                            'modified': datetime.fromtimestamp(file_path.stat().st_mtime)
                        })
                structure[folder_name] = files
                logger.info(f"Found {len(files)} files in {folder_name}")
            else:
                logger.warning(f"Folder {folder_name} not found in dataset")
        
        # Save structure metadata
        with open(self.output_dir / 'dataset_structure.json', 'w') as f:
            json.dump(structure, f, indent=2, default=str)
        
        return structure
    
    def extract_movie_metadata(self, filename: str, content: str = "") -> Dict[str, Any]:
        """Extract movie metadata from filename and content"""
        metadata = {
            'filename': filename,
            'title': None,
            'year': None,
            'language': 'hindi',  # Default assumption
            'genre': None,
            'director': None
        }
        
        # Clean filename for title extraction
        clean_name = filename.lower()
        for ext in ['.txt', '.json', '.csv', '.jpg', '.jpeg', '.png']:
            clean_name = clean_name.replace(ext, '')
        
        # Extract year from filename
        year_matches = re.findall(r'(19|20)\d{2}', filename)
        if year_matches:
            years = [int(y) for y in year_matches if 1970 <= int(y) <= 2025]
            if years:
                metadata['year'] = min(years)
        
        # Extract title (remove year, underscores, hyphens)
        title = re.sub(r'(19|20)\d{2}', '', clean_name)
        title = re.sub(r'[_\-]+', ' ', title)
        title = re.sub(r'\s+', ' ', title).strip()
        metadata['title'] = title.title() if title else filename
        
        # Try to extract additional metadata from content
        if content:
            # Look for director information
            director_patterns = [
                r'director[:\s]+([A-Za-z\s]+)',
                r'directed by[:\s]+([A-Za-z\s]+)',
                r'dir[:\s]+([A-Za-z\s]+)'
            ]
            
            for pattern in director_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    metadata['director'] = match.group(1).strip()
                    break
            
            # Look for genre information
            genre_keywords = ['romance', 'drama', 'action', 'comedy', 'thriller', 'horror', 'musical']
            content_lower = content.lower()
            found_genres = [genre for genre in genre_keywords if genre in content_lower]
            if found_genres:
                metadata['genre'] = found_genres[0]
        
        return metadata
    
    def clean_text_content(self, content: str) -> str:
        """Clean and normalize text content"""
        if not content:
            return ""
        
        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Remove special characters but keep punctuation
        content = re.sub(r'[^\w\s\.\,\!\?\;\:\-]', ' ', content)
        
        # Fix common encoding issues
        replacements = {
            'â€™': "'",
            'â€œ': '"',
            'â€': '"',
            'â€¦': '...',
            'Ã¡': 'á',
            'Ã©': 'é',
            'Ã­': 'í',
            'Ã³': 'ó',
            'Ãº': 'ú'
        }
        
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        return content.strip()
    
    def process_scripts_data(self, structure: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process all script files"""
        logger.info("Processing scripts data...")
        
        scripts_data = []
        script_files = structure.get('scripts-data', [])
        
        for file_info in script_files:
            if file_info['extension'] in ['.txt', '.json', '.csv']:
                try:
                    file_path = Path(file_info['path'])
                    
                    # Read file content
                    if file_info['extension'] == '.json':
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            data = json.load(f)
                            content = str(data) if isinstance(data, dict) else data
                    else:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                    
                    # Clean content
                    cleaned_content = self.clean_text_content(content)
                    
                    if len(cleaned_content) < 100:  # Skip very short files
                        continue
                    
                    # Extract metadata
                    metadata = self.extract_movie_metadata(file_info['name'], cleaned_content)
                    
                    script_data = {
                        'data_type': 'script',
                        'file_info': file_info,
                        'metadata': metadata,
                        'content': cleaned_content,
                        'content_length': len(cleaned_content),
                        'word_count': len(cleaned_content.split())
                    }
                    
                    scripts_data.append(script_data)
                    
                    if len(scripts_data) % 50 == 0:
                        logger.info(f"Processed {len(scripts_data)} script files...")
                
                except Exception as e:
                    logger.error(f"Error processing script file {file_info['name']}: {e}")
                    continue
        
        logger.info(f"Successfully processed {len(scripts_data)} script files")
        return scripts_data
    
    def process_wikipedia_data(self, structure: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process all Wikipedia plot files"""
        logger.info("Processing Wikipedia data...")
        
        wikipedia_data = []
        wiki_files = structure.get('wikipedia-data', [])
        
        for file_info in wiki_files:
            if file_info['extension'] in ['.txt', '.json', '.csv']:
                try:
                    file_path = Path(file_info['path'])
                    
                    # Read file content
                    if file_info['extension'] == '.json':
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            data = json.load(f)
                            content = data.get('plot', str(data)) if isinstance(data, dict) else str(data)
                    elif file_info['extension'] == '.csv':
                        df = pd.read_csv(file_path, encoding='utf-8', errors='ignore')
                        content = ' '.join(df.astype(str).values.flatten())
                    else:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                    
                    # Clean content
                    cleaned_content = self.clean_text_content(content)
                    
                    if len(cleaned_content) < 50:  # Skip very short files
                        continue
                    
                    # Extract metadata
                    metadata = self.extract_movie_metadata(file_info['name'], cleaned_content)
                    
                    wiki_data = {
                        'data_type': 'wikipedia',
                        'file_info': file_info,
                        'metadata': metadata,
                        'content': cleaned_content,
                        'content_length': len(cleaned_content),
                        'word_count': len(cleaned_content.split())
                    }
                    
                    wikipedia_data.append(wiki_data)
                    
                    if len(wikipedia_data) % 50 == 0:
                        logger.info(f"Processed {len(wikipedia_data)} Wikipedia files...")
                
                except Exception as e:
                    logger.error(f"Error processing Wikipedia file {file_info['name']}: {e}")
                    continue
        
        logger.info(f"Successfully processed {len(wikipedia_data)} Wikipedia files")
        return wikipedia_data
    
    def process_trailer_data(self, structure: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process all trailer transcript files"""
        logger.info("Processing trailer data...")
        
        trailer_data = []
        trailer_files = structure.get('trailer-data', [])
        
        for file_info in trailer_files:
            if file_info['extension'] in ['.txt', '.json', '.csv']:
                try:
                    file_path = Path(file_info['path'])
                    
                    # Read file content
                    if file_info['extension'] == '.json':
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            data = json.load(f)
                            content = data.get('transcript', str(data)) if isinstance(data, dict) else str(data)
                    elif file_info['extension'] == '.csv':
                        df = pd.read_csv(file_path, encoding='utf-8', errors='ignore')
                        content = ' '.join(df.astype(str).values.flatten())
                    else:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                    
                    # Clean content
                    cleaned_content = self.clean_text_content(content)
                    
                    if len(cleaned_content) < 30:  # Skip very short files
                        continue
                    
                    # Extract metadata
                    metadata = self.extract_movie_metadata(file_info['name'], cleaned_content)
                    
                    trailer_data_item = {
                        'data_type': 'trailer',
                        'file_info': file_info,
                        'metadata': metadata,
                        'content': cleaned_content,
                        'content_length': len(cleaned_content),
                        'word_count': len(cleaned_content.split())
                    }
                    
                    trailer_data.append(trailer_data_item)
                    
                    if len(trailer_data) % 50 == 0:
                        logger.info(f"Processed {len(trailer_data)} trailer files...")
                
                except Exception as e:
                    logger.error(f"Error processing trailer file {file_info['name']}: {e}")
                    continue
        
        logger.info(f"Successfully processed {len(trailer_data)} trailer files")
        return trailer_data
    
    def process_image_data(self, structure: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process image metadata (for poster analysis)"""
        logger.info("Processing image data...")
        
        image_data = []
        image_files = structure.get('images-data', [])
        
        for file_info in image_files:
            if file_info['extension'] in ['.jpg', '.jpeg', '.png', '.gif']:
                try:
                    # Extract metadata from filename
                    metadata = self.extract_movie_metadata(file_info['name'])
                    
                    image_data_item = {
                        'data_type': 'image',
                        'file_info': file_info,
                        'metadata': metadata,
                        'image_path': file_info['path']
                    }
                    
                    image_data.append(image_data_item)
                    
                    if len(image_data) % 100 == 0:
                        logger.info(f"Processed {len(image_data)} image files...")
                
                except Exception as e:
                    logger.error(f"Error processing image file {file_info['name']}: {e}")
                    continue
        
        logger.info(f"Successfully processed {len(image_data)} image files")
        return image_data
    
    def merge_movie_data(self, scripts_data: List[Dict], wikipedia_data: List[Dict], 
                        trailer_data: List[Dict], image_data: List[Dict]) -> List[Dict[str, Any]]:
        """Merge data from different sources for the same movies"""
        logger.info("Merging movie data from different sources...")
        
        # Create a mapping based on movie titles and years
        movie_map = {}
        
        # Add scripts data
        for item in scripts_data:
            key = self.create_movie_key(item['metadata'])
            if key not in movie_map:
                movie_map[key] = {
                    'metadata': item['metadata'],
                    'script': None,
                    'wikipedia': None,
                    'trailer': None,
                    'images': []
                }
            movie_map[key]['script'] = item
        
        # Add Wikipedia data
        for item in wikipedia_data:
            key = self.create_movie_key(item['metadata'])
            if key not in movie_map:
                movie_map[key] = {
                    'metadata': item['metadata'],
                    'script': None,
                    'wikipedia': None,
                    'trailer': None,
                    'images': []
                }
            movie_map[key]['wikipedia'] = item
        
        # Add trailer data
        for item in trailer_data:
            key = self.create_movie_key(item['metadata'])
            if key not in movie_map:
                movie_map[key] = {
                    'metadata': item['metadata'],
                    'script': None,
                    'wikipedia': None,
                    'trailer': None,
                    'images': []
                }
            movie_map[key]['trailer'] = item
        
        # Add image data
        for item in image_data:
            key = self.create_movie_key(item['metadata'])
            if key not in movie_map:
                movie_map[key] = {
                    'metadata': item['metadata'],
                    'script': None,
                    'wikipedia': None,
                    'trailer': None,
                    'images': []
                }
            movie_map[key]['images'].append(item)
        
        # Convert to list and add combined content
        merged_data = []
        for key, movie_data in movie_map.items():
            # Combine text content from all sources
            combined_content = ""
            content_sources = []
            
            if movie_data['script']:
                combined_content += movie_data['script']['content'] + " "
                content_sources.append('script')
            
            if movie_data['wikipedia']:
                combined_content += movie_data['wikipedia']['content'] + " "
                content_sources.append('wikipedia')
            
            if movie_data['trailer']:
                combined_content += movie_data['trailer']['content'] + " "
                content_sources.append('trailer')
            
            movie_data['combined_content'] = combined_content.strip()
            movie_data['content_sources'] = content_sources
            movie_data['total_content_length'] = len(combined_content)
            
            # Only include movies with substantial content
            if len(combined_content) > 200:
                merged_data.append(movie_data)
        
        logger.info(f"Merged data for {len(merged_data)} movies")
        return merged_data
    
    def create_movie_key(self, metadata: Dict[str, Any]) -> str:
        """Create a unique key for movie identification"""
        title = metadata.get('title', '').lower().strip()
        year = metadata.get('year', 'unknown')
        
        # Clean title for better matching
        title = re.sub(r'[^\w\s]', '', title)
        title = re.sub(r'\s+', '_', title)
        
        return f"{title}_{year}"
    
    def save_processed_data(self, merged_data: List[Dict[str, Any]]) -> None:
        """Save processed data to files"""
        logger.info("Saving processed data...")
        
        # Save complete processed data
        with open(self.output_dir / 'processed_movies.json', 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, indent=2, default=str, ensure_ascii=False)
        
        # Create a summary DataFrame
        summary_data = []
        for movie in merged_data:
            summary_data.append({
                'title': movie['metadata']['title'],
                'year': movie['metadata']['year'],
                'director': movie['metadata']['director'],
                'genre': movie['metadata']['genre'],
                'content_sources': ','.join(movie['content_sources']),
                'total_content_length': movie['total_content_length'],
                'has_script': movie['script'] is not None,
                'has_wikipedia': movie['wikipedia'] is not None,
                'has_trailer': movie['trailer'] is not None,
                'image_count': len(movie['images'])
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv(self.output_dir / 'movies_summary.csv', index=False)
        
        # Generate statistics
        stats = {
            'total_movies': len(merged_data),
            'movies_with_scripts': sum(1 for m in merged_data if m['script']),
            'movies_with_wikipedia': sum(1 for m in merged_data if m['wikipedia']),
            'movies_with_trailers': sum(1 for m in merged_data if m['trailer']),
            'movies_with_images': sum(1 for m in merged_data if m['images']),
            'year_range': {
                'min': min(m['metadata']['year'] for m in merged_data if m['metadata']['year']),
                'max': max(m['metadata']['year'] for m in merged_data if m['metadata']['year'])
            },
            'content_statistics': {
                'total_content_length': sum(m['total_content_length'] for m in merged_data),
                'average_content_length': np.mean([m['total_content_length'] for m in merged_data]),
                'median_content_length': np.median([m['total_content_length'] for m in merged_data])
            }
        }
        
        with open(self.output_dir / 'dataset_statistics.json', 'w') as f:
            json.dump(stats, f, indent=2, default=str)
        
        logger.info(f"Processed data saved to {self.output_dir}")
        logger.info(f"Dataset statistics: {stats}")
    
    def run_preprocessing(self) -> None:
        """Run the complete preprocessing pipeline"""
        logger.info("Starting Bollywood dataset preprocessing...")
        
        # Step 1: Scan dataset structure
        structure = self.scan_dataset_structure()
        
        # Step 2: Process each data type
        scripts_data = self.process_scripts_data(structure)
        wikipedia_data = self.process_wikipedia_data(structure)
        trailer_data = self.process_trailer_data(structure)
        image_data = self.process_image_data(structure)
        
        # Step 3: Merge data by movie
        merged_data = self.merge_movie_data(scripts_data, wikipedia_data, trailer_data, image_data)
        
        # Step 4: Save processed data
        self.save_processed_data(merged_data)
        
        logger.info("Preprocessing completed successfully!")

# Main execution function for Jupyter
def run_preprocessing(dataset_path: str):
    """Run preprocessing with the given dataset path"""
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset path {dataset_path} does not exist")
        return False
    
    print("🚀 Starting Bollywood Dataset Preprocessing...")
    print(f"📁 Dataset path: {dataset_path}")
    
    try:
        preprocessor = BollywoodDatasetPreprocessor(dataset_path)
        preprocessor.run_preprocessing()
        print("✅ Preprocessing completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Error during preprocessing: {e}")
        return False

# Example usage - CHANGE THIS PATH TO YOUR ACTUAL DATASET PATH
if __name__ == "__main__":
    # Replace this with your actual path to the Bollywood-Data repository
    DATASET_PATH = "/path/to/your/Bollywood-Data"  # ⚠️ CHANGE THIS PATH!
    
    # Check if path exists
    if not os.path.exists(DATASET_PATH):
        print("⚠️  Please update the DATASET_PATH variable with your actual path to the Bollywood-Data repository")
        print("Example paths:")
        print("  - Windows: C:/Users/YourName/Downloads/Bollywood-Data")
        print("  - Mac/Linux: /Users/YourName/Downloads/Bollywood-Data")
        print("  - Current directory: ./Bollywood-Data")
    else:
        # Run the preprocessing
        success = run_preprocessing(DATASET_PATH)
        if success:
            print("\n📊 Next steps:")
            print("1. Check the 'processed_data' folder for output files")
            print("2. Run the bias analysis script next")
