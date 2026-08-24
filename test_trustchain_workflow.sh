#!/bin/bash

set -e

BASE_URL="http://localhost:8050/api/v1"
TELEMETRY_URL="${BASE_URL}/trust/telemetry"
STATE_URL="${BASE_URL}/trust/state"
REVOKE_URL="${BASE_URL}/trust/revoke"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo_green() { echo -e "${GREEN}$1${NC}"; }
echo_yellow() { echo -e "${YELLOW}$1${NC}"; }
echo_red() { echo -e "${RED}$1${NC}"; }

AGENT_DID="did:key:zTrustChainTestAgent$(date +%s)"

echo_yellow "===== TrustChain-AI Integration Tests ====="
echo_yellow "Using Agent DID: $AGENT_DID"
echo ""

# Helper to send telemetry
send_telemetry() {
  local success=$1
  local compliance=$2
  local latency=$3
  curl -s -X POST "$TELEMETRY_URL" \
    -H "Content-Type: application/json" \
    -d "{\"agent_did\": \"$AGENT_DID\", \"success\": $success, \"compliance_event\": \"$compliance\", \"latency_ms\": $latency}" > /dev/null
}

get_state() {
  curl -s "$STATE_URL/$AGENT_DID" | jq -r '.trust_state'
}
get_score() {
  curl -s "$STATE_URL/$AGENT_DID" | jq -r '.temporal_trust_score'
}

# Initial State
echo_yellow "Checking initial state..."
STATE=$(get_state)
echo "Initial State: $STATE"

# TEST 1: Valid agent -> successful task -> TRUSTED
echo_yellow "TEST 1: Submitting 3 successful tasks..."
send_telemetry true "" 100
send_telemetry true "" 120
send_telemetry true "" 150
STATE=$(get_state)
SCORE=$(get_score)
echo "Score: $SCORE, State: $STATE"
if [ "$STATE" != "TRUSTED" ]; then echo_red "Failed Test 1"; exit 1; fi
echo_green "PASS: TEST 1"

# TEST 2 & 6: Repeated failed tasks -> S_i(t) decreases -> SUSPICIOUS
echo_yellow "TEST 2 & 6: Submitting failed tasks to cross SUSPICIOUS threshold..."
for i in {1..5}; do send_telemetry false "" 150; done
STATE=$(get_state)
SCORE=$(get_score)
echo "Score: $SCORE, State: $STATE"
if [ "$STATE" != "SUSPICIOUS" ] && [ "$STATE" != "QUARANTINED" ]; then echo_red "Failed Test 2/6"; exit 1; fi
echo_green "PASS: TEST 2 & 6"

# TEST 3, 4, 7: Protocol violations + Latency -> QUARANTINED
echo_yellow "TEST 3, 4, 7: Submitting severe violations to cross QUARANTINED threshold..."
for i in {1..10}; do send_telemetry false "invalid_scope" 2500; done
STATE=$(get_state)
SCORE=$(get_score)
echo "Score: $SCORE, State: $STATE"
if [ "$STATE" != "QUARANTINED" ]; then echo_red "Failed Test 7"; exit 1; fi
echo_green "PASS: TEST 3, 4, 7"

# TEST 9: Agent behavior improves -> trust recovery
echo_yellow "TEST 9: Submitting many successful tasks to recover trust..."
for i in {1..20}; do send_telemetry true "" 100; done
STATE=$(get_state)
SCORE=$(get_score)
echo "Score: $SCORE, State: $STATE"
if [ "$STATE" == "QUARANTINED" ]; then echo_red "Failed Test 9"; exit 1; fi
echo_green "PASS: TEST 9"

# TEST 10: Explicit revocation
echo_yellow "TEST 10: Explicitly revoking agent..."
curl -s -X POST "$REVOKE_URL/$AGENT_DID" -H "Content-Type: application/json" -d '{"reason": "Compromised key"}' > /dev/null
STATE=$(get_state)
echo "State: $STATE"
if [ "$STATE" != "REVOKED" ]; then echo_red "Failed Test 10"; exit 1; fi
echo_green "PASS: TEST 10"

echo_green "All TrustChain-AI workflow tests passed!"
exit 0
