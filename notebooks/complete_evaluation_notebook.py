"""
Complete Evaluation System - Test all components and generate metrics
"""

import sys
import os
from pathlib import Path

# Add models to path
current_dir = Path.cwd()
models_dir = current_dir / "models"
eval_dir = current_dir / "evaluation"
utils_dir = current_dir / "utils"

for directory in [models_dir, eval_dir, utils_dir]:
    if directory.exists():
        sys.path.append(str(directory))

print("🧪 Bollywood Bias Buster - Comprehensive Evaluation System")
print("=" * 60)

# Import all required modules
try:
    from bias_detection_model import ComprehensiveGenderBiasDetector
    from bias_classifier import BiasClassifier
    from bias_rewriter import LLMBiasRewriter
    from metrics_evaluator import BiasDetectionEvaluator
    from report_generator import ComprehensiveBiasReportGenerator
    print("✅ All modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all model files are in the correct directories")

def run_comprehensive_evaluation():
    """Run complete evaluation of all system components"""
    
    print("\n🔬 Starting Comprehensive Evaluation...")
    
    # Initialize components
    print("\n1️⃣ Initializing Components...")
    bias_detector = ComprehensiveGenderBiasDetector()
    bias_classifier = BiasClassifier()
    bias_rewriter = LLMBiasRewriter()
    evaluator = BiasDetectionEvaluator()
    report_generator = ComprehensiveBiasReportGenerator()
    
    print("✅ All components initialized")
    
    # Train classifier
    print("\n2️⃣ Training Bias Classifier...")
    classifier_metrics = bias_classifier.train_classifiers()
    print(f"✅ Classifier trained with F1 scores:")
    for metric, score in classifier_metrics.items():
        print(f"   • {metric}: {score:.3f}")
    
    # Evaluate bias detection
    print("\n3️⃣ Evaluating Bias Detection...")
    detection_metrics = evaluator.evaluate_bias_detection(bias_detector)
    print(f"✅ Bias detection evaluated:")
    print(f"   • Overall F1 Score: {detection_metrics['overall_f1']:.3f}")
    print(f"   • Meets F1 Target (≥0.85): {'✅ YES' if detection_metrics['meets_f1_target'] else '❌ NO'}")
    
    # Evaluate character detection
    print("\n4️⃣ Evaluating Character Detection...")
    character_metrics = evaluator.evaluate_character_detection(bias_detector)
    print(f"✅ Character detection evaluated:")
    print(f"   • Character Detection Accuracy: {character_metrics['character_detection_accuracy']:.3f}")
    print(f"   • Gender Detection Accuracy: {character_metrics['gender_detection_accuracy']:.3f}")
    
    # Evaluate rewrite quality
    print("\n5️⃣ Evaluating Rewrite Quality...")
    rewrite_metrics = evaluator.evaluate_rewrite_quality(bias_rewriter)
    print(f"✅ Rewrite quality evaluated:")
    print(f"   • Quality Score: {rewrite_metrics['quality_5_point_scale']:.2f}/5")
    print(f"   • Meets Quality Target (≥4.0): {'✅ YES' if rewrite_metrics['meets_quality_target'] else '❌ NO'}")
    print(f"   • Average Bias Reduction: {rewrite_metrics['average_bias_reduction']:.1f}%")
    
    # Generate evaluation report
    print("\n6️⃣ Generating Evaluation Report...")
    evaluation_report = evaluator.generate_evaluation_report()
    
    # Save results
    results_dir = Path("evaluation_results")
    results_dir.mkdir(exist_ok=True)
    
    evaluator.save_evaluation_results(results_dir / "comprehensive_evaluation.json")
    
    # Test sample movie analysis
    print("\n7️⃣ Testing Sample Movie Analysis...")
    sample_movie = {
        'metadata': {
            'title': 'Sample Movie',
            'year': 2023,
            'director': 'Test Director'
        },
        'combined_content': """
        Rohit is an aspiring singer who works as a salesman in a car showroom run by Malik. 
        One day he meets Sonia Saxena, daughter of Mr Saxena, when he goes to deliver a car 
        to her as a birthday present. Sonia is beautiful and comes from a wealthy family.
        """,
        'content_sources': ['script'],
        'total_content_length': 200
    }
    
    analysis_result = bias_detector.analyze_movie_comprehensive(sample_movie)
    
    if analysis_result:
        print("✅ Sample movie analysis completed")
        print(f"   • Overall Bias Score: {analysis_result['bias_scores']['overall']:.1f}/100")
        print(f"   • Characters Detected: {analysis_result['characters']['total']}")
        print(f"   • Bias Examples Found: {len(analysis_result['bias_examples'])}")
        
        # Generate sample report
        print("\n8️⃣ Generating Sample Report...")
        pdf_report = report_generator.generate_movie_report(analysis_result)
        html_report = report_generator.generate_html_report(analysis_result)
        
        print(f"✅ Reports generated:")
        print(f"   • PDF Report: {pdf_report}")
        print(f"   • HTML Report: {html_report}")
    
    # Test rewrite functionality
    print("\n9️⃣ Testing Rewrite Functionality...")
    sample_text = "Sonia Saxena, daughter of Mr Saxena, is beautiful and waits for her father's decision"
    bias_types = ['occupation_gap', 'agency_gap', 'appearance_focus', 'relationship_defining']
    
    rewrite_results = bias_rewriter.generate_multiple_rewrites(sample_text, bias_types, count=3)
    
    print(f"✅ Generated {len(rewrite_results)} rewrite options:")
    for i, result in enumerate(rewrite_results):
        print(f"   • Option {i+1}: Quality {result.quality_score:.1f}/100, Bias Reduction {result.bias_reduction_score:.1f}%")
    
    # Final summary
    print("\n" + "="*60)
    print("🎯 FINAL EVALUATION SUMMARY")
    print("="*60)
    
    all_targets_met = evaluation_report['evaluation_summary']['meets_all_targets']
    
    print(f"Overall System Performance: {'🟢 EXCELLENT' if all_targets_met else '🟡 NEEDS IMPROVEMENT'}")
    
    # Check individual targets
    if 'f1_score' in evaluation_report['target_compliance']:
        f1_data = evaluation_report['target_compliance']['f1_score']
        print(f"F1 Score Target: {f1_data['achieved']:.3f} (Target: {f1_data['target']}) {'✅' if f1_data['meets_target'] else '❌'}")
    
    if 'rewrite_quality' in evaluation_report['target_compliance']:
        quality_data = evaluation_report['target_compliance']['rewrite_quality']
        print(f"Quality Target: {quality_data['achieved']:.2f}/5 (Target: {quality_data['target']}) {'✅' if quality_data['meets_target'] else '❌'}")
    
    print(f"\nRecommendations:")
    for i, rec in enumerate(evaluation_report['recommendations']):
        print(f"{i+1}. {rec}")
    
    print("\n📁 All results saved in 'evaluation_results' and 'reports' directories")
    print("="*60)
    
    return evaluation_report

