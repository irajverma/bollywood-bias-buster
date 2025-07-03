"""
Complete Bollywood Bias Analysis - Jupyter Notebook Version
Run this cell by cell or all at once
"""

import os
import sys
from pathlib import Path

# Configuration - UPDATE THESE PATHS
DATASET_PATH = "/path/to/your/Bollywood-Data"  # ⚠️ CHANGE THIS!
SAMPLE_SIZE = 100  # Number of movies to analyze (use smaller number for testing)
RUN_FULL_ANALYSIS = False  # Set to True to analyze all movies

print("🎬 Bollywood Bias Buster - Complete Analysis")
print("=" * 50)

# Step 1: Check if dataset path exists
if not os.path.exists(DATASET_PATH):
    print("⚠️  IMPORTANT: Please update the DATASET_PATH variable!")
    print(f"Current path: {DATASET_PATH}")
    print("\nExample paths:")
    print("  - Windows: r'C:\\Users\\YourName\\Downloads\\Bollywood-Data'")
    print("  - Mac/Linux: '/Users/YourName/Downloads/Bollywood-Data'")
    print("  - Current directory: './Bollywood-Data'")
    print("\nAfter updating the path, run this cell again.")
else:
    print(f"✅ Dataset found at: {DATASET_PATH}")
    
    # Step 2: Import required modules
    print("\n📦 Importing required modules...")
    
    # Import preprocessing
    exec(open('notebooks/preprocess_dataset_notebook.py').read())
    
    # Import analysis
    exec(open('notebooks/analyze_dataset_notebook.py').read())
    
    print("✅ Modules imported successfully")
    
    # Step 3: Run preprocessing
    print("\n🔄 Step 1: Preprocessing dataset...")
    preprocessing_success = run_preprocessing(DATASET_PATH)
    
    if preprocessing_success:
        print("✅ Preprocessing completed!")
        
        # Step 4: Run analysis
        if RUN_FULL_ANALYSIS:
            print("\n🔍 Step 2: Running full dataset analysis...")
            print("⚠️  This may take a long time for large datasets!")
            results, report = run_full_analysis()
        else:
            print(f"\n🔍 Step 2: Running sample analysis ({SAMPLE_SIZE} movies)...")
            results, report = run_sample_analysis(SAMPLE_SIZE)
        
        if results:
            print(f"\n🎉 Analysis completed successfully!")
            print(f"📁 Results saved in 'analysis_results' folder")
            print(f"📊 {len(results)} movies analyzed")
            
            # Step 5: Show some interesting findings
            print("\n🔍 Key Findings:")
            
            if report and 'bias_scores' in report:
                avg_bias = report['bias_scores']['overall_average']
                if avg_bias > 70:
                    print(f"🔴 High bias detected (Average: {avg_bias:.1f}/100)")
                elif avg_bias > 50:
                    print(f"🟡 Moderate bias detected (Average: {avg_bias:.1f}/100)")
                else:
                    print(f"🟢 Relatively low bias (Average: {avg_bias:.1f}/100)")
            
            # Show most problematic movie
            if report and 'most_biased_movies' in report and report['most_biased_movies']:
                most_biased = report['most_biased_movies'][-1]
                print(f"📈 Most biased movie: {most_biased['title']} ({most_biased['bias_score']:.1f})")
            
            # Show best movie
            if report and 'least_biased_movies' in report and report['least_biased_movies']:
                least_biased = report['least_biased_movies'][0]
                print(f"📉 Least biased movie: {least_biased['title']} ({least_biased['bias_score']:.1f})")
            
            print(f"\n📋 Next steps:")
            print(f"1. Check 'analysis_results/analysis_summary.csv' for detailed results")
            print(f"2. Review 'analysis_results/bias_report.json' for comprehensive analysis")
            print(f"3. Examine specific bias examples in the detailed results")
            
        else:
            print("❌ Analysis failed. Check the error messages above.")
    
    else:
        print("❌ Preprocessing failed. Cannot proceed with analysis.")

print("\n" + "=" * 50)
print("Analysis complete! Check the output above for results.")
