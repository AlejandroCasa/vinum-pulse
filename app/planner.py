"""Deterministic sommelier progression planner for 3-to-7 course evening menus."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.schemas import (
    CourseInput,
    Dish,
    EveningCoursePairing,
    EveningMenuPlan,
    EveningMenuRequest,
    WineProfile,
    WineType,
)

if TYPE_CHECKING:
    from app.sommelier import SommelierEngine

_ORDINAL_LABELS: tuple[str, ...] = (
    "Primer Pase",
    "Segundo Pase",
    "Tercer Pase",
    "Cuarto Pase",
    "Quinto Pase",
    "Sexto Pase",
    "Séptimo Pase",
)

_CLOSING_COURSE_TYPES: frozenset[str] = frozenset({"postre", "quesos", "cierre"})

_BeamState = tuple[float, float, frozenset[str], list[tuple[WineProfile, float]]]


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
    if wine.wine_type == WineType.VERMOUTH:
        return (
            "Servir muy frío en vaso bajo con hielo grande y un twist de piel "
            "de naranja o aceituna para despertar sus botánicos."
        )
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
            "Luz tenue cálida, música acústica suave a volumen bajo y copas "
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
            "Pizarra con los pintxos, copas tulipa y vasos bajos a mano, y ritmo "
            "ágil para maridar cada bocado en su punto óptimo."
        )
    return (
        "Ambiente relajado, copas adecuadas a cada estilo y temperatura de "
        "servicio cuidada para disfrutar cada maridaje."
    )


def build_progression_summary(wines: list[WineProfile], valid: bool) -> str:
    """Generate concise editorial narrative of a 3-to-7 wine sensory trajectory."""
    n = len(wines)
    first = wines[0]
    last = wines[-1]
    if valid:
        mid = wines[n // 2]
        return (
            f"Progresión armónica en {n} pases: iniciamos con la frescura ágil de "
            f"{first.name} ({first.appellation}), crecemos hacia la estructura de "
            f"{mid.name} ({mid.appellation}), y culminamos con la riqueza envolvente "
            f"de {last.name} ({last.appellation})."
        )
    names = ", ".join(w.name for w in wines[:-1])
    return (
        f"Progresión audaz de contrastes en {n} pases entre {names} y {last.name}, "
        "con alternancia de sensaciones diseñada para realzar cada plato."
    )


def validate_course_dishes(
    engine: SommelierEngine, request: EveningMenuRequest
) -> list[tuple[CourseInput, Dish]]:
    """Retrieve and validate all requested course dishes from engine catalog."""
    resolved: list[tuple[CourseInput, Dish]] = []
    for course in request.resolved_courses():
        dish = engine.get_dish_by_id(course.dish_id)
        if not dish:
            raise ValueError(
                f"Dish '{course.dish_id}' not found in gastronomic catalog."
            )
        resolved.append((course, dish))
    return resolved


def check_budget_viability(
    wines: list[WineProfile], total_budget_eur: float, course_count: int
) -> None:
    """Ensure catalog has enough wines and budget covers the cheapest N bottles."""
    if len(wines) < course_count:
        raise ValueError(
            f"Not enough wines in catalog to plan a {course_count}-course menu."
        )
    cheapest = sorted(wines, key=lambda w: w.price_eur)[:course_count]
    min_budget = sum(w.price_eur for w in cheapest)
    if total_budget_eur < min_budget:
        raise ValueError(
            f"Total budget of {total_budget_eur:.2f} EUR is insufficient for a "
            f"{course_count}-bottle evening menu plan."
        )


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
    cheapest = sorted(scored, key=lambda item: item[1].price_eur)[:6]
    combined: dict[str, tuple[float, WineProfile]] = {}
    for sc, wine in top_picks + cheapest:
        combined[wine.id] = (sc, wine)
    return list(combined.values())


def _compute_suffix_min_costs(
    sorted_prices: list[float], course_count: int
) -> list[float]:
    """Precompute minimum remaining cost after each course index."""
    return [sum(sorted_prices[: course_count - 1 - i]) for i in range(course_count)]


def _expand_beam_step(
    beam: list[_BeamState],
    candidates: list[tuple[float, WineProfile]],
    budget: float,
    remaining_min: float,
    is_closing: bool,
    beam_width: int = 60,
) -> list[_BeamState]:
    """Advance deterministic beam search by one course while honoring budget."""
    next_states: list[_BeamState] = []
    for total_score, total_cost, used_ids, chosen in beam:
        prev_body = chosen[-1][0].sensory.body if chosen else None
        for cand_score, wine in candidates:
            if wine.id in used_ids:
                continue
            new_cost = total_cost + wine.price_eur
            if new_cost + remaining_min > budget + 1e-6:
                continue
            bonus = (
                3.0
                if prev_body is not None
                and not is_closing
                and prev_body <= wine.sensory.body + 0.5
                else 0.0
            )
            next_states.append(
                (
                    total_score + cand_score + bonus,
                    new_cost,
                    used_ids | {wine.id},
                    [*chosen, (wine, cand_score)],
                )
            )
    next_states.sort(key=lambda st: (st[0], -st[1]), reverse=True)
    return next_states[:beam_width]


def _greedy_budget_fallback(
    all_wines: list[WineProfile],
    courses: list[tuple[CourseInput, Dish]],
    engine: SommelierEngine,
    budget: float,
) -> list[tuple[WineProfile, float]]:
    """Select cheapest-compatible distinct wines when beam search hits tight budgets."""
    sorted_cheapest = sorted(all_wines, key=lambda w: w.price_eur)
    chosen: list[tuple[WineProfile, float]] = []
    used: set[str] = set()
    spent = 0.0
    for idx, (_, dish) in enumerate(courses):
        remaining = len(courses) - 1 - idx
        avail = [w for w in sorted_cheapest if w.id not in used]
        reserve = sum(w.price_eur for w in avail[:remaining])
        max_price = budget - spent - reserve
        valid = [w for w in avail if w.price_eur <= max_price + 1e-6]
        if not valid:
            raise ValueError(
                f"Total budget of {budget:.2f} EUR is insufficient for a "
                f"{len(courses)}-bottle evening menu plan."
            )
        best_wine = max(
            valid,
            key=lambda w: engine.compute_compatibility_score(
                dish.target_sensory, w.sensory
            ),
        )
        score = engine.compute_compatibility_score(
            dish.target_sensory, best_wine.sensory
        )
        chosen.append((best_wine, score))
        used.add(best_wine.id)
        spent += best_wine.price_eur
    return chosen


def select_menu_wines(
    engine: SommelierEngine,
    courses: list[tuple[CourseInput, Dish]],
    budget: float,
) -> list[tuple[WineProfile, float]]:
    """Select N distinct wines maximizing pairing score and progression."""
    all_wines = engine.get_wines(limit=500)
    n = len(courses)
    check_budget_viability(all_wines, budget, n)

    sorted_prices = sorted(w.price_eur for w in all_wines)
    min_others = sum(sorted_prices[: n - 1])
    max_single = budget - min_others
    suffix_min = _compute_suffix_min_costs(sorted_prices, n)

    beam: list[_BeamState] = [(0.0, 0.0, frozenset(), [])]
    for idx, (course_input, dish) in enumerate(courses):
        candidates = get_course_candidates(all_wines, dish, engine, max_single)
        is_closing = course_input.course_type.strip().lower() in _CLOSING_COURSE_TYPES
        beam = _expand_beam_step(
            beam=beam,
            candidates=candidates,
            budget=budget,
            remaining_min=suffix_min[idx],
            is_closing=is_closing,
        )
        if not beam:
            return _greedy_budget_fallback(all_wines, courses, engine, budget)

    return beam[0][3]


def _build_course_sommelier_note(
    idx: int,
    total: int,
    course_type: str,
    dish: Dish,
    wine: WineProfile,
) -> str:
    """Generate a tailored sommelier note for a course position and style."""
    if idx == 0:
        return (
            f"Apertura ({course_type}) con {wine.name}: frescura y vivacidad "
            f"ideales para abrir boca con {dish.name}."
        )
    if idx == total - 1:
        return (
            f"Broche final ({course_type}) con {wine.name}: riqueza aromática, "
            f"fruta o burbuja envolvente para culminar el menú junto a {dish.name}."
        )
    return (
        f"Pase de {course_type} con {wine.name}: equilibrio de cuerpo y matices "
        f"aromáticos diseñado para armonizar con {dish.name}."
    )


def build_evening_course_pairing(
    course_number: int,
    course_type: str,
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
        course_type=course_type,
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
    """Design a flexible 3-to-7 course evening wine progression within a budget."""
    course_dishes = validate_course_dishes(engine, request)
    selected = select_menu_wines(engine, course_dishes, request.total_budget_eur)
    total_courses = len(course_dishes)

    pairings: list[EveningCoursePairing] = []
    for idx, ((course_in, dish), (wine, score)) in enumerate(
        zip(course_dishes, selected, strict=True)
    ):
        ordinal = (
            _ORDINAL_LABELS[idx] if idx < len(_ORDINAL_LABELS) else f"Pase {idx + 1}"
        )
        title = f"{ordinal} · {course_in.course_type}"
        note = _build_course_sommelier_note(
            idx=idx,
            total=total_courses,
            course_type=course_in.course_type,
            dish=dish,
            wine=wine,
        )
        pairings.append(
            build_evening_course_pairing(
                course_number=idx + 1,
                course_type=course_in.course_type,
                course_title=title,
                dish=dish,
                wine=wine,
                score=score,
                sommelier_note=note,
            )
        )

    wines = [wine for wine, _ in selected]
    scores = [score for _, score in selected]
    peak_body = max(w.sensory.body for w in wines[1:])
    progression_valid = wines[0].sensory.body <= peak_body + 0.5
    total_price = round(sum(w.price_eur for w in wines), 2)
    avg_score = round(sum(scores) / float(total_courses), 1)

    return EveningMenuPlan(
        occasion=request.occasion,
        occasion_ambience_tip=compute_ambience_tip(request.occasion),
        total_budget_eur=request.total_budget_eur,
        total_price_eur=total_price,
        average_compatibility_score=avg_score,
        progression_valid=progression_valid,
        progression_summary=build_progression_summary(wines, progression_valid),
        courses=pairings,
        printable_card_title=f"Menú Maridaje Sommelier · {request.occasion}",
    )
