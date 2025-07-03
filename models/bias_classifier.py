import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split, cross_val_score
import joblib
from typing import Dict, List, Tuple, Any
import re

class BiasClassifier:
    """
    Machine Learning classifier for bias detection with F1 >= 85% target
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 3),
            stop_words='english'
        )
        self.occupation_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.agency_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.appearance_classifier = LogisticRegression(random_state=42)
        self.relationship_classifier = LogisticRegression(random_state=42)
        
        self.is_trained = False
        self.performance_metrics = {}
    
    def create_training_data(self) -> Tuple[List[str], List[Dict[str, int]]]:
        """Create comprehensive training data for bias classification"""
        
        # Occupation Gap Training Data
        occupation_examples = [
            # High bias examples
            ("Sonia Saxena, daughter of Mr Saxena", {"occupation_gap": 1}),
            ("Priya, wife of businessman Raj", {"occupation_gap": 1}),
            ("Meet Kavya, sister of the famous director", {"occupation_gap": 1}),
            ("Anjali belongs to a wealthy family", {"occupation_gap": 1}),
            ("Rohit is an engineer while Meera is his girlfriend", {"occupation_gap": 1}),
            
            # Low bias examples
            ("Dr. Sonia Saxena, a cardiologist and daughter of Mr Saxena", {"occupation_gap": 0}),
            ("Priya, a successful lawyer, is married to businessman Raj", {"occupation_gap": 0}),
            ("Software engineer Kavya, sister of the famous director", {"occupation_gap": 0}),
            ("Anjali works as a marketing executive in Mumbai", {"occupation_gap": 0}),
            ("Both Rohit and Meera are engineers working in the same company", {"occupation_gap": 0}),
        ]
        
        # Agency Gap Training Data
        agency_examples = [
            # High bias examples
            ("Priya waits for her father's decision", {"agency_gap": 1}),
            ("Sonia receives a car as a birthday gift", {"agency_gap": 1}),
            ("Meera follows her husband's advice", {"agency_gap": 1}),
            ("Anjali hopes for a better future", {"agency_gap": 1}),
            ("Kavya accepts her fate quietly", {"agency_gap": 1}),
            
            # Low bias examples
            ("Priya decides to start her own business", {"agency_gap": 0}),
            ("Sonia chooses to pursue her medical career", {"agency_gap": 0}),
            ("Meera leads the project team successfully", {"agency_gap": 0}),
            ("Anjali creates a new marketing strategy", {"agency_gap": 0}),
            ("Kavya fights for women's rights in her community", {"agency_gap": 0}),
        ]
        
        # Appearance Focus Training Data
        appearance_examples = [
            # High bias examples
            ("Beautiful Priya catches everyone's attention", {"appearance_focus": 1}),
            ("Gorgeous Sonia is the most attractive girl in college", {"appearance_focus": 1}),
            ("Pretty Meera has lovely eyes and fair skin", {"appearance_focus": 1}),
            ("Stunning Anjali is known for her beauty", {"appearance_focus": 1}),
            ("Elegant Kavya is admired for her graceful appearance", {"appearance_focus": 1}),
            
            # Low bias examples
            ("Intelligent Priya solves complex problems", {"appearance_focus": 0}),
            ("Determined Sonia works hard to achieve her goals", {"appearance_focus": 0}),
            ("Creative Meera designs innovative solutions", {"appearance_focus": 0}),
            ("Brave Anjali stands up for justice", {"appearance_focus": 0}),
            ("Skilled Kavya excels in her profession", {"appearance_focus": 0}),
        ]
        
        # Relationship Defining Training Data
        relationship_examples = [
            # High bias examples
            ("Priya, daughter of the minister", {"relationship_defining": 1}),
            ("Sonia, wife of the businessman", {"relationship_defining": 1}),
            ("Meera belongs to the Sharma family", {"relationship_defining": 1}),
            ("Anjali is engaged to Rohit", {"relationship_defining": 1}),
            ("Kavya, girlfriend of the hero", {"relationship_defining": 1}),
            
            # Low bias examples
            ("Dr. Priya Sharma, a renowned surgeon", {"relationship_defining": 0}),
            ("CEO Sonia leads the company", {"relationship_defining": 0}),
            ("Professor Meera teaches at the university", {"relationship_defining": 0}),
            ("Lawyer Anjali fights for justice", {"relationship_defining": 0}),
            ("Engineer Kavya designs bridges", {"relationship_defining": 0}),
        ]
        
        # Combine all examples
        all_examples = occupation_examples + agency_examples + appearance_examples + relationship_examples
        
        texts = [example[0] for example in all_examples]
        labels = []
        
        for _, label_dict in all_examples:
            combined_label = {
                'occupation_gap': label_dict.get('occupation_gap', 0),
                'agency_gap': label_dict.get('agency_gap', 0),
                'appearance_focus': label_dict.get('appearance_focus', 0),
                'relationship_defining': label_dict.get('relationship_defining', 0)
            }
            labels.append(combined_label)
        
        return texts, labels
    
    def train_classifiers(self) -> Dict[str, float]:
        """Train all bias classifiers and return performance metrics"""
        
        # Create training data
        texts, labels = self.create_training_data()
        
        # Vectorize texts
        X = self.vectorizer.fit_transform(texts)
        
        # Prepare labels for each bias type
        y_occupation = [label['occupation_gap'] for label in labels]
        y_agency = [label['agency_gap'] for label in labels]
        y_appearance = [label['appearance_focus'] for label in labels]
        y_relationship = [label['relationship_defining'] for label in labels]
        
        # Train classifiers and calculate metrics
        metrics = {}
        
        # Occupation Gap Classifier
        X_train, X_test, y_train, y_test = train_test_split(X, y_occupation, test_size=0.3, random_state=42)
        self.occupation_classifier.fit(X_train, y_train)
        y_pred = self.occupation_classifier.predict(X_test)
        metrics['occupation_gap_f1'] = f1_score(y_test, y_pred)
        
        # Agency Gap Classifier
        X_train, X_test, y_train, y_test = train_test_split(X, y_agency, test_size=0.3, random_state=42)
        self.agency_classifier.fit(X_train, y_train)
        y_pred = self.agency_classifier.predict(X_test)
        metrics['agency_gap_f1'] = f1_score(y_test, y_pred)
        
        # Appearance Focus Classifier
        X_train, X_test, y_train, y_test = train_test_split(X, y_appearance, test_size=0.3, random_state=42)
        self.appearance_classifier.fit(X_train, y_train)
        y_pred = self.appearance_classifier.predict(X_test)
        metrics['appearance_focus_f1'] = f1_score(y_test, y_pred)
        
        # Relationship Defining Classifier
        X_train, X_test, y_train, y_test = train_test_split(X, y_relationship, test_size=0.3, random_state=42)
        self.relationship_classifier.fit(X_train, y_train)
        y_pred = self.relationship_classifier.predict(X_test)
        metrics['relationship_defining_f1'] = f1_score(y_test, y_pred)
        
        # Overall F1 score
        metrics['overall_f1'] = np.mean(list(metrics.values()))
        
        self.performance_metrics = metrics
        self.is_trained = True
        
        return metrics
    
    def predict_bias(self, text: str) -> Dict[str, float]:
        """Predict bias scores for given text"""
        if not self.is_trained:
            raise ValueError("Classifiers must be trained before prediction")
        
        # Vectorize input text
        X = self.vectorizer.transform([text])
        
        # Get predictions from all classifiers
        predictions = {
            'occupation_gap': self.occupation_classifier.predict_proba(X)[0][1],
            'agency_gap': self.agency_classifier.predict_proba(X)[0][1],
            'appearance_focus': self.appearance_classifier.predict_proba(X)[0][1],
            'relationship_defining': self.relationship_classifier.predict_proba(X)[0][1]
        }
        
        # Calculate overall bias score
        predictions['overall'] = np.mean(list(predictions.values()))
        
        return predictions
    
    def save_models(self, filepath: str):
        """Save trained models"""
        model_data = {
            'vectorizer': self.vectorizer,
            'occupation_classifier': self.occupation_classifier,
            'agency_classifier': self.agency_classifier,
            'appearance_classifier': self.appearance_classifier,
            'relationship_classifier': self.relationship_classifier,
            'performance_metrics': self.performance_metrics,
            'is_trained': self.is_trained
        }
        joblib.dump(model_data, filepath)
    
    def load_models(self, filepath: str):
        """Load trained models"""
        model_data = joblib.load(filepath)
        self.vectorizer = model_data['vectorizer']
        self.occupation_classifier = model_data['occupation_classifier']
        self.agency_classifier = model_data['agency_classifier']
        self.appearance_classifier = model_data['appearance_classifier']
        self.relationship_classifier = model_data['relationship_classifier']
        self.performance_metrics = model_data['performance_metrics']
        self.is_trained = model_data['is_trained']
