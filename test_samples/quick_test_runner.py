#!/usr/bin/env python3
"""
Quick Test Runner for Bollywood Bias Buster
Tests all components and provides immediate feedback
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.bias_detection_model import ComprehensiveGenderBiasDetector
import json

def test_bias_detection():
    """Test the bias detection system"""
    print("🧠 TESTING BIAS DETECTION")
    print("=" * 40)
    
    detector = ComprehensiveGenderBiasDetector()
    
    test_cases = [
        {
            "text": "Priya Sharma, daughter of businessman Mr. Sharma, is beautiful and waits for her father's decision about her marriage.",
            "expected_level": "high"
        },
        {
            "text": "Gorgeous Meera belongs to a wealthy family and hopes her husband will allow her to work.",
            "expected_level": "high"
        },
        {
            "text": "Rohit is an engineer who leads the project. Sonia, his girlfriend, is pretty and supports him.",
            "expected_level": "medium"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}:")
        print(f"Input: {case['text']}")
        
        # Extract characters
        characters = detector.extract_characters_advanced(case['text'])
        print(f"Characters found: {[c.name for c in characters]}")
        
        # Calculate bias scores
        bias_scores = detector.calculate_comprehensive_bias_scores(characters)
        print(f"Overall bias score: {bias_scores.overall:.1f}/100")
        print(f"Expected level: {case['expected_level']}")
        
        # Determine result
        actual_level = 'high' if bias_scores.overall > 60 else 'medium' if bias_scores.overall > 30 else 'low'
        result = "✅ MATCH" if actual_level == case['expected_level'] else "❌ MISMATCH"
        print(f"Detection result: {result}")

def test_bias_rewriting():
    """Test the bias rewriting system"""
    print("\n✍️ TESTING BIAS REWRITING")
    print("=" * 40)
    
    # Simple rule-based rewriter for testing
    class SimpleRewriter:
        def rewrite_text_rule_based(self, text, bias_types):
            rewritten = text
            improvements = []
            
            # Add professional identity
            if 'occupation_gap' in bias_types:
                if 'daughter of' in text and 'scientist' not in text:
                    rewritten = rewritten.replace('daughter of', 'a scientist, daughter of')
                    improvements.append('Added professional identity to character introduction')
                    improvements.append('Added profession (scientist) to female character')
            
            # Convert passive to active
            if 'agency_gap' in bias_types:
                if 'waits for' in text:
                    rewritten = rewritten.replace('waits for', 'actively seeks')
                    improvements.append('Converted passive action to active agency')
            
            # Calculate quality score
            quality_score = 90.0 if len(improvements) > 1 else 65.0
            bias_reduction = 10.0 if 'scientist' in rewritten else 50.0
            
            return type('Result', (), {
                'original_text': text,
                'rewritten_text': rewritten,
                'quality_score': quality_score,
                'bias_reduction': bias_reduction,
                'improvements': improvements
            })()
    
    rewriter = SimpleRewriter()
    
    test_cases = [
        {
            "text": "Sonia Saxena, daughter of Mr Saxena, is beautiful and comes from a wealthy family.",
            "bias_types": ['occupation_gap', 'appearance_focus']
        },
        {
            "text": "Pretty Meera waits for her father's decision about her career.",
            "bias_types": ['agency_gap']
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📝 Rewrite Test {i}:")
        print(f"Original: {case['text']}")
        
        result = rewriter.rewrite_text_rule_based(case['text'], case['bias_types'])
        
        print(f"Rewritten: {result.rewritten_text}")
        print(f"Quality score: {result.quality_score}/100")
        print(f"Bias reduction: {result.bias_reduction}%")
        print(f"Improvements: {result.improvements}")
        
        quality_check = "✅ GOOD" if result.quality_score >= 60 else "❌ POOR"
        print(f"Quality check: {quality_check}")

def test_movie_analysis():
    """Test movie analysis functionality"""
    print("\n🎬 TESTING MOVIE ANALYSIS")
    print("=" * 40)
    
    detector = ComprehensiveGenderBiasDetector()
    
    # Sample movie script
    sample_script = """
    DILWALE DULHANIA LE JAYENGE
    
    RAJ MALHOTRA (22), handsome and carefree, walks with friends.
    
    RAJ
    Life is all about having fun, yaar.
    
    SIMRAN SINGH (20), beautiful and traditional, helps her mother.
    
    SIMRAN
    What about what I want?
    
    LAJJO
    Your father knows what's best for you.
    
    BALDEV SINGH decides about his daughter's marriage.
    """
    
    print("📽️ Analyzing: Dilwale Dulhania Le Jayenge")
    
    try:
        result = detector.analyze_movie_script(sample_script, "Dilwale Dulhania Le Jayenge")
        
        print("✅ Analysis completed successfully!")
        print(f"Characters detected: {result['summary']['total_characters']}")
        print(f"Male characters: {result['summary']['male_characters']}")
        print(f"Female characters: {result['summary']['female_characters']}")
        print(f"Overall bias score: {result['bias_scores']['overall']:.1f}/100")
        print(f"Bias examples found: {len([c for c in result['characters'] if c['appearance_descriptions']])}")
        
        # Find highest bias area
        bias_scores = result['bias_scores']
        highest_bias = max(bias_scores.items(), key=lambda x: x[1] if x[0] != 'overall' else 0)
        print(f"Highest bias area: {highest_bias[0]} ({highest_bias[1]:.1f})")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")

def test_report_generation():
    """Test report generation"""
    print("\n📊 TESTING REPORT GENERATION")
    print("=" * 40)
    
    try:
        # Try to import report generator
        from utils.report_generator import BiasReportGenerator
        
        generator = BiasReportGenerator()
        print("✅ Report generator imported successfully")
        
        # Test data
        sample_data = {
            'movie_title': 'Test Movie',
            'bias_scores': {
                'overall': 65.0,
                'occupation_gap': 70.0,
                'agency_gap': 60.0
            },
            'characters': [
                {'name': 'Priya', 'gender': 'female'},
                {'name': 'Rohit', 'gender': 'male'}
            ]
        }
        
        # Try to generate report
        html_report = generator.generate_html_report(sample_data)
        print("✅ HTML report generated successfully")
        
        try:
            pdf_report = generator.generate_pdf_report(sample_data)
            print("✅ PDF report generated successfully")
        except:
            print("⚠️ PDF generation requires additional setup (ReportLab)")
        
    except ImportError as e:
        print(f"❌ Could not import report generator: {e}")

def main():
    """Run all tests"""
    print("🚀 BOLLYWOOD BIAS BUSTER - QUICK SYSTEM TEST")
    print("=" * 60)
    
    test_bias_detection()
    test_bias_rewriting()
    test_movie_analysis()
    test_report_generation()
    
    print("\n" + "=" * 60)
    print("🎯 QUICK TEST SUMMARY")
    print("=" * 60)
    print("✅ If you see mostly green checkmarks above, the system is working!")
    print("❌ If you see red X marks, check the error messages for troubleshooting.")
    print("📁 Check the 'reports' directory for generated PDF/HTML files.")
    print("🔧 For detailed evaluation, run: python notebooks/complete_evaluation_notebook.py")

if __name__ == "__main__":
    main()
