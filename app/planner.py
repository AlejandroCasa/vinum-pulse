"""Deterministic sommelier progression planner for 3-course evening menus."""

from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from app.schemas import (
    Dish,
    EveningCoursePairing,
    EveningMenuPlan,
    EveningMenuRequest,
    WineProfile,
    WineType,
)

if TYPE_CHECKING:
    from app.sommelier import SommelierEngine


def compute_fridge_tip(wine: WineProfile) -> str:
    """Return plain-language refrigeration timing without enological jargon."""
    temp = wine.serving_temp_c
    if temp <= 9.0:
        return (
            f"Mételo en la nevera 90 min antes de servir (o 25 min en cubitera "
            f"con hielo y agua salada) para disfrutarlo bien frío ({temp:.0f} °C)."
        )
    if temp <= 13.0:
        return (
            f"Mételo en la nevera 45 min antes de servir para alcanzar su "
            f"punto fresco ideal ({temp:.0f} °C)."
        )
    if temp <= 16.0:
        return (
            f"Golpe de fresco: mételo en la nevera 20 min antes de servir "
            f"({temp:.0f} °C, nunca a temperatura ambiente cálida)."
        )
    return (
        f"Refrescar 15 min en nevera antes de servir ({temp:.0f} °C, "
        "temperatura de cueva fresca)."
    )


def compute_uncork_tip(wine: WineProfile) -> str:
    """Return plain-language aeration and uncorking guidance without jargon."""
    if wine.decant_minutes >= 45:
        return (
            f"Descorchar y decantar {wine.decant_minutes} min antes de sentaros "
            "a la mesa para que respire y suavice su fuerza."
        )
    if wine.decant_minutes > 0:
        return (
            f"Descorchar {wine.decant_minutes} min antes de servir para "
            "despertar sus aromas."
        )
    if wine.wine_type == WineType.SPARKLING:
        return (
            "Abrir justo al momento de servir inclinando la botella para "
            "conservar toda su burbuja fina."
        )
    return "Descorchar y servir directamente al momento; no requiere aireación previa."


def compute_vintage_status(
    wine: WineProfile, current_year: int = 2026
) -> tuple[str, str]:
    """Compute vintage semaphore color and plain-language drinking window."""
    age = max(0, current_year - wine.vintage)
    peak_end = wine.vintage + wine.aging_potential_years
    if wine.aging_potential_years >= 15 and current_year <= peak_end:
        return (
            "gold",
            f"Gran Reserva en plenitud · ventana {wine.vintage + 2}-{peak_end}",
        )
    if age <= 2 and wine.aging_potential_years <= 5:
        return (
            "green",
            f"Joven y vibrante hoy · ventana óptima {wine.vintage}-{peak_end}",
        )
    if current_year <= peak_end:
        return (
            "green",
            f"En su cumbre hoy · ventana óptima {wine.vintage + 1}-{peak_end}",
        )
    return (
        "amber",
        f"Reserva de guarda evolucionado · ventana {wine.vintage}-{peak_end}",
    )


def compute_ambience_tip(occasion: str) -> str:
    """Suggest table atmosphere and glassware setup tailored to the occasion."""
    low = occasion.lower()
    if "romántica" in low or "romantica" in low:
        return (
            "Luz tenue cálida, música acústica suave a volumen bajo y tres copas "
            "preparadas por comensal para disfrutar la evolución sin mezclar aromas."
        )
    if "barbacoa" in low or "amigos" in low:
        return (
            "Ambiente distendido al aire libre, cubitera amplia con hielo para "
            "los blancos y servicio dinámico con copas amplias para los tintos."
        )
    if "familiar" in low or "domingo" in low:
        return (
            "Mesa amplia con mantel de lino, decantador listo para el tinto "
            "principal y servicio pausado al compás de cada plato."
        )
    if "tapas" in low or "tardeo" in low:
        return (
            "Pizarra con los pintxos, copas tulipa y copitas a mano, y ritmo "
            "ágil para maridar cada bocado en su punto óptimo."
        )
    return (
        "Ambiente relajado, copas adecuadas a cada estilo y temperatura de "
        "servicio cuidada para disfrutar cada maridaje."
    )


