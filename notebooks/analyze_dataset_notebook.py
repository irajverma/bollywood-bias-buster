import json
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Dict, List, Any
import sys
import os

# Add the models directory to the path
current_dir = Path.cwd()
models_dir = current_dir / "models"
if models_dir.exists():
    sys.path.append(str(models_dir))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import the bias detection model
try:
    from bias_detection_model import GenderBiasDetectionModel
except ImportError:
    print("❌ Could not import bias detection model. Make sure the models directory exists.")
    print("Please run the preprocessing step first or check the file structure.")

class NotebookDatasetAnalyzer:
    """
    Jupyter-friendly analyzer for the complete Bollywood dataset
    """
    
    def __init__(self, processed_data_path: str = "processed_data"):
        self.processed_data_path = Path(processed_data_path)
        self.model = GenderBiasDetectionModel()
        self.results = []
        
        # Create output directory
        self.output_dir = Path("analysis_results")
        self.output_dir.mkdir(exist_ok=True)
    
    def load_processed_data(self) -> List[Dict[str, Any]]:
        """Load preprocessed movie data"""
        data_file = self.processed_data_path / "processed_movies.json"
        
        if not data_file.exists():
            print(f"❌ Processed data file not found: {data_file}")
            print("Please run the preprocessing step first")
            return []
        
        print(f"📂 Loading processed data from {data_file}")
        
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Loaded {len(data)} movies")
        return data
    
    def analyze_single_movie(self, movie_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single movie"""
        try:
            result = self.model.analyze_movie(movie_data)
            if result:
                title = result['movie_metadata']['title']
                year = result['movie_metadata']['year']
                bias_score = result['bias_scores']['overall']
                print(f"✅ Analyzed: {title} ({year}) - Bias Score: {bias_score:.1f}")
            return result
        except Exception as e:
            title = movie_data.get('metadata', {}).get('title', 'Unknown')
            print(f"❌ Error analyzing {title}: {e}")
            return None
    
    def analyze_sample_movies(self, movies_data: List[Dict[str, Any]], sample_size: int = 50) -> List[Dict[str, Any]]:
        """Analyze a sample of movies for testing"""
        print(f"🔍 Analyzing sample of {sample_size} movies...")
        
        # Filter movies with sufficient content
        valid_movies = [movie for movie in movies_data 
                       if movie.get('total_content_length', 0) > 500]
        
        print(f"📊 Found {len(valid_movies)} movies with sufficient content")
        
        # Take a sample
        sample_movies = valid_movies[:sample_size]
        print(f"🎬 Analyzing {len(sample_movies)} movies...")
        
        results = []
        for i, movie_data in enumerate(sample_movies):
            result = self.analyze_single_movie(movie_data)
            if result:
                results.append(result)
            
            # Progress update
            if (i + 1) % 10 == 0:
                print(f"📈 Progress: {i + 1}/{len(sample_movies)} movies processed")
        
        print(f"✅ Successfully analyzed {len(results)} movies")
        return results
    
    def analyze_all_movies(self, movies_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze all movies in the dataset"""
        print("🚀 Starting full dataset analysis...")
        
        # Filter movies with sufficient content
        valid_movies = [movie for movie in movies_data 
                       if movie.get('total_content_length', 0) > 500]
        
        print(f"📊 Analyzing {len(valid_movies)} movies with sufficient content")
        
        results = []
        for i, movie_data in enumerate(valid_movies):
            result = self.analyze_single_movie(movie_data)
            if result:
                results.append(result)
            
            # Progress updates
            if (i + 1) % 50 == 0:
                print(f"📈 Progress: {i + 1}/{len(valid_movies)} movies processed")
        
        print(f"✅ Successfully analyzed {len(results)} movies")
        return results
    
    def generate_quick_report(self, analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a quick summary report"""
        if not analysis_results:
            return {"error": "No analysis results to report"}
        
        print("📊 Generating analysis report...")
        
        # Basic statistics
        total_movies = len(analysis_results)
        total_characters = sum(r['characters']['total'] for r in analysis_results)
        total_male_chars = sum(r['characters']['male'] for r in analysis_results)
        total_female_chars = sum(r['characters']['female'] for r in analysis_results)
        
        # Bias score statistics
        overall_scores = [r['bias_scores']['overall'] for r in analysis_results]
        occupation_scores = [r['bias_scores']['occupation_gap'] for r in analysis_results]
        agency_scores = [r['bias_scores']['agency_gap'] for r in analysis_results]
        appearance_scores = [r['bias_scores']['appearance_focus'] for r in analysis_results]
        
        # Most and least biased movies
        sorted_by_bias = sorted(analysis_results, key=lambda x: x['bias_scores']['overall'])
        most_biased = sorted_by_bias[-5:]  # Top 5 most biased
        least_biased = sorted_by_bias[:5]  # Top 5 least biased
        
        # Decade analysis
        decade_data = {}
        for result in analysis_results:
            year = result['movie_metadata'].get('year')
            if year:
                decade = (year // 10) * 10
                decade_key = f"{decade}s"
                if decade_key not in decade_data:
                    decade_data[decade_key] = []
                decade_data[decade_key].append(result['bias_scores']['overall'])
        
        decade_averages = {decade: np.mean(scores) for decade, scores in decade_data.items() if len(scores) >= 3}
        
        report = {
            'summary': {
                'total_movies_analyzed': total_movies,
                'total_characters': total_characters,
                'male_characters': total_male_chars,
                'female_characters': total_female_chars,
                'gender_ratio': f"{total_male_chars}:{total_female_chars}"
            },
            'bias_scores': {
                'overall_average': np.mean(overall_scores),
                'occupation_gap_average': np.mean(occupation_scores),
                'agency_gap_average': np.mean(agency_scores),
                'appearance_focus_average': np.mean(appearance_scores)
            },
            'most_biased_movies': [
                {
                    'title': movie['movie_metadata']['title'],
                    'year': movie['movie_metadata']['year'],
                    'bias_score': movie['bias_scores']['overall']
                } for movie in most_biased
            ],
            'least_biased_movies': [
                {
                    'title': movie['movie_metadata']['title'],
                    'year': movie['movie_metadata']['year'],
                    'bias_score': movie['bias_scores']['overall']
                } for movie in least_biased
            ],
            'decade_trends': decade_averages
        }
        
        return report
    
    def save_results(self, analysis_results: List[Dict[str, Any]], report: Dict[str, Any]) -> None:
        """Save analysis results"""
        print("💾 Saving analysis results...")
        
        # Save detailed results
        with open(self.output_dir / 'analysis_results.json', 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=2, default=str, ensure_ascii=False)
        
        # Save report
        with open(self.output_dir / 'bias_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str, ensure_ascii=False)
        
        # Create CSV summary
        summary_data = []
        for result in analysis_results:
            summary_data.append({
                'title': result['movie_metadata']['title'],
                'year': result['movie_metadata']['year'],
                'director': result['movie_metadata']['director'],
                'total_characters': result['characters']['total'],
                'male_characters': result['characters']['male'],
                'female_characters': result['characters']['female'],
                'overall_bias_score': result['bias_scores']['overall'],
                'occupation_gap': result['bias_scores']['occupation_gap'],
                'agency_gap': result['bias_scores']['agency_gap'],
                'appearance_focus': result['bias_scores']['appearance_focus'],
                'bias_examples_count': len(result['bias_examples'])
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv(self.output_dir / 'analysis_summary.csv', index=False)
        
        print(f"✅ Results saved to {self.output_dir}")
    
    def print_report_summary(self, report: Dict[str, Any]) -> None:
        """Print a summary of the analysis"""
        print("\n" + "="*60)
        print("🎬 BOLLYWOOD BIAS ANALYSIS SUMMARY")
        print("="*60)
        
        summary = report['summary']
        print(f"📊 Movies Analyzed: {summary['total_movies_analyzed']}")
        print(f"👥 Total Characters: {summary['total_characters']}")
        print(f"⚖️  Gender Distribution: {summary['gender_ratio']} (Male:Female)")
        
        print(f"\n📈 AVERAGE BIAS SCORES (0-100, higher = more biased):")
        bias_scores = report['bias_scores']
        print(f"   Overall Bias: {bias_scores['overall_average']:.1f}")
        print(f"   Occupation Gap: {bias_scores['occupation_gap_average']:.1f}")
        print(f"   Agency Gap: {bias_scores['agency_gap_average']:.1f}")
        print(f"   Appearance Focus: {bias_scores['appearance_focus_average']:.1f}")
        
        print(f"\n🔴 MOST BIASED MOVIES:")
        for movie in report['most_biased_movies']:
            print(f"   • {movie['title']} ({movie['year']}): {movie['bias_score']:.1f}")
        
        print(f"\n🟢 LEAST BIASED MOVIES:")
        for movie in report['least_biased_movies']:
            print(f"   • {movie['title']} ({movie['year']}): {movie['bias_score']:.1f}")
        
        if report['decade_trends']:
            print(f"\n📅 DECADE TRENDS:")
            for decade, avg_bias in sorted(report['decade_trends'].items()):
                print(f"   • {decade}: {avg_bias:.1f}")
        
        print("\n" + "="*60)

# Main functions for Jupyter execution
def run_sample_analysis(sample_size: int = 50):
    """Run analysis on a sample of movies"""
    analyzer = NotebookDatasetAnalyzer()
    
    # Load data
    movies_data = analyzer.load_processed_data()
    if not movies_data:
        return None
    
    # Analyze sample
    results = analyzer.analyze_sample_movies(movies_data, sample_size)
    if not results:
        print("❌ No movies were successfully analyzed")
        return None
    
    # Generate report
    report = analyzer.generate_quick_report(results)
    
    # Save results
    analyzer.save_results(results, report)
    
    # Print summary
    analyzer.print_report_summary(report)
    
    return results, report

def run_full_analysis():
    """Run analysis on the complete dataset"""
    analyzer = NotebookDatasetAnalyzer()
    
    # Load data
    movies_data = analyzer.load_processed_data()
    if not movies_data:
        return None
    
    # Analyze all movies
    results = analyzer.analyze_all_movies(movies_data)
    if not results:
        print("❌ No movies were successfully analyzed")
        return None
    
    # Generate report
    report = analyzer.generate_quick_report(results)
    
    # Save results
    analyzer.save_results(results, report)
    
    # Print summary
    analyzer.print_report_summary(report)
    
    return results, report

# Example usage
if __name__ == "__main__":
    print("🎬 Bollywood Bias Analysis - Notebook Version")
    print("\nAvailable functions:")
    print("1. run_sample_analysis(50) - Analyze 50 movies")
    print("2. run_full_analysis() - Analyze all movies")
    print("\nExample:")
    print("results, report = run_sample_analysis(20)")
