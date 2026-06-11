import json
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

load_dotenv()

#########################################################
# ✅ GROQ + LITELLM (CORRECT CONFIG)
#########################################################

llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

#########################################################
# LOAD DATABASE
#########################################################

with open("passport_db.json", "r") as f:
    DB = json.load(f)

#########################################################
# USER INPUT
#########################################################

user = {
    "age": 24,
    "profession": "private sector",
    "urgency": "express",
    "pages": 64,
    "requested_validity": 10,
    "has_nid": True,
    "city": "Dhaka"
}

#########################################################
# POLICY LOGIC
#########################################################

def passport_policy(age):
    if age < 18:
        return {"validity": 5, "id": "Birth Registration"}
    elif age > 65:
        return {"validity": 5, "id": "NID"}
    else:
        return {"validity": 10, "id": "NID"}

policy = passport_policy(user["age"])

#########################################################
# POLICY CHECK
#########################################################

policy_flag = "No Issues"
if user["requested_validity"] != policy["validity"]:
    policy_flag = "Requested validity violates policy"

#########################################################
# FEE CALCULATION
#########################################################

page_key = f'{user["pages"]}_pages'
year_key = f'{policy["validity"]}_years'
speed = user["urgency"]

total_fee = DB["fees_2026"][page_key][year_key][speed]

#########################################################
# DOCUMENTS
#########################################################

documents = DB["required_docs"]["adult"].copy()

if user["profession"] == "government":
    documents += DB["required_docs"].get("government_staff", [])

documents.append(policy["id"])

#########################################################
# AGENTS (FIXED)
#########################################################

policy_agent = Agent(
    role="Policy Guardian",
    goal="Check passport eligibility and rules",
    backstory="Experienced Bangladesh passport officer",
    llm=llm,
    verbose=True
)

fee_agent = Agent(
    role="Fee Calculator",
    goal="Calculate passport fees accurately",
    backstory="Government finance analyst",
    llm=llm,
    verbose=True
)

doc_agent = Agent(
    role="Document Specialist",
    goal="Prepare required document checklist",
    backstory="Passport documentation expert",
    llm=llm,
    verbose=True
)

#########################################################
# TASKS
#########################################################

task1 = Task(
    description=f"""
Applicant age: {user['age']}
Requested validity: {user['requested_validity']}

Check eligibility and policy compliance.
""",
    expected_output="Eligibility report",
    agent=policy_agent
)

task2 = Task(
    description=f"""
Calculate passport fee:

Pages: {user['pages']}
Validity: {policy['validity']}
Speed: {speed}
""",
    expected_output="Fee report",
    agent=fee_agent,
    context=[task1]
)

task3 = Task(
    description="""
Generate complete document checklist for passport application.
""",
    expected_output="Document list",
    agent=doc_agent,
    context=[task1, task2]
)

#########################################################
# CREW
#########################################################

crew = Crew(
    agents=[policy_agent, fee_agent, doc_agent],
    tasks=[task1, task2, task3],
    verbose=True
)

#########################################################
# RUN SAFELY
#########################################################

try:
    result = crew.kickoff()
    print("\n================ CREW RESULT ================\n")
    print(result)

except Exception as e:
    print("\n❌ Crew Execution Failed:", e)

#########################################################
# LOCAL FALLBACK (ALWAYS WORKS)
#########################################################

print("\n================ LOCAL REPORT ================\n")

print("| Item | Result |")
print("|------|--------|")
print(f"| Validity | {policy['validity']} Years |")
print(f"| Delivery | {speed.title()} |")
print(f"| Total Fee | {total_fee} BDT |")
print(f"| Required ID | {policy['id']} |")
print(f"| Documents | {', '.join(set(documents))} |")
print(f"| Policy Status | {policy_flag} |")

print("\nবাংলা রিপোর্ট\n")
print(f"পাসপোর্টের মেয়াদ: {policy['validity']} বছর")
print(f"ডেলিভারি: {speed}")
print(f"মোট ফি: {total_fee} টাকা")
print(f"প্রয়োজনীয় আইডি: {policy['id']}")

print("\nডকুমেন্ট:")
for d in set(documents):
    print("-", d)

print("\nস্ট্যাটাস:", policy_flag)