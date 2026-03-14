import json
import statistics

class DataIntegrityAuditor:
    """
    Automated Auditor for Machine Learning Data Pipelines.
    Ensures statistical bounds and detects 'statistical anomalies'.
    Inspired by 'Calling Bullshit in AI' & ML training.
    """
    def __init__(self, feature_schema: dict):
        self.schema = feature_schema

    def audit_batch(self, data_batch: list):
        print("[Auditor] Initiating statistical integrity check...")
        issues = []
        for feature, bounds in self.schema.items():
            values = [row.get(feature) for row in data_batch if feature in row]
            if not values:
                issues.append(f"MISSING_FEATURE: {feature}")
                continue
            
            mean_val = statistics.mean(values)
            if mean_val < bounds["min"] or mean_val > bounds["max"]:
                issues.append(f"OUT_OF_BOUNDS: {feature} (Mean: {round(mean_val, 2)})")
        
        return {
            "status": "PASS" if not issues else "FAIL",
            "detected_issues": issues,
            "sample_size": len(data_batch)
        }

class ModelInferenceEngine:
    """
    Predictive Inference Engine with built-in audit hooks.
    """
    def __init__(self, model_name: str):
        self.model_name = model_name

    def predict(self, input_features: dict, audit_report: dict):
        if audit_report["status"] == "FAIL":
            print(f"[ModelEngine] Warning: Input audit failed. Prediction might be unreliable.")
        
        # Simulating ML Prediction Logic
        prediction = sum(input_features.values()) * 0.85
        return {
            "model": self.model_name,
            "prediction_value": round(prediction, 2),
            "confidence": 0.94 if audit_report["status"] == "PASS" else 0.45
        }

if __name__ == "__main__":
    # Test Data & Schema
    schema = {"sensor_a": {"min": 10, "max": 100}, "sensor_b": {"min": 5, "max": 50}}
    batch = [{"sensor_a": 120, "sensor_b": 25}, {"sensor_a": 115, "sensor_b": 20}] # Deliberate fail
    
    auditor = DataIntegrityAuditor(schema)
    engine = ModelInferenceEngine("Production-Regresso-v1")
    
    report = auditor.audit_batch(batch)
    inference = engine.predict(batch[0], report)
    
    print("\n--- ML Audit & Inference Report ---")
    print(json.dumps({"audit": report, "inference": inference}, indent=2))