def build_progression_summary(
    w1: WineProfile, w2: WineProfile, w3: WineProfile, valid: bool
) -> str:
    """Generate concise editorial narrative of 3-wine sensory trajectory."""
    if valid:
        return (
            f"Progresión armónica en tres tiempos: iniciamos con la frescura ágil de "
            f"{w1.name} ({w1.appellation}), crecemos hacia la estructura y cuerpo de "
            f"{w2.name} ({w2.appellation}), y culminamos con la riqueza envolvente de "
            f"{w3.name} ({w3.appellation})."
        )
    return (
        f"Progresión audaz de contrastes entre {w1.name}, {w2.name} y {w3.name}, "
        "con alternancia de sensaciones diseñada para realzar los tres platos."
    )


def validate_dishes(
    engine: SommelierEngine, request: EveningMenuRequest
) -> tuple[Dish, Dish, Dish]:
    """Retrieve and validate the 3 required course dishes from engine catalog."""
    d1 = engine.get_dish_by_id(request.starter_dish_id)
    if not d1:
        raise ValueError(
            f"Dish '{request.starter_dish_id}' not found in gastronomic catalog."
        )
    d2 = engine.get_dish_by_id(request.main_dish_id)
    if not d2:
        raise ValueError(
            f"Dish '{request.main_dish_id}' not found in gastronomic catalog."
        )
    d3 = engine.get_dish_by_id(request.dessert_dish_id)
    if not d3:
        raise ValueError(
            f"Dish '{request.dessert_dish_id}' not found in gastronomic catalog."
        )
    return d1, d2, d3


def check_budget_viability(wines: list[WineProfile], total_budget_eur: float) -> None:
    """Ensure catalog has sufficient wines and budget covers at least 3 cheapest."""
    if len(wines) < 3:
        raise ValueError("Not enough wines in catalog to plan a 3-course menu.")
    cheapest_three = sorted(wines, key=lambda w: w.price_eur)[:3]
    min_budget = sum(w.price_eur for w in cheapest_three)
    if total_budget_eur < min_budget:
        raise ValueError(
            f"Total budget of {total_budget_eur:.2f} EUR is insufficient for a "
            "3-bottle evening menu plan."
        )


def evaluate_trio(
    w1: WineProfile,
    s1: float,
    w2: WineProfile,
    s2: float,
    w3: WineProfile,
    s3: float,
    budget: float,
) -> tuple[float, bool]:
    """Check budget and distinctness constraints and calculate score with bonus."""
    if len({w1.id, w2.id, w3.id}) < 3:
        return 0.0, False
    total_price = w1.price_eur + w2.price_eur + w3.price_eur
    if total_price > budget:
        return 0.0, False
    bonus = 5.0 if w1.sensory.body <= w2.sensory.body + 0.5 else 0.0
    return s1 + s2 + s3 + bonus, True


def find_best_trio(
    c1: list[tuple[float, WineProfile]],
    c2: list[tuple[float, WineProfile]],
    c3: list[tuple[float, WineProfile]],
    budget: float,
) -> tuple[WineProfile, WineProfile, WineProfile, float, float, float] | None:
    """Search for the highest scoring 3-wine combination satisfying budget."""
    best_score = -1.0
    best_trio: (
        tuple[WineProfile, WineProfile, WineProfile, float, float, float] | None
    ) = None
    for (s1, w1), (s2, w2), (s3, w3) in itertools.product(c1, c2, c3):
        score, ok = evaluate_trio(w1, s1, w2, s2, w3, s3, budget)
        if not ok:
            continue
        if score > best_score:
            best_score = score
            best_trio = (w1, w2, w3, s1, s2, s3)
    return best_trio


def get_course_candidates(
    all_wines: list[WineProfile],
    dish: Dish,
    engine: SommelierEngine,
    max_bottle_price: float,
) -> list[tuple[float, WineProfile]]:
    """Return top sensory-matched and economical wine candidates for a dish."""
    affordable = [w for w in all_wines if w.price_eur <= max_bottle_price]
    scored = [
        (engine.compute_compatibility_score(dish.target_sensory, w.sensory), w)
        for w in affordable
    ]
    scored.sort(key=lambda item: item[0], reverse=True)
    top_picks = scored[:12]
    cheapest = sorted(scored, key=lambda item: item[1].price_eur)[:3]
    combined_dict: dict[str, tuple[float, WineProfile]] = {}
    for sc, w in top_picks + cheapest:
        combined_dict[w.id] = (sc, w)
    return list(combined_dict.values())


