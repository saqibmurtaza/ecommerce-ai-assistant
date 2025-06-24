from agents import Agent, Runner, trace


print(type(trace))

spans = getattr(trace, "spans", None)
if spans:
    # process spans
    pass
else:
    print("No spans attribute found.")

if hasattr(trace, 'spans'):
    spans = getattr(trace, 'spans', None)
    if spans:
        final_output = spans[-1].attributes.get("final_output", None)
        if final_output:
            print(f"\n🧠 Agent Output:\n{final_output}\n")
        else:
            print("No final_output found in last span.")
    else:
        print("No spans found.")
else:
    print(f"trace does not have 'spans' attribute. It is of type: {type(trace)}")
