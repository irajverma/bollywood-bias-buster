import json
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Dict, List, Any
import multiprocessing as mp
from functools import partial
import sys
import os

# Add the models directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.bias_detection_model import GenderBiasDetectionModel

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FullDatasetAnalyzer:
    """
    Analyzer for the complete Bollywood dataset
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
            logger.error(f"Processed data file not found: {data_file}")
            logger.error("Please run preprocess_dataset.py first")
            return []
        
        logger.info(f"Loading processed data from {data_file}")
        
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"Loaded {len(data)} movies")
        return data
    
    def analyze_single_movie(self, movie_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single movie (for multiprocessing)"""
        try:
            result = self.model.analyze_movie(movie_data)
            if result:
                logger.info(f"Analyzed: {result['movie_metadata']['title']} ({result['movie_metadata']['year']})")
            return result
        except Exception as e:
            logger.error(f"Error analyzing movie {movie_data.get('metadata', {}).get('title', 'Unknown')}: {e}")
            return None
    
    def analyze_dataset_parallel(self, movies_data: List[Dict[str, Any]], num_processes: int = None) -> List[Dict[str, Any]]:
        """Analyze dataset using parallel processing"""
        if num_processes is None:
            num_processes = min(mp.cpu_count(), 8)  # Use up to 8 processes
        
        logger.info(f"Starting parallel analysis with {num_processes} processes")
        
        # Filter movies with sufficient content
        valid_movies = [movie for movie in movies_data 
                       if movie.get('total_content_length', 0) > 500]
        
        logger.info(f"Analyzing {len(valid_movies)} movies with sufficient content")
        
        # Use multiprocessing for parallel analysis
        with mp.Pool(processes=num_processes) as pool:
            results = pool.map(self.analyze_single_movie, valid_movies)
        
        # Filter out None results
        valid_results = [result for result in results if result is not None]
        
        logger.info(f"Successfully analyzed {len(valid_results)} movies")
        return valid_results
    
    def analyze_dataset_sequential(self, movies_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze dataset sequentially (fallback for debugging)"""
        logger.info("Starting sequential analysis")
        
        results = []
        valid_movies = [movie for movie in movies_data 
                       if movie.get('total_content_length', 0) > 500]
        
        for i, movie_data in enumerate(valid_movies):
            try:
                result = self.analyze_single_movie(movie_data)
                if result:
                    results.append(result)
                
                if (i + 1) % 50 == 0:
                    logger.info(f"Processed {i + 1}/{len(valid_movies)} movies")
                    
            except Exception as e:
                logger.error(f"Error processing movie {i}: {e}")
                continue
        
        return results
    
    def generate_comprehensive_report(self, analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive bias analysis report"""
        logger.info("Generating comprehensive report...")
        
        # Basic statistics
        total_movies = len(analysis_results)
        total_characters = sum(r['characters']['total'] for r in analysis_results)
        total_male_chars = sum(r['characters']['male'] for r in analysis_results)
        total_female_chars = sum(r['characters']['female'] for r in analysis_results)
        
        # Bias score statistics
        bias_scores = {
            'occupation_gap': [r['bias_scores']['occupation_gap'] for r in analysis_results],
            'agency_gap': [r['bias_scores']['agency_gap'] for r in analysis_results],
            'appearance_focus': [r['bias_scores']['appearance_focus'] for r in analysis_results],
            'relationship_defining': [r['bias_scores']['relationship_defining'] for r in analysis_results],
            'dialogue_imbalance': [r['bias_scores']['dialogue_imbalance'] for r in analysis_results],
            'screen_time_imbalance': [r['bias_scores']['screen_time_imbalance'] for r in analysis_results],
            'overall': [r['bias_scores']['overall'] for r in analysis_results]
        }
        
        # Calculate statistics for each bias type
        bias_statistics = {}
        for bias_type, scores in bias_scores.items():
            bias_statistics[bias_type] = {
                'mean': np.mean(scores),
                'median': np.median(scores),
                'std': np.std(scores),
                'min': np.min(scores),
                'max': np.max(scores),
                'percentile_25': np.percentile(scores, 25),
                'percentile_75': np.percentile(scores, 75)
            }
        
        # Decade analysis
        decade_analysis = self.analyze_by_decade(analysis_results)
        
        # Director analysis
        director_analysis = self.analyze_by_director(analysis_results)
        
        # Genre analysis (if available)
        genre_analysis = self.analyze_by_genre(analysis_results)
        
        # Most and least biased movies
        sorted_by_bias = sorted(analysis_results, key=lambda x: x['bias_scores']['overall'])
        most_biased = sorted_by_bias[-10:]  # Top 10 most biased
        least_biased = sorted_by_bias[:10]  # Top 10 least biased
        
        # Bias examples summary
        all_bias_examples = []
        for result in analysis_results:
            for example in result['bias_examples']:
                example['movie_title'] = result['movie_metadata']['title']
                example['movie_year'] = result['movie_metadata']['year']
                all_bias_examples.append(example)
        
        # Group bias examples by type
        bias_examples_by_type = {}
        for example in all_bias_examples:
            bias_type = example['bias_type']
            if bias_type not in bias_examples_by_type:
                bias_examples_by_type[bias_type] = []
            bias_examples_by_type[bias_type].append(example)
        
        # Character representation analysis
        character_analysis = self.analyze_character_representation(analysis_results)
        
        report = {
            'analysis_summary': {
                'total_movies_analyzed': total_movies,
                'total_characters': total_characters,
                'male_characters': total_male_chars,
                'female_characters': total_female_chars,
                'gender_ratio': f"{total_male_chars}:{total_female_chars}",
                'analysis_date': pd.Timestamp.now().isoformat()
            },
            'bias_statistics': bias_statistics,
            'decade_trends': decade_analysis,
            'director_analysis': director_analysis,
            'genre_analysis': genre_analysis,
            'most_biased_movies': [
                {
                    'title': movie['movie_metadata']['title'],
                    'year': movie['movie_metadata']['year'],
                    'director': movie['movie_metadata']['director'],
                    'overall_bias_score': movie['bias_scores']['overall'],
                    'main_bias_types': self.get_main_bias_types(movie['bias_scores'])
                } for movie in most_biased
            ],
            'least_biased_movies': [
                {
                    'title': movie['movie_metadata']['title'],
                    'year': movie['movie_metadata']['year'],
                    'director': movie['movie_metadata']['director'],
                    'overall_bias_score': movie['bias_scores']['overall'],
                    'main_bias_types': self.get_main_bias_types(movie['bias_scores'])
                } for movie in least_biased
            ],
            'bias_examples_summary': {
                'total_examples': len(all_bias_examples),
                'by_type': {bias_type: len(examples) for bias_type, examples in bias_examples_by_type.items()},
                'sample_examples': {bias_type: examples[:5] for bias_type, examples in bias_examples_by_type.items()}
            },
            'character_representation': character_analysis,
            'recommendations': self.generate_recommendations(bias_statistics, decade_analysis)
        }
        
        return report
    
    def analyze_by_decade(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze bias trends by decade"""
        decade_data = {}
        
        for result in results:
            year = result['movie_metadata'].get('year')
            if not year:
                continue
            
            decade = (year // 10) * 10
            decade_key = f"{decade}s"
            
            if decade_key not in decade_data:
                decade_data[decade_key] = []
            
            decade_data[decade_key].append(result)
        
        decade_analysis = {}
        for decade, movies in decade_data.items():
            if len(movies) < 5:  # Skip decades with too few movies
                continue
            
            bias_scores = {
                'occupation_gap': np.mean([m['bias_scores']['occupation_gap'] for m in movies]),
                'agency_gap': np.mean([m['bias_scores']['agency_gap'] for m in movies]),
                'appearance_focus': np.mean([m['bias_scores']['appearance_focus'] for m in movies]),
                'relationship_defining': np.mean([m['bias_scores']['relationship_defining'] for m in movies]),
                'dialogue_imbalance': np.mean([m['bias_scores']['dialogue_imbalance'] for m in movies]),
                'screen_time_imbalance': np.mean([m['bias_scores']['screen_time_imbalance'] for m in movies]),
                'overall': np.mean([m['bias_scores']['overall'] for m in movies])
            }
            
            decade_analysis[decade] = {
                'movie_count': len(movies),
                'bias_scores': bias_scores,
                'character_stats': {
                    'total_characters': sum(m['characters']['total'] for m in movies),
                    'male_characters': sum(m['characters']['male'] for m in movies),
                    'female_characters': sum(m['characters']['female'] for m in movies)
                }
            }
        
        return decade_analysis
    
    def analyze_by_director(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze bias patterns by director"""
        director_data = {}
        
        for result in results:
            director = result['movie_metadata'].get('director')
            if not director or director.lower() in ['unknown', 'none', '']:
                continue
            
            if director not in director_data:
                director_data[director] = []
            
            director_data[director].append(result)
        
        # Only analyze directors with multiple movies
        director_analysis = {}
        for director, movies in director_data.items():
            if len(movies) < 2:
                continue
            
            bias_scores = {
                'occupation_gap': np.mean([m['bias_scores']['occupation_gap'] for m in movies]),
                'agency_gap': np.mean([m['bias_scores']['agency_gap'] for m in movies]),
                'appearance_focus': np.mean([m['bias_scores']['appearance_focus'] for m in movies]),
                'relationship_defining': np.mean([m['bias_scores']['relationship_defining'] for m in movies]),
                'overall': np.mean([m['bias_scores']['overall'] for m in movies])
            }
            
            director_analysis[director] = {
                'movie_count': len(movies),
                'bias_scores': bias_scores,
                'movies': [m['movie_metadata']['title'] for m in movies]
            }
        
        # Sort by overall bias score
        sorted_directors = sorted(director_analysis.items(), 
                                key=lambda x: x[1]['bias_scores']['overall'], 
                                reverse=True)
        
        return dict(sorted_directors[:20])  # Top 20 directors
    
    def analyze_by_genre(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze bias patterns by genre"""
        genre_data = {}
        
        for result in results:
            genre = result['movie_metadata'].get('genre')
            if not genre or genre.lower() in ['unknown', 'none', '']:
                continue
            
            if genre not in genre_data:
                genre_data[genre] = []
            
            genre_data[genre].append(result)
        
        genre_analysis = {}
        for genre, movies in genre_data.items():
            if len(movies) < 5:  # Skip genres with too few movies
                continue
            
            bias_scores = {
                'occupation_gap': np.mean([m['bias_scores']['occupation_gap'] for m in movies]),
                'agency_gap': np.mean([m['bias_scores']['agency_gap'] for m in movies]),
                'appearance_focus': np.mean([m['bias_scores']['appearance_focus'] for m in movies]),
                'relationship_defining': np.mean([m['bias_scores']['relationship_defining'] for m in movies]),
                'overall': np.mean([m['bias_scores']['overall'] for m in movies])
            }
            
            genre_analysis[genre] = {
                'movie_count': len(movies),
                'bias_scores': bias_scores
            }
        
        return genre_analysis
    
    def analyze_character_representation(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze character representation patterns"""
        total_movies = len(results)
        
        # Movies with female protagonists (more female characters than male)
        female_protagonist_movies = sum(1 for r in results if r['characters']['female'] > r['characters']['male'])
        
        # Movies with balanced representation (within 1 character difference)
        balanced_movies = sum(1 for r in results if abs(r['characters']['female'] - r['characters']['male']) <= 1)
        
        # Average characters per movie
        avg_total_chars = np.mean([r['characters']['total'] for r in results])
        avg_male_chars = np.mean([r['characters']['male'] for r in results])
        avg_female_chars = np.mean([r['characters']['female'] for r in results])
        
        # Professional representation
        movies_with_female_professionals = 0
        movies_with_male_professionals = 0
        
        for result in results:
            # Check if movie has female characters with professions
            female_chars_with_professions = sum(1 for char in result['characters']['character_details'] 
                                              if char['gender'] == 'female' and char['profession_count'] > 0)
            if female_chars_with_professions > 0:
                movies_with_female_professionals += 1
            
            # Check if movie has male characters with professions
            male_chars_with_professions = sum(1 for char in result['characters']['character_details'] 
                                            if char['gender'] == 'male' and char['profession_count'] > 0)
            if male_chars_with_professions > 0:
                movies_with_male_professionals += 1
        
        return {
            'total_movies': total_movies,
            'female_protagonist_movies': female_protagonist_movies,
            'female_protagonist_percentage': (female_protagonist_movies / total_movies) * 100,
            'balanced_representation_movies': balanced_movies,
            'balanced_representation_percentage': (balanced_movies / total_movies) * 100,
            'average_characters': {
                'total': avg_total_chars,
                'male': avg_male_chars,
                'female': avg_female_chars
            },
            'professional_representation': {
                'movies_with_female_professionals': movies_with_female_professionals,
                'movies_with_male_professionals': movies_with_male_professionals,
                'female_professional_percentage': (movies_with_female_professionals / total_movies) * 100,
                'male_professional_percentage': (movies_with_male_professionals / total_movies) * 100
            }
        }
    
    def get_main_bias_types(self, bias_scores: Dict[str, float]) -> List[str]:
        """Get the main bias types for a movie (scores above threshold)"""
        threshold = 60  # Consider scores above 60 as significant bias
        main_biases = []
        
        for bias_type, score in bias_scores.items():
            if bias_type != 'overall' and score > threshold:
                main_biases.append(bias_type.replace('_', ' ').title())
        
        return main_biases
    
    def generate_recommendations(self, bias_statistics: Dict[str, Any], decade_analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # Overall bias level recommendations
        overall_mean = bias_statistics['overall']['mean']
        if overall_mean > 70:
            recommendations.append("High overall bias detected. Immediate action needed to improve gender representation.")
        elif overall_mean > 50:
            recommendations.append("Moderate bias levels found. Focus on balanced character development and representation.")
        else:
            recommendations.append("Relatively low bias levels. Continue current practices while monitoring for improvements.")
        
        # Specific bias type recommendations
        if bias_statistics['occupation_gap']['mean'] > 60:
            recommendations.append("Significant occupation gap found. Ensure female characters have clear professional identities.")
        
        if bias_statistics['agency_gap']['mean'] > 60:
            recommendations.append("Agency gap detected. Give female characters more active, decision-making roles.")
        
        if bias_statistics['appearance_focus']['mean'] > 60:
            recommendations.append("Excessive focus on female appearance. Balance physical descriptions with character traits.")
        
        if bias_statistics['relationship_defining']['mean'] > 60:
            recommendations.append("Characters often defined by relationships. Develop independent character identities.")
        
        # Trend-based recommendations
        if len(decade_analysis) > 1:
            decades = sorted(decade_analysis.keys())
            if len(decades) >= 2:
                recent_bias = decade_analysis[decades[-1]]['bias_scores']['overall']
                older_bias = decade_analysis[decades[0]]['bias_scores']['overall']
                
                if recent_bias > older_bias:
                    recommendations.append("Bias levels have increased over time. Review recent practices and policies.")
                else:
                    recommendations.append("Positive trend: bias levels have decreased over time. Continue improvement efforts.")
        
        return recommendations
    
    def save_results(self, analysis_results: List[Dict[str, Any]], report: Dict[str, Any]) -> None:
        """Save analysis results and report"""
        logger.info("Saving analysis results...")
        
        # Save detailed results
        with open(self.output_dir / 'detailed_analysis_results.json', 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, indent=2, default=str, ensure_ascii=False)
        
        # Save comprehensive report
        with open(self.output_dir / 'comprehensive_bias_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, default=str, ensure_ascii=False)
        
        # Create CSV summary for easy analysis
        summary_data = []
        for result in analysis_results:
            summary_data.append({
                'title': result['movie_metadata']['title'],
                'year': result['movie_metadata']['year'],
                'director': result['movie_metadata']['director'],
                'genre': result['movie_metadata']['genre'],
                'total_characters': result['characters']['total'],
                'male_characters': result['characters']['male'],
                'female_characters': result['characters']['female'],
                'occupation_gap_score': result['bias_scores']['occupation_gap'],
                'agency_gap_score': result['bias_scores']['agency_gap'],
                'appearance_focus_score': result['bias_scores']['appearance_focus'],
                'relationship_defining_score': result['bias_scores']['relationship_defining'],
                'dialogue_imbalance_score': result['bias_scores']['dialogue_imbalance'],
                'screen_time_imbalance_score': result['bias_scores']['screen_time_imbalance'],
                'overall_bias_score': result['bias_scores']['overall'],
                'bias_examples_count': len(result['bias_examples']),
                'content_sources': ','.join(result['content_sources'])
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv(self.output_dir / 'bias_analysis_summary.csv', index=False)
        
        # Save bias examples separately
        all_examples = []
        for result in analysis_results:
            for example in result['bias_examples']:
                all_examples.append({
                    'movie_title': result['movie_metadata']['title'],
                    'movie_year': result['movie_metadata']['year'],
                    'bias_type': example['bias_type'],
                    'character_name': example['character_name'],
                    'excerpt': example['excerpt'],
                    'severity': example['severity'],
                    'explanation': example['explanation'],
                    'suggestion': example['suggestion']
                })
        
        examples_df = pd.DataFrame(all_examples)
        examples_df.to_csv(self.output_dir / 'bias_examples.csv', index=False)
        
        logger.info(f"Results saved to {self.output_dir}")
        logger.info(f"- Detailed results: detailed_analysis_results.json")
        logger.info(f"- Comprehensive report: comprehensive_bias_report.json")
        logger.info(f"- Summary CSV: bias_analysis_summary.csv")
        logger.info(f"- Bias examples: bias_examples.csv")
    
    def run_full_analysis(self, use_parallel: bool = True) -> None:
        """Run the complete analysis pipeline"""
        logger.info("Starting full dataset analysis...")
        
        # Load processed data
        movies_data = self.load_processed_data()
        if not movies_data:
            logger.error("No data to analyze. Exiting.")
            return
        
        # Run analysis
        if use_parallel:
            try:
                analysis_results = self.analyze_dataset_parallel(movies_data)
            except Exception as e:
                logger.error(f"Parallel processing failed: {e}")
                logger.info("Falling back to sequential processing...")
                analysis_results = self.analyze_dataset_sequential(movies_data)
        else:
            analysis_results = self.analyze_dataset_sequential(movies_data)
        
        if not analysis_results:
            logger.error("No movies were successfully analyzed. Exiting.")
            return
        
        # Generate comprehensive report
        report = self.generate_comprehensive_report(analysis_results)
        
        # Save results
        self.save_results(analysis_results, report)
        
        # Print summary
        self.print_analysis_summary(report)
        
        logger.info("Full dataset analysis completed successfully!")
    
    def print_analysis_summary(self, report: Dict[str, Any]) -> None:
        """Print a summary of the analysis results"""
        print("\n" + "="*80)
        print("BOLLYWOOD BIAS ANALYSIS - SUMMARY REPORT")
        print("="*80)
        
        summary = report['analysis_summary']
        print(f"Movies Analyzed: {summary['total_movies_analyzed']}")
        print(f"Total Characters: {summary['total_characters']}")
        print(f"Gender Distribution: {summary['gender_ratio']} (Male:Female)")
        
        print(f"\nBIAS SCORES (0-100, higher = more biased):")
        bias_stats = report['bias_statistics']
        for bias_type, stats in bias_stats.items():
            print(f"- {bias_type.replace('_', ' ').title()}: {stats['mean']:.1f} (±{stats['std']:.1f})")
        
        print(f"\nMOST BIASED MOVIES:")
        for movie in report['most_biased_movies'][-5:]:  # Top 5
            print(f"- {movie['title']} ({movie['year']}): {movie['overall_bias_score']:.1f}")
        
        print(f"\nLEAST BIASED MOVIES:")
        for movie in report['least_biased_movies'][:5]:  # Top 5
            print(f"- {movie['title']} ({movie['year']}): {movie['overall_bias_score']:.1f}")
        
        if 'decade_trends' in report and report['decade_trends']:
            print(f"\nDECADE TRENDS:")
            for decade, data in sorted(report['decade_trends'].items()):
                print(f"- {decade}: {data['bias_scores']['overall']:.1f} ({data['movie_count']} movies)")
        
        print(f"\nKEY RECOMMENDATIONS:")
        for rec in report['recommendations']:
            print(f"- {rec}")
        
        print("\n" + "="*80)

def main():
    """Main function to run the full analysis"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze full Bollywood dataset for gender bias')
    parser.add_argument('--processed_data_path', default='processed_data', 
                       help='Path to processed data directory')
    parser.add_argument('--sequential', action='store_true', 
                       help='Use sequential processing instead of parallel')
    parser.add_argument('--processes', type=int, default=None,
                       help='Number of processes for parallel processing')
    
    args = parser.parse_args()
    
    # Set up multiprocessing
    if args.processes:
        mp.set_start_method('spawn', force=True)
    
    analyzer = FullDatasetAnalyzer(args.processed_data_path)
    analyzer.run_full_analysis(use_parallel=not args.sequential)

if __name__ == "__main__":
    main()