def select_menu_wines(
    engine: SommelierEngine,
    d1: Dish,
    d2: Dish,
    d3: Dish,
    budget: float,
) -> tuple[WineProfile, WineProfile, WineProfile, float, float, float]:
    """Select 3 distinct wines maximizing pairing score and progression."""
    all_wines = engine.get_wines(limit=500)
    check_budget_viability(all_wines, budget)
    sorted_cheapest = sorted(all_wines, key=lambda w: w.price_eur)
    min_two = sorted_cheapest[0].price_eur + sorted_cheapest[1].price_eur
    max_single = budget - min_two

    c1 = get_course_candidates(all_wines, d1, engine, max_single)
    c2 = get_course_candidates(all_wines, d2, engine, max_single)
    c3 = get_course_candidates(all_wines, d3, engine, max_single)

    trio = find_best_trio(c1, c2, c3, budget)
    if trio is not None:
        return trio

    scored1 = [
        (engine.compute_compatibility_score(d1.target_sensory, w.sensory), w)
        for w in all_wines
    ]
    scored2 = [
        (engine.compute_compatibility_score(d2.target_sensory, w.sensory), w)
        for w in all_wines
    ]
    scored3 = [
        (engine.compute_compatibility_score(d3.target_sensory, w.sensory), w)
        for w in all_wines
    ]
    fallback = find_best_trio(scored1, scored2, scored3, budget)
    if fallback is None:
        raise ValueError(
            f"Total budget of {budget:.2f} EUR is insufficient for a "
            "3-bottle evening menu plan."
        )
    return fallback


def build_evening_course_pairing(
    course_number: int,
    course_title: str,
    dish: Dish,
    wine: WineProfile,
    score: float,
    sommelier_note: str,
) -> EveningCoursePairing:
    """Assemble a single course pairing schema with temperature and opening tips."""
    sem, label = compute_vintage_status(wine)
    return EveningCoursePairing(
        course_number=course_number,
        course_title=course_title,
        dish=dish,
        wine=wine,
        compatibility_score=score,
        fridge_tip=compute_fridge_tip(wine),
        uncork_tip=compute_uncork_tip(wine),
        vintage_semaphore=sem,
        vintage_status_label=label,
        sommelier_note=sommelier_note,
    )


def build_evening_menu_plan(
    engine: SommelierEngine, request: EveningMenuRequest
) -> EveningMenuPlan:
    """Design a 3-course evening wine progression within a global budget."""
    d1, d2, d3 = validate_dishes(engine, request)
    w1, w2, w3, s1, s2, s3 = select_menu_wines(
        engine, d1, d2, d3, request.total_budget_eur
    )

    c1 = build_evening_course_pairing(
        1,
        "Primer Plato · Entrante",
        d1,
        w1,
        s1,
        (
            f"Entrada con {w1.name}: frescura y vivacidad ideales para "
            f"abrir boca con {d1.name}."
        ),
    )
    c2 = build_evening_course_pairing(
        2,
        "Segundo Plato · Principal",
        d2,
        w2,
        s2,
        (
            f"Plato fuerte con {w2.name}: cuerpo estructurado y notas "
            f"aromáticas que armonizan con la potencia de {d2.name}."
        ),
    )
    c3 = build_evening_course_pairing(
        3,
        "Tercer Plato · Postre y Cierre",
        d3,
        w3,
        s3,
        (
            f"Broche final con {w3.name}: dulzor, fruta o burbuja "
            f"envolvente para culminar el menú junto a {d3.name}."
        ),
    )

    progression_valid = w1.sensory.body <= w2.sensory.body + 0.5
    total_price = round(w1.price_eur + w2.price_eur + w3.price_eur, 2)
    avg_score = round((s1 + s2 + s3) / 3.0, 1)

    return EveningMenuPlan(
        occasion=request.occasion,
        occasion_ambience_tip=compute_ambience_tip(request.occasion),
        total_budget_eur=request.total_budget_eur,
        total_price_eur=total_price,
        average_compatibility_score=avg_score,
        progression_valid=progression_valid,
        progression_summary=build_progression_summary(w1, w2, w3, progression_valid),
        courses=[c1, c2, c3],
        printable_card_title=f"Menú Maridaje Sommelier · {request.occasion}",
    )
