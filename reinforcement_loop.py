import csv
import os
import time
from attack_module import AttackModule
from defense_module import DefenseModule

# Constants
NUM_ITERATIONS = 100
LOG_PATH = "data/logs.csv"
SLEEP_SECONDS = 5  # To avoid Gemini API rate limits

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Set your Gemini API key here or via environment variable
API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyDDKvpe02p6R-fYL0lCUDNBLWJRiBR4B78"

# Initialize attacker and defender with API key
attacker = AttackModule(api_key=API_KEY)
defender = DefenseModule(api_key=API_KEY)

correct = 0
total = 0

with open(LOG_PATH, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Iteration", "AttackQuery", "AttackOutput", "DefenseResponse", "Secure", "Accuracy", "Loss"])

    for i in range(1, NUM_ITERATIONS + 1):
        print(f"\n=== Iteration {i} ===")

        query = attacker.generate_adversarial_query(iteration=i)
        print(f"🔓 Attack Query: {query}")

        attack_output = attacker.attack(query) if hasattr(attacker, "attack") else ""
        if attack_output:
            print(f"⚔️  Attack Output: {attack_output[:100]}...")
        else:
            print("⚔️  Attack Output: <No output generated>")

        defense_response, is_secure = defender.defend(query)
        print(f"🛡️ Defense Response: {defense_response[:100]}...")
        print(f"✅ Secure: {is_secure}")

        total += 1
        if is_secure:
            correct += 1

        accuracy = correct / total
        loss = 1 - accuracy

        # Print accuracy and loss each iteration
        print(f"📊 Accuracy: {accuracy:.2%}, Loss: {loss:.4f}")

        writer.writerow([
            i,
            query,
            attack_output,
            defense_response,
            is_secure,
            f"{accuracy:.4f}",
            f"{loss:.4f}"
        ])
        f.flush()

        time.sleep(SLEEP_SECONDS)

print("\n✅ Reinforcement loop completed.")
print(f"🟢 Final Accuracy: {accuracy:.2%}")
print(f"🔴 Final Loss: {loss:.4f}")