def test_individual_components():
    """Test individual components separately"""
    
    print("\n🔧 Testing Individual Components...")
    
    # Test 1: Bias Detection Model
    print("\n🧠 Testing Bias Detection Model...")
    detector = ComprehensiveGenderBiasDetector()
    
    test_text = "Rohit is an engineer. Priya, daughter of Mr. Sharma, is beautiful."
    characters = detector.extract_characters_advanced(test_text)
    bias_scores = detector.calculate_comprehensive_bias_scores(characters)
    
    print(f"✅ Detected {len(characters)} characters")
    print(f"✅ Overall bias score: {bias_scores.overall:.1f}")
    
    # Test 2: Bias Classifier
    print("\n🤖 Testing Bias Classifier...")
    classifier = BiasClassifier()
    metrics = classifier.train_classifiers()
    
    test_prediction = classifier.predict_bias("Beautiful Sonia, daughter of Mr. Saxena")
    print(f"✅ Classifier trained with overall F1: {metrics['overall_f1']:.3f}")
    print(f"✅ Sample prediction: {test_prediction['overall']:.3f}")
    
    # Test 3: Bias Rewriter
    print("\n✍️ Testing Bias Rewriter...")
    rewriter = LLMBiasRewriter()
    
    test_rewrite = rewriter.rewrite_text_rule_based(
        "Sonia, daughter of Mr. Saxena, is beautiful",
        ['occupation_gap', 'appearance_focus']
    )
    
    print(f"✅ Rewrite quality: {test_rewrite.quality_score:.1f}/100")
    print(f"✅ Bias reduction: {test_rewrite.bias_reduction_score:.1f}%")
    
    # Test 4: Report Generator
    print("\n📊 Testing Report Generator...")
    report_gen = ComprehensiveBiasReportGenerator()
    
    # Create mock analysis result
    mock_result = {
        'movie_metadata': {'title': 'Test Movie', 'year': 2023, 'director': 'Test Director'},
        'bias_scores': {
            'occupation_gap': 75.0,
            'agency_gap': 60.0,
            'appearance_focus': 80.0,
            'relationship_defining': 70.0,
            'dialogue_imbalance': 55.0,
            'screen_time_imbalance': 65.0,
            'overall': 67.5
        },
        'characters': {
            'total': 4,
            'male': 2,
            'female': 2,
            'unknown': 0,
            'character_details': []
        },
        'bias_examples': [
            {
                'bias_type': 'Occupation Gap',
                'character_name': 'Test Character',
                'excerpt': 'Test excerpt',
                'severity': 'high',
                'explanation': 'Test explanation',
                'suggestion': 'Test suggestion'
            }
        ]
    }
    
    try:
        pdf_path = report_gen.generate_movie_report(mock_result)
        html_path = report_gen.generate_html_report(mock_result)
        print(f"✅ PDF report generated: {pdf_path}")
        print(f"✅ HTML report generated: {html_path}")
    except Exception as e:
        print(f"⚠️ Report generation error (may need additional dependencies): {e}")
    
    print("\n✅ All individual component tests completed!")

# Main execution
if __name__ == "__main__":
    
    print("Choose evaluation mode:")
    print("1. Run comprehensive evaluation (recommended)")
    print("2. Test individual components only")
    print("3. Run both")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        evaluation_report = run_comprehensive_evaluation()
    elif choice == "2":
        test_individual_components()
    elif choice == "3":
        test_individual_components()
        evaluation_report = run_comprehensive_evaluation()
    else:
        print("Running comprehensive evaluation by default...")
        evaluation_report = run_comprehensive_evaluation()
    
    print("\n🎉 Evaluation completed! Check the output directories for detailed results.")
