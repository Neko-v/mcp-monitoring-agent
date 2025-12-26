# /agent/main.py

import sys
from langchain_core.messages import HumanMessage
from graph import app

def main():
    print("==================================================")
    print(" BD-SRE Agent is Online. (Powered by LangGraph)")
    print(" Type 'quit' or 'exit' to stop.")
    print("==================================================")

    while True:
        try:
            user_input = input("\nUser (You): ")
            if user_input.lower() in ["quit", "exit"]:
                print("Goodbye!")
                break
            
            # Construct the input message
            inputs = {"messages": [HumanMessage(content=user_input)]}
            
            # Stream the results so we can see the thought process
            # stream_mode="values" will give us the updated state after each step
            print("\nAgent Thinking...", flush=True)
            
            # Running the graph using app.stream
            # config={"recursion_limit": 10} prevents infinite loops
            for event in app.stream(inputs, config={"recursion_limit": 15}):
                # Print the status at each step for easier debugging
                for key, value in event.items():
                    # The key here could be "agent" or "tools"
                    # The value contains the latest messages
                    last_msg = value["messages"][-1]
                    
                    if last_msg.type == "ai":
                        # If the AI ​​decides to call tools
                        if last_msg.tool_calls:
                            print(f"\n[Step: Decided to Call Tool]")
                            for tc in last_msg.tool_calls:
                                print(f"  --> Tool: {tc['name']}")
                                print(f"  --> Args: {tc['args']}")
                        # If the AI ​​only provides a response
                        else:
                            print(f"\n[Step: Final Answer]\n{last_msg.content}")
                            
                    elif last_msg.type == "tool":
                        print(f"\n[Step: Tool Output]")
                        # The first 200 characters are extracted to prevent spamming
                        output_preview = str(last_msg.content)[:200]
                        print(f"  --> Result: {output_preview}...")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()