from .database import init_db, get_history

def main():
    init_db()
    rows = get_history()

    print("\n========== CANDIDATE HISTORY ==========")
    if not rows:
        print("No candidate records yet.")
        return

    print(f"{'ID':<4}{'Candidate':<12}{'Score':<8}{'Review':<10}{'Decision':<12}{'Status'}")
    print("-" * 65)

    for candidate_id, name, score, review, decision, status in rows:
        print(f"{candidate_id:<4}{name:<12}{score:<8}{review or '-':<10}{decision:<12}{status}")

if __name__ == "__main__":
    main()
