#!/usr/bin/env python3
"""
Complete pipeline to preprocess and analyze the entire Bollywood dataset
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_command(command, description):
    """Run a command and handle errors"""
    logger.info(f"Starting: {description}")
    logger.info(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        logger.info(f"Completed: {description}")
        if result.stdout:
            logger.info(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed: {description}")
        logger.error(f"Error: {e.stderr}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    logger.info("Checking dependencies...")
    
    required_packages = ['pandas', 'numpy', 'spacy', 'textblob']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            logger.info(f"✓ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            logger.warning(f"✗ {package} is missing")
    
    if missing_packages:
        logger.error(f"Missing packages: {missing_packages}")
        logger.info("Install with: pip install " + " ".join(missing_packages))
        return False
    
    # Check spaCy model
    try:
        import spacy
        spacy.load("en_core_web_sm")
        logger.info("✓ spaCy English model is available")
    except OSError:
        logger.warning("✗ spaCy English model not found")
        logger.info("Install with: python -m spacy download en_core_web_sm")
        return False
    
    return True

def main():
    """Run the complete analysis pipeline"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Complete Bollywood bias analysis pipeline')
    parser.add_argument('dataset_path', help='Path to the Bollywood-Data repository')
    parser.add_argument('--skip-preprocessing', action='store_true', 
                       help='Skip preprocessing if already done')
    parser.add_argument('--sequential', action='store_true',
                       help='Use sequential processing instead of parallel')
    
    args = parser.parse_args()
    
    # Validate dataset path
    dataset_path = Path(args.dataset_path)
    if not dataset_path.exists():
        logger.error(f"Dataset path does not exist: {dataset_path}")
        return 1
    
    # Check for expected folders
    expected_folders = ['scripts-data', 'wikipedia-data', 'trailer-data', 'images-data']
    missing_folders = []
    
    for folder in expected_folders:
        if not (dataset_path / folder).exists():
            missing_folders.append(folder)
    
    if missing_folders:
        logger.warning(f"Some expected folders are missing: {missing_folders}")
        logger.info("Continuing with available data...")
    
    # Check dependencies
    if not check_dependencies():
        logger.error("Dependencies check failed. Please install missing packages.")
        return 1
    
    logger.info("="*80)
    logger.info("BOLLYWOOD BIAS ANALYSIS - COMPLETE PIPELINE")
    logger.info("="*80)
    
    # Step 1: Preprocessing (if not skipped)
    if not args.skip_preprocessing:
        logger.info("STEP 1: Data Preprocessing")
        preprocess_cmd = f"python scripts/preprocess_dataset.py {dataset_path}"
        if not run_command(preprocess_cmd, "Data preprocessing"):
            logger.error("Preprocessing failed. Cannot continue.")
            return 1
    else:
        logger.info("STEP 1: Skipping preprocessing (as requested)")
        # Check if processed data exists
        if not Path("processed_data/processed_movies.json").exists():
            logger.error("Processed data not found. Cannot skip preprocessing.")
            return 1
    
    # Step 2: Bias Analysis
    logger.info("STEP 2: Bias Analysis")
    analysis_cmd = "python scripts/analyze_full_dataset.py"
    if args.sequential:
        analysis_cmd += " --sequential"
    
    if not run_command(analysis_cmd, "Bias analysis"):
        logger.error("Analysis failed.")
        return 1
    
    # Step 3: Generate summary report
    logger.info("STEP 3: Generating Summary Report")
    
    # Check if results exist
    results_dir = Path("analysis_results")
    if results_dir.exists():
        logger.info("Analysis completed successfully!")
        logger.info(f"Results saved in: {results_dir}")
        logger.info("Files generated:")
        for file_path in results_dir.glob("*"):
            logger.info(f"  - {file_path.name}")
        
        # Display quick stats if summary exists
        summary_file = results_dir / "bias_analysis_summary.csv"
        if summary_file.exists():
            try:
                import pandas as pd
                df = pd.read_csv(summary_file)
                logger.info(f"\nQuick Statistics:")
                logger.info(f"  - Total movies analyzed: {len(df)}")
                logger.info(f"  - Average overall bias score: {df['overall_bias_score'].mean():.1f}")
                logger.info(f"  - Year range: {df['year'].min()}-{df['year'].max()}")
                logger.info(f"  - Most biased movie: {df.loc[df['overall_bias_score'].idxmax(), 'title']} ({df['overall_bias_score'].max():.1f})")
                logger.info(f"  - Least biased movie: {df.loc[df['overall_bias_score'].idxmin(), 'title']} ({df['overall_bias_score'].min():.1f})")
            except Exception as e:
                logger.warning(f"Could not display quick stats: {e}")
    
    logger.info("="*80)
    logger.info("PIPELINE COMPLETED SUCCESSFULLY!")
    logger.info("="*80)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
