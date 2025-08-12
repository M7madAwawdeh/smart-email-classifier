#!/usr/bin/env python3
"""
Data Validation Script for Smart Email Classifier
Validates training data quality and consistency
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Any

def validate_json_file(file_path: Path) -> Dict[str, Any]:
    """Validate a JSON training data file"""
    print(f"🔍 Validating {file_path.name}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            return {"valid": False, "error": "Data must be a list"}
        
        validation_results = {
            "valid": True,
            "total_examples": len(data),
            "categories": {},
            "confidence_range": {"min": 1.0, "max": 0.0},
            "errors": [],
            "warnings": []
        }
        
        required_fields = ["id", "subject", "body", "category", "confidence"]
        valid_categories = ["Support", "Sales", "Complaints", "Feedback", "General"]
        
        for i, item in enumerate(data):
            # Check required fields
            for field in required_fields:
                if field not in item:
                    validation_results["errors"].append(f"Example {i+1}: Missing field '{field}'")
                    validation_results["valid"] = False
            
            # Check data types
            if not isinstance(item.get("id"), int):
                validation_results["warnings"].append(f"Example {i+1}: ID should be integer")
            
            if not isinstance(item.get("subject"), str):
                validation_results["errors"].append(f"Example {i+1}: Subject must be string")
                validation_results["valid"] = False
            
            if not isinstance(item.get("body"), str):
                validation_results["errors"].append(f"Example {i+1}: Body must be string")
                validation_results["valid"] = False
            
            # Check category validity
            category = item.get("category")
            if category not in valid_categories:
                validation_results["errors"].append(f"Example {i+1}: Invalid category '{category}'")
                validation_results["valid"] = False
            
            # Track categories
            if category:
                validation_results["categories"][category] = validation_results["categories"].get(category, 0) + 1
            
            # Check confidence range
            confidence = item.get("confidence")
            if isinstance(confidence, (int, float)):
                validation_results["confidence_range"]["min"] = min(validation_results["confidence_range"]["min"], confidence)
                validation_results["confidence_range"]["max"] = max(validation_results["confidence_range"]["max"], confidence)
                
                if not 0 <= confidence <= 1:
                    validation_results["warnings"].append(f"Example {i+1}: Confidence should be between 0 and 1")
            else:
                validation_results["warnings"].append(f"Example {i+1}: Confidence should be numeric")
            
            # Check content quality
            subject = item.get("subject", "")
            body = item.get("body", "")
            
            if len(subject.strip()) < 5:
                validation_results["warnings"].append(f"Example {i+1}: Subject seems too short")
            
            if len(body.strip()) < 20:
                validation_results["warnings"].append(f"Example {i+1}: Body seems too short")
        
        return validation_results
        
    except Exception as e:
        return {"valid": False, "error": str(e)}

def validate_csv_file(file_path: Path) -> Dict[str, Any]:
    """Validate a CSV training data file"""
    print(f"🔍 Validating {file_path.name}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        
        if not data:
            return {"valid": False, "error": "CSV file is empty"}
        
        validation_results = {
            "valid": True,
            "total_examples": len(data),
            "categories": {},
            "confidence_range": {"min": 1.0, "max": 0.0},
            "errors": [],
            "warnings": []
        }
        
        required_fields = ["id", "subject", "body", "category", "confidence"]
        valid_categories = ["Support", "Sales", "Complaints", "Feedback", "General"]
        
        # Check headers
        headers = list(data[0].keys())
        missing_headers = [field for field in required_fields if field not in headers]
        if missing_headers:
            validation_results["errors"].append(f"Missing headers: {missing_headers}")
            validation_results["valid"] = False
        
        for i, row in enumerate(data):
            # Check required fields
            for field in required_fields:
                if field not in row or not row[field]:
                    validation_results["errors"].append(f"Row {i+1}: Missing or empty field '{field}'")
                    validation_results["valid"] = False
            
            # Check data types
            try:
                row_id = int(row.get("id", 0))
            except ValueError:
                validation_results["warnings"].append(f"Row {i+1}: ID should be integer")
            
            # Check category validity
            category = row.get("category")
            if category not in valid_categories:
                validation_results["errors"].append(f"Row {i+1}: Invalid category '{category}'")
                validation_results["valid"] = False
            
            # Track categories
            if category:
                validation_results["categories"][category] = validation_results["categories"].get(category, 0) + 1
            
            # Check confidence range
            try:
                confidence = float(row.get("confidence", 0))
                validation_results["confidence_range"]["min"] = min(validation_results["confidence_range"]["min"], confidence)
                validation_results["confidence_range"]["max"] = max(validation_results["confidence_range"]["max"], confidence)
                
                if not 0 <= confidence <= 1:
                    validation_results["warnings"].append(f"Row {i+1}: Confidence should be between 0 and 1")
            except ValueError:
                validation_results["warnings"].append(f"Row {i+1}: Confidence should be numeric")
            
            # Check content quality
            subject = row.get("subject", "")
            body = row.get("body", "")
            
            if len(subject.strip()) < 5:
                validation_results["warnings"].append(f"Row {i+1}: Subject seems too short")
            
            if len(body.strip()) < 20:
                validation_results["warnings"].append(f"Row {i+1}: Body seems too short")
        
        return validation_results
        
    except Exception as e:
        return {"valid": False, "error": str(e)}

def print_validation_results(results: Dict[str, Any], filename: str):
    """Print validation results in a formatted way"""
    print(f"\n📊 Validation Results for {filename}")
    print("-" * 50)
    
    if not results["valid"]:
        print("❌ Validation FAILED")
        if "error" in results:
            print(f"Error: {results['error']}")
        for error in results.get("errors", []):
            print(f"❌ {error}")
    else:
        print("✅ Validation PASSED")
        print(f"📈 Total examples: {results['total_examples']}")
        
        if results["categories"]:
            print("\n📋 Category Distribution:")
            for cat, count in results["categories"].items():
                print(f"   {cat}: {count}")
        
        if results["confidence_range"]["min"] <= results["confidence_range"]["max"]:
            print(f"\n🎯 Confidence Range: {results['confidence_range']['min']:.2f} - {results['confidence_range']['max']:.2f}")
    
    if results.get("warnings"):
        print(f"\n⚠️  Warnings ({len(results['warnings'])}):")
        for warning in results["warnings"][:5]:  # Show first 5 warnings
            print(f"   ⚠️  {warning}")
        if len(results["warnings"]) > 5:
            print(f"   ... and {len(results['warnings']) - 5} more warnings")

def main():
    """Main validation function"""
    print("🔍 Data Validation for Smart Email Classifier")
    print("=" * 50)
    
    data_dir = Path(__file__).parent
    validation_results = []
    
    # Validate all data files
    for file_path in data_dir.glob("*.json"):
        if file_path.name not in ["README.md", "load_training_data.py", "validate_data.py"]:
            results = validate_json_file(file_path)
            results["filename"] = file_path.name
            validation_results.append(results)
    
    for file_path in data_dir.glob("*.csv"):
        results = validate_csv_file(file_path)
        results["filename"] = file_path.name
        validation_results.append(results)
    
    # Print results
    for results in validation_results:
        print_validation_results(results, results["filename"])
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 VALIDATION SUMMARY")
    print("=" * 50)
    
    total_files = len(validation_results)
    valid_files = sum(1 for r in validation_results if r["valid"])
    total_examples = sum(r.get("total_examples", 0) for r in validation_results)
    
    print(f"📁 Files processed: {total_files}")
    print(f"✅ Valid files: {valid_files}")
    print(f"❌ Invalid files: {total_files - valid_files}")
    print(f"📊 Total examples: {total_examples}")
    
    if valid_files == total_files:
        print("\n🎉 All data files are valid!")
    else:
        print(f"\n⚠️  {total_files - valid_files} files have validation issues")
    
    print("\n💡 Tips:")
    print("- Fix errors before using the data for training")
    print("- Review warnings for potential data quality issues")
    print("- Ensure categories match exactly: Support, Sales, Complaints, Feedback, General")
    print("- Confidence scores should be between 0 and 1")

if __name__ == "__main__":
    main() 