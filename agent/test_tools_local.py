# /agent/test_tools_local.py

from tools import consult_runbook

# Test runbook
print("Testing Runbook Access...")
result = consult_runbook("kafka")
print(result)

if "Kafka Consumer Lag" in result:
    print("\nRunbook test PASSED!")
else:
    print("\nRunbook test FAILED!")