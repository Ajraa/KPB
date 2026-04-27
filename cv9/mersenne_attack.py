import sys
import random
import time

sys.stdout.reconfigure(encoding="utf-8")


# Simulace napadené aplikace

def generate_lottery(seed: int, count: int = 6) -> list[int]:
    """Vygeneruje `count` čísel z <1,49> pomocí Mersenne Twisteru se seedem."""
    rng = random.Random(seed)
    return [rng.randint(1, 49) for _ in range(count)]


def simulate_target_application() -> tuple[list[int], int]:
    """
    Simuluje cílovou aplikaci: seeduje aktuálním časem a vrátí
    zachycenou posloupnost a skutečný seed (ten útočník NEZNÁ).
    """
    actual_seed = int(time.time())
    captured = generate_lottery(actual_seed)
    return captured, actual_seed


# Útok: prohledání časového okna

def attack_time_seed(captured: list[int],
                     window_seconds: int = 120) -> int | None:
    """
    Prohledá posledních `window_seconds` sekund a vrátí nalezený seed
    nebo None.
    """
    now = int(time.time())
    search_start = now - window_seconds

    print(f"  Hledám v rozsahu seedů: {search_start} – {now}")
    print(f"  Počet kandidátů       : {now - search_start + 1}")

    for candidate in range(search_start, now + 1):
        if generate_lottery(candidate) == captured:
            return candidate

    return None


# Předpověď dalších čísel

def predict_next(found_seed: int, skip: int = 6, count: int = 6) -> list[int]:
    """
    Inicializuje RNG nalezeným seedem, přeskočí prvních `skip` čísel
    (která útočník již zná) a vrátí dalších `count` čísel.
    """
    rng = random.Random(found_seed)
    for _ in range(skip):
        rng.randint(1, 49)
    return [rng.randint(1, 49) for _ in range(count)]


# Hlavní program



if __name__ == "__main__":
    print("Simulace cílové aplikace")
    captured, actual_seed = simulate_target_application()
    print(f"  Zachycená posloupnost : {captured}")
    print(f"  Skutečný seed         : {actual_seed}  (útočník toto NEZNÁ)")

    print("Útok: prohledávání časového okna (posledních 120 s)")
    t0 = time.perf_counter()
    found_seed = attack_time_seed(captured, window_seconds=120)
    elapsed = time.perf_counter() - t0

    if found_seed is None:
        print("\n  Seed NENALEZEN — aplikace mohla být spuštěna příliš dávno.")
        print("  Rozšiřte okno parametrem window_seconds.")
    else:
        print("Výsledek")
        print(f"  Nalezený seed         : {found_seed}")
        print(f"  Skutečný seed         : {actual_seed}")
        print(f"  Shoda seedů           : {'ANO [OK]' if found_seed == actual_seed else 'NE [!!]'}")
        print(f"  Doba útoku            : {elapsed * 1000:.1f} ms")

        # Ověření: přegenerovat zachycenou posloupnost
        regenerated = generate_lottery(found_seed)
        print(f"\n  Přegenerovaná posloupnost : {regenerated}")
        print(f"  Zachycená posloupnost     : {captured}")
        print(f"  Shoda sekvencí            : {'ANO [OK]' if regenerated == captured else 'NE [!!]'}")

        print("Předpověď dalších čísel v posloupnosti")
        next_numbers = predict_next(found_seed, skip=6, count=6)
        print(f"  Dalších 6 čísel (pozice 7–12) : {next_numbers}")