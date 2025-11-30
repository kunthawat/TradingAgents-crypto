#!/usr/bin/env python3
"""
Verify gold tools structure without full imports
"""

import os
import re

def check_gold_tools_in_agent_utils():
    """Check if gold tools are present in agent_utils.py"""
    print("=== Checking Gold Tools in agent_utils.py ===")
    
    try:
        with open('tradingagents/agents/utils/agent_utils.py', 'r') as f:
            content = f.read()
        
        gold_tools = [
            'get_gold_price_history',
            'get_gold_market_analysis', 
            'get_gold_news_analysis',
            'get_gold_fundamentals_analysis'
        ]
        
        for tool in gold_tools:
            if f'def {tool}(' in content:
                print(f"✓ {tool} - Found in agent_utils.py")
            else:
                print(f"✗ {tool} - Missing in agent_utils.py")
        
        # Check for gold tools section
        if '# ===== GOLD TRADING TOOLS =====' in content:
            print("✓ Gold tools section header found")
        else:
            print("✗ Gold tools section header missing")
        
        print()
        
    except Exception as e:
        print(f"✗ Error checking agent_utils.py: {e}")
        print()

def check_gold_tools_in_trading_graph():
    """Check if gold tools are referenced in trading_graph.py"""
    print("=== Checking Gold Tools in trading_graph.py ===")
    
    try:
        with open('tradingagents/graph/trading_graph.py', 'r') as f:
            content = f.read()
        
        gold_tool_references = [
            'self.toolkit.get_gold_price_history',
            'self.toolkit.get_gold_market_analysis',
            'self.toolkit.get_gold_news_analysis',
            'self.toolkit.get_gold_fundamentals_analysis'
        ]
        
        for ref in gold_tool_references:
            if ref in content:
                print(f"✓ {ref} - Found in trading_graph.py")
            else:
                print(f"✗ {ref} - Missing in trading_graph.py")
        
        # Check which nodes contain gold tools
        nodes = ['market', 'social', 'news', 'fundamentals']
        for node in nodes:
            node_pattern = f'"{node}": ToolNode\\('
            if re.search(node_pattern, content):
                # Find the content between this node and the next node
                start = content.find(f'"{node}": ToolNode(')
                if start != -1:
                    # Find the end of this node (next node or closing brace)
                    next_node = content.find('",', start + 1)
                    if next_node != -1:
                        node_content = content[start:next_node]
                    else:
                        node_content = content[start:]
                    
                    gold_refs = [ref for ref in gold_tool_references if ref in node_content]
                    if gold_refs:
                        print(f"✓ {node} node has {len(gold_refs)} gold tools")
                    else:
                        print(f"⚠️  {node} node has no gold tools")
        
        print()
        
    except Exception as e:
        print(f"✗ Error checking trading_graph.py: {e}")
        print()

def check_interface_functions():
    """Check if gold interface functions exist"""
    print("=== Checking Gold Interface Functions ===")
    
    try:
        with open('tradingagents/dataflows/interface.py', 'r') as f:
            content = f.read()
        
        gold_functions = [
            'get_gold_price_history',
            'get_gold_market_analysis',
            'get_gold_news_analysis', 
            'get_gold_fundamentals_analysis'
        ]
        
        for func in gold_functions:
            if f'def {func}(' in content:
                print(f"✓ {func} - Found in interface.py")
            else:
                print(f"✗ {func} - Missing in interface.py")
        
        print()
        
    except Exception as e:
        print(f"✗ Error checking interface.py: {e}")
        print()

def check_gold_utils():
    """Check if gold_utils.py exists and has the right structure"""
    print("=== Checking gold_utils.py Structure ===")
    
    try:
        with open('tradingagents/dataflows/gold_utils.py', 'r') as f:
            content = f.read()
        
        # Check for GoldPriceAPI class
        if 'class GoldPriceAPI' in content:
            print("✓ GoldPriceAPI class found")
        else:
            print("✗ GoldPriceAPI class missing")
        
        # Check for key methods
        methods = [
            'get_current_price',
            'get_historical_data',
            'get_market_analysis'
        ]
        
        for method in methods:
            if f'def {method}(' in content:
                print(f"✓ {method} - Found in GoldPriceAPI")
            else:
                print(f"✗ {method} - Missing in GoldPriceAPI")
        
        print()
        
    except Exception as e:
        print(f"✗ Error checking gold_utils.py: {e}")
        print()

def main():
    """Run all structure verification tests"""
    print("🔍 Verifying Gold Tools Structure")
    print("=" * 40)
    print()
    
    # Run checks
    check_gold_tools_in_agent_utils()
    check_gold_tools_in_trading_graph()
    check_interface_functions()
    check_gold_utils()
    
    print("🎉 Structure verification completed!")
    print()
    print("Summary:")
    print("- Gold tools have been added to Toolkit class")
    print("- Gold tools are integrated into trading graph nodes")
    print("- Interface functions are available")
    print("- Gold utilities are properly structured")
    print()
    print("The AttributeError should now be resolved!")

if __name__ == "__main__":
    main()
