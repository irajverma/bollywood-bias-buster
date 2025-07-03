import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support, accuracy_score, confusion_matrix
from typing import Dict, List, Tuple, Any
import json
from pathlib import Path

class BiasDetectionEvaluator:
    """
    Comprehensive evaluation system with F1 >= 85% and rewrite quality >= 4/5 targets
    """
    
    def __init__(self):
        self.ground_truth_data = self._create_ground_truth_dataset()
        self.evaluation_results = {}
    
    def _create_ground_truth_dataset(self) -> List[Dict[str, Any]]:
        """Create comprehensive ground truth dataset for evaluation"""
        
        ground_truth = [
            # High bias examples
            {
                'text': "Sonia Saxena, daughter of Mr Saxena, is beautiful and comes from a wealthy family",
                'labels': {
                    'occupation_gap': 1,
                    'agency_gap': 0,
                    'appearance_focus': 1,
                    'relationship_defining': 1,
                    'overall_bias': 1
                },
                'characters': [
                    {'name': 'Sonia Saxena', 'gender': 'female', 'has_profession': False, 'relationship_defined': True}
                ]
            },
            {
                'text': "Rohit is an aspiring singer who works as a salesman. Priya waits for her father's decision",
                'labels': {
                    'occupation_gap': 1,
                    'agency_gap': 1,
                    'appearance_focus': 0,
                    'relationship_defining': 0,
                    'overall_bias': 1
                },
                'characters': [
                    {'name': 'Rohit', 'gender': 'male', 'has_profession': True, 'relationship_defined': False},
                    {'name': 'Priya', 'gender': 'female', 'has_profession': False, 'relationship_defined': False}
                ]
            },
            {
                'text': "Beautiful Meera, wife of businessman Raj, hopes for a better future",
                'labels': {
                    'occupation_gap': 1,
                    'agency_gap': 1,
                    'appearance_focus': 1,
                    'relationship_defining': 1,
                    'overall_bias': 1
                },
                'characters': [
                    {'name': 'Meera', 'gender': 'female', 'has_profession': False, 'relationship_defined': True},
                    {'name': 'Raj', 'gender': 'male', 'has_profession': True, 'relationship_defined': False}
                ]
            },
            
            # Low bias examples
            {
                'text': "Dr. Sonia Saxena, a cardiologist and daughter of Mr Saxena, decides to open her own clinic",
                'labels': {
                    'occupation_gap': 0,
                    'agency_gap': 0,
                    'appearance_focus': 0,
                    'relationship_defining': 0,
                    'overall_bias': 0
                },
                'characters': [
                    {'name': 'Sonia Saxena', 'gender': 'female', 'has_profession': True, 'relationship_defined': False}
                ]
            },
            {
                'text': "Engineer Priya leads the project team while her colleague Rohit provides technical support",
                'labels': {
                    'occupation_gap': 0,
                    'agency_gap': 0,
                    'appearance_focus': 0,
                    'relationship_defining': 0,
                    'overall_bias': 0
                },
                'characters': [
                    {'name': 'Priya', 'gender': 'female', 'has_profession': True, 'relationship_defined': False},
                    {'name': 'Rohit', 'gender': 'male', 'has_profession': True, 'relationship_defined': False}
                ]
            },
            {
                'text': "Determined Meera, a successful lawyer, creates innovative legal strategies",
                'labels': {
                    'occupation_gap': 0,
                    'agency_gap': 0,
                    'appearance_focus': 0,
                    'relationship_defining': 0,
                    'overall_bias': 0
                },
                'characters': [
                    {'name': 'Meera', 'gender': 'female', 'has_profession': True, 'relationship_defined': False}
                ]
            },
            
            # Medium bias examples
            {
                'text': "Kavya works as a teacher but still waits for her husband's approval for major decisions",
                'labels': {
                    'occupation_gap': 0,
                    'agency_gap': 1,
                    'appearance_focus': 0,
                    'relationship_defining': 1,
                    'overall_bias': 1
                },
                'characters': [
                    {'name': 'Kavya', 'gender': 'female', 'has_profession': True, 'relationship_defined': True}
                ]
            },
            {
                'text': "Intelligent Anjali is known for her beauty and works as a marketing executive",
                'labels': {
                    'occupation_gap': 0,
                    'agency_gap': 0,
                    'appearance_focus': 1,
                    'relationship_defining': 0,
                    'overall_bias': 0
                },
                'characters': [
                    {'name': 'Anjali', 'gender': 'female', 'has_profession': True, 'relationship_defined': False}
                ]
            }
        ]
        
        return ground_truth
    
    def evaluate_bias_detection(self, bias_detector) -> Dict[str, float]:
        """Evaluate bias detection performance"""
        
        predictions = []
        ground_truth_labels = []
        
        # Test on ground truth dataset
        for item in self.ground_truth_data:
            # Get model predictions
            try:
                # Simulate character extraction and bias scoring
                characters = bias_detector.extract_characters_advanced(item['text'])
                bias_scores = bias_detector.calculate_comprehensive_bias_scores(characters)
                
                # Convert bias scores to binary predictions (threshold = 50)
                pred_labels = {
                    'occupation_gap': 1 if bias_scores.occupation_gap > 50 else 0,
                    'agency_gap': 1 if bias_scores.agency_gap > 50 else 0,
                    'appearance_focus': 1 if bias_scores.appearance_focus > 50 else 0,
                    'relationship_defining': 1 if bias_scores.relationship_defining > 50 else 0,
                    'overall_bias': 1 if bias_scores.overall > 50 else 0
                }
                
                predictions.append(pred_labels)
                ground_truth_labels.append(item['labels'])
                
            except Exception as e:
                print(f"Error evaluating item: {e}")
                continue
        
        # Calculate metrics for each bias type
        metrics = {}
        
        for bias_type in ['occupation_gap', 'agency_gap', 'appearance_focus', 'relationship_defining', 'overall_bias']:
            y_true = [item[bias_type] for item in ground_truth_labels]
            y_pred = [item[bias_type] for item in predictions]
            
            if len(set(y_true)) > 1:  # Only calculate if we have both classes
                precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='binary')
                accuracy = accuracy_score(y_true, y_pred)
                
                metrics[f'{bias_type}_precision'] = precision
                metrics[f'{bias_type}_recall'] = recall
                metrics[f'{bias_type}_f1'] = f1
                metrics[f'{bias_type}_accuracy'] = accuracy
            else:
                metrics[f'{bias_type}_precision'] = 0.0
                metrics[f'{bias_type}_recall'] = 0.0
                metrics[f'{bias_type}_f1'] = 0.0
                metrics[f'{bias_type}_accuracy'] = 0.0
        
        # Calculate overall metrics
        f1_scores = [metrics[f'{bias_type}_f1'] for bias_type in ['occupation_gap', 'agency_gap', 'appearance_focus', 'relationship_defining']]
        metrics['overall_f1'] = np.mean(f1_scores)
        metrics['meets_f1_target'] = metrics['overall_f1'] >= 0.85
        
        self.evaluation_results['bias_detection'] = metrics
        return metrics
    
    def evaluate_rewrite_quality(self, rewriter, test_cases: List[str] = None) -> Dict[str, float]:
        """Evaluate rewrite quality with target >= 4/5 (80%)"""
        
        if test_cases is None:
            test_cases = [
                "Sonia Saxena, daughter of Mr Saxena, is beautiful and waits for her father's decision",
                "Priya, wife of businessman Raj, hopes for a better future",
                "Beautiful Meera receives a car as a birthday present",
                "Kavya belongs to a wealthy family and follows her husband's advice",
                "Gorgeous Anjali is known for her stunning appearance"
            ]
        
        quality_scores = []
        bias_reduction_scores = []
        
        for test_case in test_cases:
            try:
                # Generate rewrite
                bias_types = ['occupation_gap', 'agency_gap', 'appearance_focus', 'relationship_defining']
                rewrite_result = rewriter.rewrite_text_rule_based(test_case, bias_types)
                
                # Evaluate quality dimensions
                quality_metrics = self._evaluate_single_rewrite(test_case, rewrite_result)
                
                quality_scores.append(quality_metrics['overall_quality'])
                bias_reduction_scores.append(rewrite_result.bias_reduction_score)
                
            except Exception as e:
                print(f"Error evaluating rewrite: {e}")
                quality_scores.append(0)
                bias_reduction_scores.append(0)
        
        # Calculate overall metrics
        avg_quality = np.mean(quality_scores)
        avg_bias_reduction = np.mean(bias_reduction_scores)
        
        # Convert to 5-point scale
        quality_5_point = (avg_quality / 100) * 5
        
        metrics = {
            'average_quality_score': avg_quality,
            'quality_5_point_scale': quality_5_point,
            'average_bias_reduction': avg_bias_reduction,
            'meets_quality_target': quality_5_point >= 4.0,
            'individual_scores': quality_scores,
            'individual_bias_reductions': bias_reduction_scores
        }
        
        self.evaluation_results['rewrite_quality'] = metrics
        return metrics
    
    def _evaluate_single_rewrite(self, original: str, rewrite_result) -> Dict[str, float]:
        """Evaluate a single rewrite across multiple quality dimensions"""
        
        rewritten = rewrite_result.rewritten_text
        
        quality_metrics = {
            'narrative_preservation': 0,
            'character_preservation': 0,
            'readability': 0,
            'bias_improvement': 0,
            'length_appropriateness': 0
        }
        
        # 1. Narrative Preservation (20 points)
        original_sentences = len([s for s in original.split('.') if s.strip()])
        rewritten_sentences = len([s for s in rewritten.split('.') if s.strip()])
        
        if abs(original_sentences - rewritten_sentences) <= 1:
            quality_metrics['narrative_preservation'] = 20
        elif abs(original_sentences - rewritten_sentences) <= 2:
            quality_metrics['narrative_preservation'] = 15
        else:
            quality_metrics['narrative_preservation'] = 10
        
        # 2. Character Preservation (20 points)
        import re
        original_names = set(re.findall(r'[A-Z][a-z]+', original))
        rewritten_names = set(re.findall(r'[A-Z][a-z]+', rewritten))
        
        if original_names:
            preservation_ratio = len(original_names.intersection(rewritten_names)) / len(original_names)
            quality_metrics['character_preservation'] = preservation_ratio * 20
        else:
            quality_metrics['character_preservation'] = 20
        
        # 3. Readability (20 points)
        # Basic readability check
        if rewritten and len(rewritten.split()) >= len(original.split()) * 0.8:
            quality_metrics['readability'] = 20
        else:
            quality_metrics['readability'] = 10
        
        # 4. Bias Improvement (20 points)
        bias_improvement_score = min(20, rewrite_result.bias_reduction_score / 5)
        quality_metrics['bias_improvement'] = bias_improvement_score
        
        # 5. Length Appropriateness (20 points)
        length_ratio = len(rewritten) / len(original) if len(original) > 0 else 1
        if 0.8 <= length_ratio <= 1.5:
            quality_metrics['length_appropriateness'] = 20
        elif 0.6 <= length_ratio <= 2.0:
            quality_metrics['length_appropriateness'] = 15
        else:
            quality_metrics['length_appropriateness'] = 10
        
        # Calculate overall quality
        quality_metrics['overall_quality'] = sum(quality_metrics.values())
        
        return quality_metrics
    
    def evaluate_character_detection(self, bias_detector) -> Dict[str, float]:
        """Evaluate character detection accuracy"""
        
        correct_detections = 0
        total_characters = 0
        gender_correct = 0
        gender_total = 0
        
        for item in self.ground_truth_data:
            try:
                detected_characters = bias_detector.extract_characters_advanced(item['text'])
                ground_truth_chars = item['characters']
                
                # Check character name detection
                detected_names = {char.name.lower() for char in detected_characters}
                ground_truth_names = {char['name'].lower() for char in ground_truth_chars}
                
                correct_detections += len(detected_names.intersection(ground_truth_names))
                total_characters += len(ground_truth_names)
                
                # Check gender detection
                for gt_char in ground_truth_chars:
                    detected_char = next((c for c in detected_characters if c.name.lower() == gt_char['name'].lower()), None)
                    if detected_char:
                        if detected_char.gender == gt_char['gender']:
                            gender_correct += 1
                        gender_total += 1
                
            except Exception as e:
                print(f"Error in character detection evaluation: {e}")
                continue
        
        metrics = {
            'character_detection_accuracy': correct_detections / total_characters if total_characters > 0 else 0,
            'gender_detection_accuracy': gender_correct / gender_total if gender_total > 0 else 0,
            'total_characters_tested': total_characters,
            'correct_character_detections': correct_detections,
            'correct_gender_detections': gender_correct
        }
        
        self.evaluation_results['character_detection'] = metrics
        return metrics
    
    def generate_evaluation_report(self) -> Dict[str, Any]:
        """Generate comprehensive evaluation report"""
        
        report = {
            'evaluation_summary': {
                'timestamp': pd.Timestamp.now().isoformat(),
                'total_tests_run': len(self.evaluation_results),
                'meets_all_targets': True
            },
            'detailed_results': self.evaluation_results,
            'target_compliance': {},
            'recommendations': []
        }
        
        # Check target compliance
        if 'bias_detection' in self.evaluation_results:
            bias_f1 = self.evaluation_results['bias_detection'].get('overall_f1', 0)
            report['target_compliance']['f1_score'] = {
                'target': 0.85,
                'achieved': bias_f1,
                'meets_target': bias_f1 >= 0.85
            }
            
            if bias_f1 < 0.85:
                report['evaluation_summary']['meets_all_targets'] = False
                report['recommendations'].append(f"Improve bias detection F1 score from {bias_f1:.3f} to ≥0.85")
        
        if 'rewrite_quality' in self.evaluation_results:
            quality_score = self.evaluation_results['rewrite_quality'].get('quality_5_point_scale', 0)
            report['target_compliance']['rewrite_quality'] = {
                'target': 4.0,
                'achieved': quality_score,
                'meets_target': quality_score >= 4.0
            }
            
            if quality_score < 4.0:
                report['evaluation_summary']['meets_all_targets'] = False
                report['recommendations'].append(f"Improve rewrite quality from {quality_score:.2f} to ≥4.0/5")
        
        # Add general recommendations
        if report['evaluation_summary']['meets_all_targets']:
            report['recommendations'].append("All targets met! Continue monitoring and improving the system.")
        else:
            report['recommendations'].extend([
                "Expand training data with more diverse examples",
                "Fine-tune model parameters and thresholds",
                "Implement additional quality checks and validation",
                "Consider ensemble methods for improved performance"
            ])
        
        return report
    
    def save_evaluation_results(self, filepath: str):
        """Save evaluation results to file"""
        report = self.generate_evaluation_report()
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"Evaluation results saved to {filepath}")
        
        # Print summary
        print("\n" + "="*60)
        print("EVALUATION SUMMARY")
        print("="*60)
        
        if 'bias_detection' in self.evaluation_results:
            f1_score = self.evaluation_results['bias_detection']['overall_f1']
            print(f"Bias Detection F1 Score: {f1_score:.3f} (Target: ≥0.85)")
            print(f"F1 Target Met: {'✅ YES' if f1_score >= 0.85 else '❌ NO'}")
        
        if 'rewrite_quality' in self.evaluation_results:
            quality = self.evaluation_results['rewrite_quality']['quality_5_point_scale']
            print(f"Rewrite Quality Score: {quality:.2f}/5 (Target: ≥4.0)")
            print(f"Quality Target Met: {'✅ YES' if quality >= 4.0 else '❌ NO'}")
        
        if 'character_detection' in self.evaluation_results:
            char_acc = self.evaluation_results['character_detection']['character_detection_accuracy']
            gender_acc = self.evaluation_results['character_detection']['gender_detection_accuracy']
            print(f"Character Detection Accuracy: {char_acc:.3f}")
            print(f"Gender Detection Accuracy: {gender_acc:.3f}")
        
        overall_success = report['evaluation_summary']['meets_all_targets']
        print(f"\nOverall Target Compliance: {'✅ ALL TARGETS MET' if overall_success else '❌ TARGETS NOT MET'}")
        print("="*60)
