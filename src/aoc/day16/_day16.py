from __future__ import annotations

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from math import prod
from typing import Any, Callable, Iterable, Type, TypeVar


# Mypy does not fully support a Comparable abstract type, this is a workaround, but not great
class Comparable(metaclass=ABCMeta):
    @abstractmethod
    def __lt__(self, other: Any) -> bool:
        ...


T = TypeVar("T")
CT = TypeVar("CT", bound=Comparable)


@dataclass
class _PacketBase:

    version: int
    p_type: int


@dataclass
class LiteralPacket(_PacketBase):

    literal: int


@dataclass
class OperatorPacket(_PacketBase):

    packets: list[_PacketBase]


def _decode_operator(bin_text: str) -> tuple[list[_PacketBase], str]:
    length_type_id, bin_text = bin_text[0] == "1", bin_text[1:]

    packets = []

    if length_type_id:
        # 11 bits = no. packets
        len_packets, bin_text = int(bin_text[:11], 2), bin_text[11:]
        for _ in range(len_packets):
            packet, bin_text = _decode(bin_text)
            packets.append(packet)
    else:
        # 15 bits = no. bits
        len_bits, bin_text = int(bin_text[:15], 2), bin_text[15:]
        used_bits = 0
        while used_bits < len_bits:
            curr_len = len(bin_text)
            packet, bin_text = _decode(bin_text)
            new_len = len(bin_text)
            used_bits += curr_len - new_len
            packets.append(packet)

    return packets, bin_text


def _decode_literal(bin_text: str) -> tuple[int, str]:
    literal = ""
    while True:
        pack, bin_text = bin_text[:5], bin_text[5:]
        literal += pack[1:]
        if pack[0] == "0":
            break
    return int(literal, 2), bin_text


def _decode(bin_text: str) -> tuple[_PacketBase, str]:
    version = int(bin_text[:3], 2)
    p_type = int(bin_text[3:6], 2)

    if p_type == 4:
        literal, remaining = _decode_literal(bin_text[6:])
        return LiteralPacket(version, p_type, literal), remaining
    else:
        packets, remaining = _decode_operator(bin_text[6:])
        return OperatorPacket(version, p_type, packets), remaining


def _sum_versions(packet: _PacketBase) -> int:
    if isinstance(packet, LiteralPacket):
        return packet.version
    elif isinstance(packet, OperatorPacket):
        return packet.version + sum(_sum_versions(p) for p in packet.packets)
    else:
        raise Exception("Abtrasct instance")


def _eval(packet: _PacketBase) -> int:
    # Worked on the first try B)
    if isinstance(packet, LiteralPacket):
        return packet.literal
    elif isinstance(packet, OperatorPacket):

        def _gt(__iterable: Iterable[CT]) -> int:
            fst, snd = __iterable
            return 1 if fst > snd else 0

        def _lt(__iterable: Iterable[CT]) -> int:
            fst, snd = __iterable
            return 1 if fst < snd else 0

        def _eq(__iterable: Iterable[T]) -> int:
            fst, snd = __iterable
            return 1 if fst == snd else 0

        # Here the workaround from Comparable fails
        type_op_map: dict[int, Callable[[Iterable[int]], int]] = {
            0: sum,
            1: prod,
            2: min,
            3: max,
            5: _gt,  # type: ignore
            6: _lt,  # type: ignore
            7: _eq,
        }
        op = type_op_map[packet.p_type]

        return op(_eval(p) for p in packet.packets)
    else:
        raise Exception("Abstract instance")


def solve(input_text: str) -> tuple[int, int]:

    bin_text = bin(int(input_text, 16))[2:].zfill(len(input_text) * 4)

    packet, _ = _decode(bin_text)

    versions = _sum_versions(packet)

    value = _eval(packet)

    return versions, value
