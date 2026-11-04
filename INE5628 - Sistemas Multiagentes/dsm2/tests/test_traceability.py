import re
from pathlib import Path

REQ_TESTS = {
    "REQ-F01": ["T-PROT-01", "T-SCEN-01"],
    "REQ-F02": ["T-PROT-02", "T-PROT-03"],
    "REQ-F03": ["T-BDI-01", "T-BDI-02"],
    "REQ-F04": ["T-SWAP-01", "T-SWAP-02"],
    "REQ-F05": ["T-OPEN-01"],
    "REQ-F06": ["T-BDI-03", "T-OPEN-02"],
    "REQ-F07": ["T-EVT-01"],
    "REQ-S01": ["T-REG-01"],
    "REQ-S02": ["T-REG-02"],
    "REQ-S03": ["T-ROOM-01"],
    "REQ-P01": ["T-PRIV-01"],
    "REQ-O01": ["T-TRACE-01"],
    "REQ-O02": ["T-OBS-01"],
    "REQ-R01": ["T-REPRO-01"],
}
NAO_IMPLEMENTADOS = {"REQ-F04"}


def ids_com_teste() -> set[str]:
    names = re.findall(r"def test_(T_[A-Z]+_\d\d)", "\n".join(p.read_text(encoding="utf-8") for p in Path(__file__).parent.glob("test_*.py")))
    return {n.replace("_", "-") for n in names}


def test_T_TRACE_01_todo_requisito_implementado_tem_teste_rastreavel():
    found = ids_com_teste()
    for req, tests in REQ_TESTS.items():
        if req in NAO_IMPLEMENTADOS:
            assert not found & set(tests), f"{req} está declarado como não implementado, mas tem teste"
        else:
            assert set(tests) <= found, f"{req} sem teste: {sorted(set(tests) - found)}"


def test_nenhum_teste_com_id_fora_da_matriz():
    mapped = {t for tests in REQ_TESTS.values() for t in tests}
    assert ids_com_teste() <= mapped
