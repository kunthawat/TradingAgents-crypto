#!/usr/bin/env python3
"""
Quick test of agent toolkit integration
"""

import sys
sys.path.insert(0, '.')

from tradingagents.agents.utils.agent_utils import AgentUtils
from datetime import datetime

# Test the agent toolkit
print('=== Testing Agent Toolkit ===')
tools = AgentUtils.get_available_tools()
gold_tools = [tool for tool in tools if 'gold' in tool.lower()]
print(f'Total tools: {len(tools)}')
print(f'Gold tools: {gold_tools}')

# Test get_gold_technical_analysis
if hasattr(AgentUtils, 'get_gold_technical_analysis'):
    print('✓ get_gold_technical_analysis found')
    end_date = datetime.now().strftime('%Y-%m-%d')
    result = AgentUtils.get_gold_technical_analysis('GOLD', end_date, 30)
    print(f'Result length: {len(result)}')
    
    # Check for issues
    has_zero_prices = '$0.00' in result
    has_realistic_prices = '$4,' in result or '$3,' in result
    
    print(f'Contains $0.00: {has_zero_prices}')
    print(f'Contains realistic prices: {has_realistic_prices}')
    print(f'First 500 chars: {result[:500]}...')
    
    if has_zero_prices and not has_realistic_prices:
        print('❌ ISSUE FOUND: Agent toolkit returning $0.00!')
    elif has_realistic_prices:
        print('✅ Agent toolkit working correctly!')
    else:
        print('⚠️  Unclear result from agent toolkit')
        
else:
    print('❌ get_gold_technical_analysis NOT found')
